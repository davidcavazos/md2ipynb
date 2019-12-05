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

from . import sections


class SectionsTest(unittest.TestCase):
  def test_sections(self):
    expected = [
        [
            '# H1',
            'line 1\nline 2',
            '```\ncode 1\ncode 2\n```',
            'line 3',
        ],
        [
            '## H2',
            'line 4',
            '```\ncode 3\n```',
        ],
    ]
    actual = list(sections([
        'line 0',
        '# H1',
        'line 1\nline 2',
        '```\ncode 1\ncode 2\n```',
        'line 3',
        '## H2',
        'line 4',
        '```\ncode 3\n```',
    ]))
    self.assertEqual(expected, actual)

  def test_sections_start_on_header(self):
    expected = [['line 0'], ['# H1', 'line 1\nline 2']]
    actual = list(sections(
        input_file=[
            'line 0',
            '# H1',
            'line 1\nline 2',
        ],
        start_on_header=False,
    ))
    self.assertEqual(expected, actual)
