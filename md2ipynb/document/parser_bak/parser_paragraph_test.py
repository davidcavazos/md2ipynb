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

from ..paragraph import Paragraph

import unittest

# from . import parser as p
# from .parser import parse
# from .parser import Parser
# from .parser import _Paragraph
# from .parser_test import ParserTestCase

# p = Parser()


# Paragraph blocks are _Paragraph blocks before _parse_inlines.
# https://github.github.com/gfm/#paragraphs
# class ParserParagraphTest(ParserTestCase):
# class ParserParagraphTest(unittest.TestCase):
#     def test_one_line(self) -> None:
#         lines = ['aaa']
#         self.assertEqual(p._parse(lines), [
#             _Paragraph('aaa'),
#         ])

#     def test_one_line(self) -> None:
#         lines = ['aaa']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa'),
#         ])

#     def test_multiline(self) -> None:
#         lines = ['aaa', 'bbb', 'ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa bbb ccc'),
#         ])

#     def test_many_paragraphs(self) -> None:
#         lines = ['aaa', '', 'bbb', '', 'ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa'),
#             _Paragraph('bbb'),
#             _Paragraph('ccc'),
#         ])

#     def test_many_paragraphs_multiline(self) -> None:
#         lines = ['aaa', '', 'bbb', 'ccc', '', 'ddd', 'eee', 'fff']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa'),
#             _Paragraph('bbb ccc'),
#             _Paragraph('ddd eee fff'),
#         ])

#     def test_many_blank_lines(self) -> None:
#         lines = ['', '', 'aaa', '', '', 'bbb', '', '', '', 'ccc', '', '']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa'),
#             _Paragraph('bbb'),
#             _Paragraph('ccc'),
#         ])

#     def test_non_empty_blank_lines(self) -> None:
#         # https://github.github.com/gfm/#blank-lines
#         lines = ['aaa', ' ', 'bbb', '    ', 'ccc', '    \t', 'ddd']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa'),
#             _Paragraph('bbb'),
#             _Paragraph('ccc'),
#             _Paragraph('ddd'),
#         ])

#     def test_leading_spaces(self) -> None:
#         # Note: 4+ leading spaces create a CodeBlock
#         lines = [' aaa', '  bbb', '   ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa bbb ccc'),
#         ])

#     def test_leading_spaces_after_first_paragraph_line(self) -> None:
#         lines = ['   aaa', '    bbb', '\tccc', '    \tddd', '    ---']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa bbb ccc ddd ---'),
#         ])

#     def test_trailing_spaces(self) -> None:
#         # https://github.github.com/gfm/#soft-line-breaks
#         # https://github.github.com/gfm/#hard-line-breaks
#         lines = [
#             'aaa ',     # 1 trailing space is trimmed
#             'bbb ',     # trailing spaces at the end are trimmed
#             '',
#             'ccc  ',    # 2 or more trailing spaces are a hard line break
#             'ddd  ',    # trimmed
#             '',
#             'eee    ',  # hard line break
#             'fff    ',  # trimmed
#             '',
#             'ggg\t\t',  # tabs don't count as trailing spaces, so are trimmed
#             'hhh\t\t',  # trimmed
#         ]
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa bbb'),
#             _Paragraph('ccc\nddd'),
#             _Paragraph('eee\nfff'),
#             _Paragraph('ggg\thhh'),
#         ])

#     def test_inbetween_spaces(self) -> None:
#         lines = [
#             'a  a  a', '',
#             'b    b        b', '',
#             'c\tc\t\t\tc', '',
#             'd \t d\t \td',
#         ]
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('a a a'),
#             _Paragraph('b b b'),
#             _Paragraph('c\tc\tc'),
#             _Paragraph('d d\td'),
#         ])

#     def test_utf8(self) -> None:
#         # https://github.github.com/gfm/#textual-content
#         lines = ['🌰 🌱 🌿 🌾 🌵 🌴 🌳 🌲 🌍']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('🌰 🌱 🌿 🌾 🌵 🌴 🌳 🌲 🌍'),
#         ])
