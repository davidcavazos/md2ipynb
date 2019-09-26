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

import unittest

from . import util


class UtilTest(unittest.TestCase):
  def test_parse_attributes_no_match(self):
    expected = None
    actual = util.parse_attributes('asdf')
    self.assertEqual(expected, actual)

  def test_parse_attributes_unknown_attrib(self):
    expected = {}
    actual = util.parse_attributes('{:@}')
    self.assertEqual(expected, actual)

  def test_parse_attributes_empty(self):
    expected = {}
    actual = util.parse_attributes('{:}')
    self.assertEqual(expected, actual)

  def test_parse_attributes_id(self):
    expected = {'id': 'tag-id'}
    actual = util.parse_attributes('{:#tag-id}')
    self.assertEqual(expected, actual)

  def test_parse_attributes_classes_single(self):
    expected = {'class': ['A']}
    actual = util.parse_attributes('{:.A}')
    self.assertEqual(expected, actual)

  def test_parse_attributes_classes_multiple(self):
    expected = {'class': ['A', 'B', 'C']}
    actual = util.parse_attributes('{: .A .B .C }')
    self.assertEqual(expected, actual)

  def test_parse_attributes_custom_single(self):
    expected = {'a': 'A'}
    actual = util.parse_attributes("{:a='A'}")
    self.assertEqual(expected, actual)

  def test_parse_attributes_custom_multiple(self):
    expected = {'a': 'A', 'b': 'B', 'c': 'C'}
    actual = util.parse_attributes('''{: a='A' b="B" c='C' }''')
    self.assertEqual(expected, actual)

  def test_parse_attributes_mixed(self):
    expected = {'id': 'tag-id', 'class': ['class-A'], 'a': 'A'}
    actual = util.parse_attributes('{:#tag-id .class-A a="A"}')
    self.assertEqual(expected, actual)
