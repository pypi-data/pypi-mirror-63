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
"""Example coders."""

from __future__ import absolute_import
from __future__ import division
# Standard __future__ imports
from __future__ import print_function

# pylint: disable=unused-import
# pytype: disable=import-error
# pylint: disable=g-import-not-at-top
# See b/148667210 for why the ImportError is ignored.
try:
  from tfx_bsl.cc.tfx_bsl_extension.coders import ExamplesToRecordBatchDecoder
  from tfx_bsl.cc.tfx_bsl_extension.coders import ExampleToNumpyDict
except ImportError:
  import sys
  sys.stderr.write("Error importing tfx_bsl_extension.arrow.table_util. "
                   "Some tfx_bsl functionalities are not available")
# pylint: enable=g-import-not-at-top
# pytype: enable=import-error
# pylint: enable=unused-import
