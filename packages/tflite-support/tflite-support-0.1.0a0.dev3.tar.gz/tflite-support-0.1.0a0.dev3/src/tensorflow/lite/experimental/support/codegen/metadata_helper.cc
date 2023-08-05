/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "tensorflow/lite/experimental/support/codegen/metadata_helper.h"

#include "tensorflow/lite/experimental/support/codegen/utils.h"
#include "tensorflow/lite/experimental/support/metadata/metadata_schema_generated.h"

namespace tflite {
namespace support {
namespace codegen {

constexpr char BUFFER_KEY[] = "TFLITE_METADATA";
const ModelMetadata* GetMetadataFromModel(const Model* model) {
  for (auto i = 0; i < model->metadata()->size(); i++) {
    if (model->metadata()->Get(i)->name()->str() == BUFFER_KEY) {
      const auto buffer_index = model->metadata()->Get(i)->buffer();
      const auto* buffer = model->buffers()->Get(buffer_index)->data()->data();
      return GetModelMetadata(buffer);
    }
  }
  return nullptr;
}

void FindAssociatedFile(const TensorMetadata* metadata,
                        const std::string& tensor_identifier,
                        std::string* file_path, int* file_index,
                        ErrorReporter* err) {
  *file_path = "";
  *file_index = -1;
  if (metadata->associated_files() == nullptr ||
      metadata->associated_files()->size() == 0) {
    return;
  }
  for (int i = 0; i < metadata->associated_files()->size(); i++) {
    const auto* file_metadata = metadata->associated_files()->Get(i);
    if (file_metadata->type() == AssociatedFileType_TENSOR_AXIS_LABELS) {
      if (*file_index >= 0) {
        err->Warning(
            "Multiple associated axis label file found on tensor %s. Only the "
            "first one will be used.",
            tensor_identifier.c_str());
        continue;
      }
      *file_path = file_metadata->name()->str();
      *file_index = i;
    }
  }
}

}  // namespace codegen
}  // namespace support
}  // namespace tflite
