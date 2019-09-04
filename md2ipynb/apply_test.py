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

from . import apply


def lowercase(lines):
  for line in lines:
    yield line.lower()


def remove(lines, text='Hello'):
  for line in lines:
    yield line.replace(text, '*')


class ApplyTest(unittest.TestCase):
  def test_apply_empty(self):
    expected = []
    actual = apply([])
    self.assertEqual(expected, actual)

  def test_apply_list(self):
    expected = ['a', 'b', 'c']
    actual = apply(['a', 'b', 'c'])
    self.assertEqual(expected, actual)

  def test_apply_iterable(self):
    def get_inputs():
      yield 'a'
      yield 'b'
      yield 'c'
    expected = ['a', 'b', 'c']
    actual = apply(get_inputs())
    self.assertEqual(expected, actual)

  def test_apply(self):
    expected = ['* world', 'say hello']
    actual = list(apply(
        inputs=['Hello World', 'Say hello'],
        steps=[remove, lowercase],
    ))
    self.assertEqual(expected, actual)

  def test_apply_fn_args(self):
    expected = ['* world', 'say *']
    actual = list(apply(
        inputs=['Hello World', 'Say hello'],
        steps=[lowercase, (remove, 'hello')],
    ))
    self.assertEqual(expected, actual)
