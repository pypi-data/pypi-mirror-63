# Copyright 2019 Google LLC
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
"""Tests for tfx_bsl.coders.example_coder."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pyarrow as pa
import tensorflow as tf
from tfx_bsl.coders import example_coder

from google.protobuf import text_format
from absl.testing import absltest
from absl.testing import parameterized
from tensorflow_metadata.proto.v0 import schema_pb2


_TEST_EXAMPLES = [
    """
   features {
      feature {
        key: "x"
        value { bytes_list { value: [ "a", "b" ] } }
      }
      feature { key: "y" value { float_list { value: [ 1.0, 2.0 ] } } }
      feature { key: "z" value { int64_list { value: [ 4, 5 ] } } }
    }
    """,
    """
    features {
      feature { key: "w" value { } }
      feature { key: "x" value { } }
      feature { key: "y" value { } }
      feature { key: "z" value { } }
    }
    """,
    """
    features {
      feature { key: "v" value { float_list { value: [1.0]} } }
      feature { key: "x" value { } }
      feature { key: "y" value { } }
      feature { key: "z" value { } }
    }
        """,
    """
    features {
      feature { key: "x" value { bytes_list { value: [] } } }
      feature { key: "y" value { float_list { value: [] } } }
      feature { key: "z" value { int64_list { value: [] } } }
    }
        """,
]


_DECODE_CASES = [
    dict(
        testcase_name="without_schema_simple",
        schema_text_proto=None,
        examples_text_proto=_TEST_EXAMPLES,
        expected=pa.RecordBatch.from_arrays([
            pa.array([None, None, [1.0], None], type=pa.list_(pa.float32())),
            pa.array([None, None, None, None], type=pa.null()),
            pa.array([[b"a", b"b"], None, None, []], type=pa.list_(
                pa.binary())),
            pa.array([[1.0, 2.0], None, None, []], type=pa.list_(pa.float32())),
            pa.array([[4, 5], None, None, []], type=pa.list_(pa.int64()))
        ], ["v", "w", "x", "y", "z"])),
    dict(
        testcase_name="with_schema_simple",
        schema_text_proto="""
        feature {
          name: "x"
          type: BYTES
        }
        feature {
          name: "y"
          type: FLOAT
        }
        feature {
          name: "z"
          type: INT
        }""",
        examples_text_proto=_TEST_EXAMPLES,
        expected=pa.RecordBatch.from_arrays([
            pa.array([[b"a", b"b"], None, None, []], type=pa.list_(
                pa.binary())),
            pa.array([[1.0, 2.0], None, None, []], type=pa.list_(pa.float32())),
            pa.array([[4, 5], None, None, []], type=pa.list_(pa.int64()))
        ], ["x", "y", "z"])),
    dict(
        testcase_name="ignore_features_not_in_schema",
        schema_text_proto="""
        feature {
          name: "x"
          type: BYTES
        }
        feature {
          name: "y"
          type: FLOAT
        }
        """,
        examples_text_proto=_TEST_EXAMPLES,
        expected=pa.RecordBatch.from_arrays([
            pa.array([[b"a", b"b"], None, None, []], type=pa.list_(
                pa.binary())),
            pa.array([[1.0, 2.0], None, None, []], type=pa.list_(pa.float32())),
        ], ["x", "y"])),
    dict(
        testcase_name="build_nulls_for_unseen_feature",
        schema_text_proto="""
        feature {
          name: "a"
          type: BYTES
        }
        """,
        examples_text_proto=_TEST_EXAMPLES,
        expected=pa.RecordBatch.from_arrays([
            pa.array([None, None, None, None], type=pa.list_(pa.binary())),
        ], ["a"])),
    dict(
        testcase_name="build_null_for_unset_kind",
        schema_text_proto="""
        feature {
          name: "a"
          type: BYTES
        }
        """,
        examples_text_proto=[
            """
        features { feature { key: "a" value { } } }
        """
        ],
        expected=pa.RecordBatch.from_arrays([
            pa.array([None], type=pa.list_(pa.binary())),
        ], ["a"])),
]

_INVALID_INPUT_CASES = [
    dict(
        testcase_name="actual_type_mismatches_schema_type",
        schema_text_proto="""
        feature {
          name: "a"
          type: BYTES
        }
        """,
        examples_text_proto=[
            """
        features { feature { key: "a" value { float_list { value: [] } } } }
        """
        ],
        error=RuntimeError,
        error_msg_regex="Feature had wrong type",
    ),
    dict(
        testcase_name="no_schema_mixed_type",
        schema_text_proto=None,
        examples_text_proto=[
            """
        features { feature { key: "a" value { float_list { value: [] } } } }
        """, """
        features { feature { key: "a" value { int64_list { value: [] } } } }
        """
        ],
        error=RuntimeError,
        error_msg_regex="Feature had wrong type",
    ),
]


class ExamplesToRecordBatchDecoderTest(parameterized.TestCase):

  @parameterized.named_parameters(*_DECODE_CASES)
  def test_decode(self, schema_text_proto, examples_text_proto, expected):
    serialized_examples = [
        text_format.Merge(pbtxt, tf.train.Example()).SerializeToString()
        for pbtxt in examples_text_proto
    ]
    serialized_schema = None
    if schema_text_proto is not None:
      serialized_schema = text_format.Merge(
          schema_text_proto, schema_pb2.Schema()).SerializeToString()

    if serialized_schema:
      coder = example_coder.ExamplesToRecordBatchDecoder(serialized_schema)
    else:
      coder = example_coder.ExamplesToRecordBatchDecoder()

    result = coder.DecodeBatch(serialized_examples)
    self.assertIsInstance(result, pa.RecordBatch)
    self.assertTrue(
        result.equals(expected),
        "actual: {}\n expected:{}".format(result, expected))

  @parameterized.named_parameters(*_INVALID_INPUT_CASES)
  def test_invalid_input(self, schema_text_proto, examples_text_proto, error,
                         error_msg_regex):
    serialized_examples = [
        text_format.Merge(pbtxt, tf.train.Example()).SerializeToString()
        for pbtxt in examples_text_proto
    ]
    serialized_schema = None
    if schema_text_proto is not None:
      serialized_schema = text_format.Merge(
          schema_text_proto, schema_pb2.Schema()).SerializeToString()

    if serialized_schema:
      coder = example_coder.ExamplesToRecordBatchDecoder(serialized_schema)
    else:
      coder = example_coder.ExamplesToRecordBatchDecoder()

    with self.assertRaisesRegex(error, error_msg_regex):
      coder.DecodeBatch(serialized_examples)


if __name__ == "__main__":
  absltest.main()
