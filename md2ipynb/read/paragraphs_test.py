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

from . import paragraphs


class ParagraphsTest(unittest.TestCase):
  def test_paragraphs(self):
    actual = list(paragraphs([
        '# H1',
        'line 1',
        'line 2',
        '```',
        'code 1',
        'code 2',
        '```',
        'line 3',
    ]))
    expected = [
        '# H1',
        'line 1\nline 2',
        '```\ncode 1\ncode 2\n```',
        'line 3',
    ]
    self.assertEqual(actual, expected)

  def test_paragraphs_spaced(self):
    actual = list(paragraphs([
        '', '', '# H1',
        '', '', 'line 1',
        '', '', 'line 2',
        '', '', '```',
        '', '', 'code 1',
        '', '', 'code 2',
        '', '', '```',
        '', '', 'line 3',
        '', '',
    ]))
    expected = [
        '# H1',
        'line 1',
        'line 2',
        '```\n\n\ncode 1\n\n\ncode 2\n\n\n```',
        'line 3',
    ]
    self.assertEqual(actual, expected)
