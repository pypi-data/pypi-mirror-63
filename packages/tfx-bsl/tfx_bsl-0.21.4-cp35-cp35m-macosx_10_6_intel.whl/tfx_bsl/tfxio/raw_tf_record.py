# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TFXIO implementations for raw TF Record."""

from __future__ import absolute_import
from __future__ import division
# Standard __future__ imports
from __future__ import print_function

import apache_beam as beam
import pyarrow as pa
import tensorflow as tf  # pylint: disable=g-explicit-tensorflow-version-import
from tfx_bsl.tfxio import record_based_tfxio
from tfx_bsl.tfxio import tensor_adapter
from tfx_bsl.tfxio import tfxio
from typing import List, Optional, Text

from tensorflow_metadata.proto.v0 import schema_pb2


class _RawRecordTFXIO(record_based_tfxio.RecordBasedTFXIO):
  """Base class for raw record TFXIO implementations.

  A raw record TFXIO decodes a record based on-disk format into an
  RecordBatches of one column that contains the raw records. Its TensorAdapter
  converts one such RecordBatch into a dense string tensor that contains
  the raw records.

  `raw_record_column_name` determines the name of the raw record column and
  the tensor.
  """

  def __init__(self, raw_record_column_name: Text):
    assert raw_record_column_name is not None
    super(_RawRecordTFXIO, self).__init__(raw_record_column_name)

  def SupportAttachingRawRecords(self) -> bool:
    return True

  def RawRecordToRecordBatch(self,
                             batch_size: Optional[int] = None
                            ) -> beam.PTransform:

    @beam.ptransform_fn
    @beam.typehints.with_input_types(beam.Pipeline)
    @beam.typehints.with_output_types(pa.RecordBatch)
    def _PTransformFn(raw_record_pcoll: beam.pvalue.PCollection):
      return (raw_record_pcoll
              | 'Batch' >> beam.BatchElements(
                  **record_based_tfxio.GetBatchElementsKwargs(batch_size))
              | 'ToRecordBatch' >> beam.Map(_BatchedRecordsToArrow,
                                            self.raw_record_column_name))

    return _PTransformFn()  # pylint: disable=no-value-for-parameter

  def _ArrowSchemaNoRawRecordColumn(self) -> pa.Schema:
    # The only column is the raw record column.
    return pa.schema([])

  def TensorFlowDataset(self) -> tf.data.Dataset:
    raise NotImplementedError

  def TensorRepresentations(self) -> tensor_adapter.TensorRepresentations:
    return {
        self.raw_record_column_name:
            schema_pb2.TensorRepresentation(
                dense_tensor=schema_pb2.TensorRepresentation.DenseTensor(
                    column_name=self.raw_record_column_name,
                    shape=schema_pb2.FixedShape(),  # scalar
                ))
    }

  def _ProjectImpl(self, tensor_names: List[Text]) -> tfxio.TFXIO:
    assert (len(tensor_names) == 1 and
            tensor_names[0] == self.raw_record_column_name)
    return self


def _BatchedRecordsToArrow(records: List[bytes],
                           raw_record_column_name) -> pa.RecordBatch:
  raw_record_column = record_based_tfxio.CreateRawRecordColumn(records)
  return pa.RecordBatch.from_arrays(
      [raw_record_column], [raw_record_column_name])


class RawTfRecordTFXIO(_RawRecordTFXIO):
  """Raw record TFXIO for TFRecord format."""

  def __init__(self, file_pattern: Text, raw_record_column_name: Text):
    super(RawTfRecordTFXIO, self).__init__(raw_record_column_name)
    self._file_pattern = file_pattern

  def RawRecordBeamSource(self) -> beam.PTransform:
    @beam.ptransform_fn
    @beam.typehints.with_input_types(beam.Pipeline)
    @beam.typehints.with_output_types(bytes)
    def _PTransformFn(pipeline: beam.pvalue.PCollection):
      return pipeline | 'ReadFromTFRecord' >> beam.io.ReadFromTFRecord(
          self._file_pattern,
          coder=beam.coders.BytesCoder(),
          # TODO(b/114938612): Eventually remove this override.
          validate=False)

    return _PTransformFn()  # pylint: disable=no-value-for-parameter
