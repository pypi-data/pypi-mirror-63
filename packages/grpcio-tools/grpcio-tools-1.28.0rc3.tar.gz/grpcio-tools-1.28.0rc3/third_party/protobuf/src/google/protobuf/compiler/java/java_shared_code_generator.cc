// Protocol Buffers - Google's data interchange format
// Copyright 2008 Google Inc.  All rights reserved.
// https://developers.google.com/protocol-buffers/
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// Author: xiaofeng@google.com (Feng Xiao)

#include <google/protobuf/compiler/java/java_shared_code_generator.h>

#include <memory>

#include <google/protobuf/compiler/java/java_helpers.h>
#include <google/protobuf/compiler/java/java_name_resolver.h>
#include <google/protobuf/compiler/code_generator.h>
#include <google/protobuf/descriptor.pb.h>
#include <google/protobuf/io/printer.h>
#include <google/protobuf/io/zero_copy_stream.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/stubs/strutil.h>

namespace google {
namespace protobuf {
namespace compiler {
namespace java {

SharedCodeGenerator::SharedCodeGenerator(const FileDescriptor* file,
                                         const Options& options)
    : name_resolver_(new ClassNameResolver), file_(file), options_(options) {}

SharedCodeGenerator::~SharedCodeGenerator() {}

void SharedCodeGenerator::Generate(
    GeneratorContext* context, std::vector<std::string>* file_list,
    std::vector<std::string>* annotation_file_list) {
  std::string java_package = FileJavaPackage(file_);
  std::string package_dir = JavaPackageToDir(java_package);

  if (HasDescriptorMethods(file_, options_.enforce_lite)) {
    // Generate descriptors.
    std::string classname = name_resolver_->GetDescriptorClassName(file_);
    std::string filename = package_dir + classname + ".java";
    file_list->push_back(filename);
    std::unique_ptr<io::ZeroCopyOutputStream> output(context->Open(filename));
    GeneratedCodeInfo annotations;
    io::AnnotationProtoCollector<GeneratedCodeInfo> annotation_collector(
        &annotations);
    std::unique_ptr<io::Printer> printer(
        new io::Printer(output.get(), '$',
                        options_.annotate_code ? &annotation_collector : NULL));
    std::string info_relative_path = classname + ".java.pb.meta";
    std::string info_full_path = filename + ".pb.meta";
    printer->Print(
        "// Generated by the protocol buffer compiler.  DO NOT EDIT!\n"
        "// source: $filename$\n"
        "\n",
        "filename", file_->name());
    if (!java_package.empty()) {
      printer->Print(
          "package $package$;\n"
          "\n",
          "package", java_package);
    }
    PrintGeneratedAnnotation(printer.get(), '$',
                             options_.annotate_code ? info_relative_path : "");
    printer->Print(
        "public final class $classname$ {\n"
        "  public static com.google.protobuf.Descriptors.FileDescriptor\n"
        "      descriptor;\n"
        "  static {\n",
        "classname", classname);
    printer->Annotate("classname", file_->name());
    printer->Indent();
    printer->Indent();
    GenerateDescriptors(printer.get());
    printer->Outdent();
    printer->Outdent();
    printer->Print(
        "  }\n"
        "}\n");

    if (options_.annotate_code) {
      std::unique_ptr<io::ZeroCopyOutputStream> info_output(
          context->Open(info_full_path));
      annotations.SerializeToZeroCopyStream(info_output.get());
      annotation_file_list->push_back(info_full_path);
    }

    printer.reset();
    output.reset();
  }
}

void SharedCodeGenerator::GenerateDescriptors(io::Printer* printer) {
  // Embed the descriptor.  We simply serialize the entire FileDescriptorProto
  // and embed it as a string literal, which is parsed and built into real
  // descriptors at initialization time.  We unfortunately have to put it in
  // a string literal, not a byte array, because apparently using a literal
  // byte array causes the Java compiler to generate *instructions* to
  // initialize each and every byte of the array, e.g. as if you typed:
  //   b[0] = 123; b[1] = 456; b[2] = 789;
  // This makes huge bytecode files and can easily hit the compiler's internal
  // code size limits (error "code to large").  String literals are apparently
  // embedded raw, which is what we want.
  FileDescriptorProto file_proto;
  file_->CopyTo(&file_proto);

  std::string file_data;
  file_proto.SerializeToString(&file_data);

  printer->Print("java.lang.String[] descriptorData = {\n");
  printer->Indent();

  // Limit the number of bytes per line.
  static const int kBytesPerLine = 40;
  // Limit the number of lines per string part.
  static const int kLinesPerPart = 400;
  // Every block of bytes, start a new string literal, in order to avoid the
  // 64k length limit. Note that this value needs to be <64k.
  static const int kBytesPerPart = kBytesPerLine * kLinesPerPart;
  for (int i = 0; i < file_data.size(); i += kBytesPerLine) {
    if (i > 0) {
      if (i % kBytesPerPart == 0) {
        printer->Print(",\n");
      } else {
        printer->Print(" +\n");
      }
    }
    printer->Print("\"$data$\"", "data",
                   CEscape(file_data.substr(i, kBytesPerLine)));
  }

  printer->Outdent();
  printer->Print("\n};\n");

  // -----------------------------------------------------------------
  // Find out all dependencies.
  std::vector<std::pair<std::string, std::string> > dependencies;
  for (int i = 0; i < file_->dependency_count(); i++) {
    std::string filename = file_->dependency(i)->name();
    std::string package = FileJavaPackage(file_->dependency(i));
    std::string classname =
        name_resolver_->GetDescriptorClassName(file_->dependency(i));
    std::string full_name;
    if (package.empty()) {
      full_name = classname;
    } else {
      full_name = package + "." + classname;
    }
    dependencies.push_back(std::make_pair(filename, full_name));
  }

  // -----------------------------------------------------------------
  // Invoke internalBuildGeneratedFileFrom() to build the file.
  printer->Print(
      "descriptor = com.google.protobuf.Descriptors.FileDescriptor\n"
      "  .internalBuildGeneratedFileFrom(descriptorData,\n");
  printer->Print(
      "    new com.google.protobuf.Descriptors.FileDescriptor[] {\n");

  for (int i = 0; i < dependencies.size(); i++) {
    const std::string& dependency = dependencies[i].second;
    printer->Print("      $dependency$.getDescriptor(),\n", "dependency",
                   dependency);
  }

  printer->Print("    });\n");
}

}  // namespace java
}  // namespace compiler
}  // namespace protobuf
}  // namespace google
