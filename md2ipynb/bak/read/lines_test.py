# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import jinja2
import json
import unittest

from io import StringIO
from unittest.mock import patch

from . import lines

source_file = 'test/hello.md'
expected_file = 'test/hello-expected.md'
variables_file = 'test/hello-variables.json'

with open(source_file) as f:
  source = f.read().rstrip()
with open(expected_file) as f:
  expected = f.read().rstrip()
with open(variables_file) as f:
  variables = json.load(f)


class ReadLinesTest(unittest.TestCase):
  def test_from_iterable(self):
    actual = '\n'.join(lines(source.splitlines(), variables))
    self.assertEqual(expected, actual)

  def test_from_file(self):
    actual = '\n'.join(lines(source_file, variables))
    self.assertEqual(expected, actual)

  @patch("sys.stdin", StringIO(source))
  def test_from_stdin(self):
    actual = '\n'.join(lines(variables=variables))
    self.assertEqual(expected, actual)

  def test_no_variables(self):
    actual = '\n'.join(lines(
      source
        .replace('{{ title }}', variables['title'])
        .replace('{{name}}', variables['name'])
        .splitlines()
    ))
    self.assertEqual(expected, actual)
