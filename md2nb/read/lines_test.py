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
import unittest

from io import StringIO
from unittest.mock import patch

from . import lines

with open('examples/pages/hello-world.md') as f:
  source = f.read()

variables = {
    'title': 'Hello world',
    'name': 'md2nb',
}

expected = [
    '# Hello world',
    '',
    'Hello md2nb!',
]


class ReadLinesTest(unittest.TestCase):
  def test_from_iterable(self):
    actual = list(lines(source.splitlines(), variables))
    self.assertEqual(actual, expected)

  def test_from_file(self):
    actual = list(lines('examples/pages/hello-world.md', variables))
    self.assertEqual(actual, expected)

  @patch("sys.stdin", StringIO(source))
  def test_from_stdin(self):
    actual = list(lines(variables=variables))
    self.assertEqual(actual, expected)
