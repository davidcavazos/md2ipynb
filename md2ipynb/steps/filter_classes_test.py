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

import md2ipynb
from md2ipynb import testing

from . import filter_classes


def get_paragraphs(class_names):
  def get_paragraphs_fn(test_file):
    sections = md2ipynb.read.sections(test_file)
    return md2ipynb.apply(sections, [
        md2ipynb.steps.flatten,
        (filter_classes, class_names),
    ])
  return get_paragraphs_fn


class FilterClassesTest(unittest.TestCase):
  def test_classes_code_block_A(self):
    expected, actual = testing.compare_files(
        'test/classes-code-block.md',
        'test/classes-A-code-block-expected.md',
        get_paragraphs('classA'),
    )
    self.assertEqual(expected, actual)

  def test_classes_code_block_A_language(self):
    expected, actual = testing.compare_files(
        'test/classes-code-block.md',
        'test/classes-A-code-block-expected.md',
        get_paragraphs('language-classA'),
    )
    self.assertEqual(expected, actual)

  def test_classes_code_block_B(self):
    expected, actual = testing.compare_files(
        'test/classes-code-block.md',
        'test/classes-B-code-block-expected.md',
        get_paragraphs('classB'),
    )
    self.assertEqual(expected, actual)

  def test_classes_code_block_B_language(self):
    expected, actual = testing.compare_files(
        'test/classes-code-block.md',
        'test/classes-B-code-block-expected.md',
        get_paragraphs('language-classB'),
    )
    self.assertEqual(expected, actual)

  def test_classes_code_block_AB(self):
    expected, actual = testing.compare_files(
        'test/classes-code-block.md',
        'test/classes-AB-code-block-expected.md',
        get_paragraphs(['classA', 'classB']),
    )
    self.assertEqual(expected, actual)

  def test_classes_code_block_AB_language(self):
    expected, actual = testing.compare_files(
        'test/classes-code-block.md',
        'test/classes-AB-code-block-expected.md',
        get_paragraphs(['language-classA', 'language-classB']),
    )
    self.assertEqual(expected, actual)

  def test_classes_leading_A(self):
    expected, actual = testing.compare_files(
        'test/classes-leading.md',
        'test/classes-A-expected.md',
        get_paragraphs('classA'),
    )
    self.assertEqual(expected, actual)

  def test_classes_leading_B(self):
    expected, actual = testing.compare_files(
        'test/classes-leading.md',
        'test/classes-B-expected.md',
        get_paragraphs('classB'),
    )
    self.assertEqual(expected, actual)

  def test_classes_leading_AB(self):
    expected, actual = testing.compare_files(
        'test/classes-leading.md',
        'test/classes-AB-expected.md',
        get_paragraphs(['classA', 'classB']),
    )
    self.assertEqual(expected, actual)

  def test_classes_leading_line_A(self):
    expected, actual = testing.compare_files(
        'test/classes-leading-line.md',
        'test/classes-A-expected.md',
        get_paragraphs('classA'),
    )
    self.assertEqual(expected, actual)

  def test_classes_leading_line_B(self):
    expected, actual = testing.compare_files(
        'test/classes-leading-line.md',
        'test/classes-B-expected.md',
        get_paragraphs('classB'),
    )
    self.assertEqual(expected, actual)

  def test_classes_leading_line_AB(self):
    expected, actual = testing.compare_files(
        'test/classes-leading-line.md',
        'test/classes-AB-expected.md',
        get_paragraphs(['classA', 'classB']),
    )
    self.assertEqual(expected, actual)

  def test_classes_trailing_A(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing.md',
        'test/classes-A-expected.md',
        get_paragraphs('classA'),
    )
    self.assertEqual(expected, actual)

  def test_classes_trailing_B(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing.md',
        'test/classes-B-expected.md',
        get_paragraphs('classB'),
    )
    self.assertEqual(expected, actual)

  def test_classes_trailing_AB(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing.md',
        'test/classes-AB-expected.md',
        get_paragraphs(['classA', 'classB']),
    )
    self.assertEqual(expected, actual)

  def test_classes_trailing_line_A(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing-line.md',
        'test/classes-A-expected.md',
        get_paragraphs('classA'),
    )
    self.assertEqual(expected, actual)

  def test_classes_trailing_line_B(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing-line.md',
        'test/classes-B-expected.md',
        get_paragraphs('classB'),
    )
    self.assertEqual(expected, actual)

  def test_classes_trailing_line_AB(self):
    expected, actual = testing.compare_files(
        'test/classes-trailing-line.md',
        'test/classes-AB-expected.md',
        get_paragraphs(['classA', 'classB']),
    )
    self.assertEqual(expected, actual)

  def test_multiple_classes(self):
    expected = [
        'classA',
        'classA classB',
        'classB classA',
    ]
    actual = list(filter_classes(
        paragraphs=[
            '{:.classA}\nclassA',
            '{:.classB}\nclassB',
            '{:.classA .classB}\nclassA classB',
            '{:.classB .classA}\nclassB classA',
        ],
        keep_classes='classA',
    ))
    self.assertEqual(expected, actual)

  def test_force_filter(self):
    expected = [
        'classA',
    ]
    actual = list(filter_classes(
        paragraphs=[
            '{:.classA}\nclassA',
            '{:.classB}\nclassB',
            '{:.classA .classB}\nclassA classB',
            '{:.classB .classA}\nclassB classA',
        ],
        keep_classes='classA',
        force_filter='classB',
    ))
    self.assertEqual(expected, actual)
