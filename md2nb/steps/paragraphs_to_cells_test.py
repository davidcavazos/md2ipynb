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
  def test_paragraphs_to_cells(self):
    actual = list(paragraphs_to_cells([
        'line 0',
        '# H1',
        'line 1\nline 2',
        '```\ncode 1\n```',
        'line 3',
        '## H2',
        'line 4\nline 5',
        '```\ncode 2\n```',
        '```\ncode 3\n```',
    ]))
    expected = [
        md_cell('line 0'),
        md_cell('# H1\n\nline 1\nline 2', 'h1'),
        code_cell('code 1', 'h1-code'),
        md_cell('line 3', 'h1-2'),
        md_cell('## H2\n\nline 4\nline 5', 'h2'),
        code_cell('code 2', 'h2-code'),
        code_cell('code 3', 'h2-code-2'),
    ]
    self.assertEqual(actual, expected)
