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

import nbformat
import unittest

from . import paragraphs_to_cells


def md_cell(source, id=''):
  return nbformat.v4.new_markdown_cell(source, metadata={'id': id})


def code_cell(source, id=''):
  return nbformat.v4.new_code_cell(source, metadata={'id': id})


class ParagraphsToCellsTest(unittest.TestCase):
  def test_no_lines(self):
    actual = list(paragraphs_to_cells([
        '',
        '```\n```',
    ]))
    expected = [
        md_cell('', '_'),
        code_cell('', '_-code'),
    ]
    self.assertEqual(actual, expected)

  def test_one_line(self):
    actual = list(paragraphs_to_cells([
        'line 1',
        '```\ncode 1\n```',
    ]))
    expected = [
        md_cell('line 1', '_'),
        code_cell('code 1', '_-code'),
    ]
    self.assertEqual(actual, expected)

  def test_three_lines(self):
    actual = list(paragraphs_to_cells([
        'line 1\nline 2\nline 3',
        '```\ncode 1\ncode 2\ncode 3\n```',
    ]))
    expected = [
        md_cell('line 1\nline 2\nline 3', '_'),
        code_cell('code 1\ncode 2\ncode 3', '_-code'),
    ]
    self.assertEqual(actual, expected)

  def test_cell_id_with_headers(self):
    actual = list(paragraphs_to_cells([
        'line 0',
        '```\ncode 0\n```',
        '# H1',
        'line 1',
        '```\ncode 1\n```',
        'line 2',
        '## H2 & sym !@#$%^&*()_+~`- bols',
        '```\ncode 2\n```',
        'line 3',
        '```\ncode 3\n```',
    ]))
    expected = [
        md_cell('line 0', '_'),
        code_cell('code 0', '_-code'),
        md_cell('# H1\n\nline 1', 'h1'),
        code_cell('code 1', 'h1-code'),
        md_cell('line 2', 'h1-2'),
        md_cell('## H2 & sym !@#$%^&*()_+~`- bols', 'h2-sym-_-bols'),
        code_cell('code 2', 'h2-sym-_-bols-code'),
        md_cell('line 3', 'h2-sym-_-bols-2'),
        code_cell('code 3', 'h2-sym-_-bols-code-2'),
    ]
    self.assertEqual(actual, expected)
