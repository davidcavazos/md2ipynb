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

# Based roughly on the GitHub Flavored Markdown Spec:
#   https://github.github.com/gfm/

import unittest

from ..divider import Divider

from .parser import Parser
from .parser import _Paragraph

p = Parser()


# https://github.github.com/gfm/#thematic-breaks
class ParserDividerTest(unittest.TestCase):
    def test_divider_types(self) -> None:
        p.reset(['***', '---', '___'])
        self.assertEqual(p._parse_blocks(), [
            Divider(),
            Divider(),
            Divider(),
        ])

    def test_inbetween_text(self) -> None:
        p.reset(['aaa', '---', 'bbb'])
        self.assertEqual(p._parse_blocks(), [
            _Paragraph('aaa'),
            Divider(),
            _Paragraph('bbb'),
        ])

    def test_parse_divider_leading_spaces(self) -> None:
        # Note: 4 leading spaces create a CodeBlock
        p.reset([' ---', '  ---', '   ---'])
        self.assertEqual(p._parse_blocks(), [
            Divider(),
            Divider(),
            Divider(),
        ])

    def test_parse_divider_long(self) -> None:
        p.reset(['----------', '**********', '__________'])
        self.assertEqual(p._parse_blocks(), [
            Divider(),
            Divider(),
            Divider(),
        ])

    def test_parse_divider_with_spaces(self) -> None:
        p.reset([' - - - ', '  *  *  *  ', '   _   _   _   '])
        self.assertEqual(p._parse_blocks(), [
            Divider(),
            Divider(),
            Divider(),
        ])

    def test_parse_divider_negatives(self) -> None:
        p.reset([
            '+++', '',  # invalid characters
            '===', '',  # invalid characters
            '**', '',   # too short
            '--', '',   # too short
            '__', '',   # too short
            'a---', '',  # invalid mixed character
            '---a', '',  # invalid mixed character
            '-  -', '',  # not enough non-blank characters
            '-*-', '',  # mixed characters
        ])
        self.assertEqual(p._parse_blocks(), [
            _Paragraph('+++'),
            _Paragraph('==='),
            _Paragraph('**'),
            _Paragraph('--'),
            _Paragraph('__'),
            _Paragraph('a---'),
            _Paragraph('---a'),
            _Paragraph('-  -'),
            _Paragraph('-*-'),
        ])
