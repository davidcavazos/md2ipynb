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

from ..block_quote import BlockQuote
from ..code_block import CodeBlock

# from .parser import Parser
# from .parser import _Paragraph
# from .parser_test import ParserTestCase

# p = Parser()


# https://github.github.com/gfm/#block-quotes
# class ParserBlockQuoteTest(ParserTestCase):
#     def test_empty(self) -> None:
#         lines = ['>']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote(),
#         ])

#     def test_one_line(self) -> None:
#         lines = ['> aaa']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa')]),
#         ])

#     def test_one_line_no_space(self) -> None:
#         lines = ['>aaa']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa')]),
#         ])

#     def test_multiline(self) -> None:
#         lines = ['>aaa', '> bbb', '>   ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa bbb ccc')]),
#         ])

#     def test_multiline_many_paragraphs(self) -> None:
#         lines = ['>aaa', '>', '> bbb', '> ', '>  ', '>   ', '>   ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([
#                 _Paragraph('aaa'),
#                 _Paragraph('bbb'),
#                 _Paragraph('ccc'),
#             ]),
#         ])

#     def test_many_quote_blocks(self) -> None:
#         lines = ['> aaa', '', '> bbb', '', '> ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa')]),
#             BlockQuote([_Paragraph('bbb')]),
#             BlockQuote([_Paragraph('ccc')]),
#         ])

#     def test_many_quote_blocks_multiline(self) -> None:
#         lines = ['> aaa', '', '> bbb', '> ccc', '', '> ddd', '> eee', '> fff']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa')]),
#             BlockQuote([_Paragraph('bbb ccc')]),
#             BlockQuote([_Paragraph('ddd eee fff')]),
#         ])

#     def test_many_blank_lines(self) -> None:
#         lines = ['> aaa', '', '', '> bbb', '', '', '', '> ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa')]),
#             BlockQuote([_Paragraph('bbb')]),
#             BlockQuote([_Paragraph('ccc')]),
#         ])

#     def test_non_empty_blank_lines(self) -> None:
#         lines = ['> aaa', ' ', '> bbb', '    ', '> ccc', '    \t', '> ddd']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa')]),
#             BlockQuote([_Paragraph('bbb')]),
#             BlockQuote([_Paragraph('ccc')]),
#             BlockQuote([_Paragraph('ddd')]),
#         ])

#     def test_leading_spaces(self) -> None:
#         # Note: 4+ leading spaces create a CodeBlock
#         lines = [' >  aaa', '  >   bbb', '   >    ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BlockQuote([_Paragraph('aaa bbb ccc')]),
#         ])

#     def test_interrupt_paragraph(self) -> None:
#         lines = ['aaa', '> bbb']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             _Paragraph('aaa'),
#             BlockQuote([_Paragraph('bbb')])
#         ])

#     def test_negatives(self) -> None:
#         lines = [
#             '    > aaa',
#         ]
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             CodeBlock('> aaa'),
#         ])
