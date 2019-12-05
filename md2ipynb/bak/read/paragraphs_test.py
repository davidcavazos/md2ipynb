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

from md2ipynb import testing

from . import paragraphs


class ParagraphsTest(unittest.TestCase):
  def test_paragraphs(self):
    expected, actual = testing.compare_files(
        'test/paragraphs.md',
        'test/paragraphs-expected.md',
        paragraphs)
    self.assertEqual(expected, actual)

  @unittest.skip('TODO: fix html2md to not replace multiple newlines inside code blocks')
  def test_paragraphs_spaced(self):
    expected, actual = testing.compare_files(
        'test/paragraphs-spaced.md',
        'test/paragraphs-spaced-expected.md',
        paragraphs)
    self.assertEqual(expected, actual)

  def test_paragraph_classes_leading(self):
    expected, actual = testing.compare_files(
        'test/classes-leading.md',
        'test/classes-leading.md',
        paragraphs)
    self.assertEqual(expected, actual)

  def test_paragraph_classes_leading_line(self):
    expected, actual = testing.compare_files(
        'test/classes-leading-line.md',
        'test/classes-leading-line.md',
        paragraphs)
    self.assertEqual(expected, actual)

  def test_paragraph_classes_trailing(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing.md',
        'test/classes-trailing.md',
        paragraphs)
    self.assertEqual(expected, actual)

  def test_paragraph_classes_trailing_line(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing-line.md',
        'test/classes-trailing-line.md',
        paragraphs)
    self.assertEqual(expected, actual)
