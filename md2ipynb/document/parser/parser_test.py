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
import logging
from io import StringIO
from unittest import mock
from typing import Any

from ..block import Block
from ..element import Element

from ..document import Document

from ..code_block import CodeBlock
from ..divider import Divider
# from ..header import Header
# from ..html_block import HtmlBlock
# from ..table import Table
from ..paragraph import Paragraph

# from ..block_quote import BlockQuote
from ..bullet_list import BulletList
# from ..ordered_list import OrderedList
# from ..task_list import TaskList

# from ..comment import Comment
# from ..image import Image
# from ..link import Link
from ..text import Text

from .parser import Parser
from .parser import _Paragraph

p = Parser()


class ParserIndentsTest(unittest.TestCase):
    def test_eof(self) -> None:
        p._line = None
        self.assertEqual(p._line_contents(''), None)

    def test_spaces(self) -> None:
        p._line = '    aaa'
        self.assertEqual(p._line_contents(''), '    aaa')
        self.assertEqual(p._line_contents(' '), '   aaa')
        self.assertEqual(p._line_contents('  '), '  aaa')
        self.assertEqual(p._line_contents('   '), ' aaa')
        self.assertEqual(p._line_contents('    '), 'aaa')
        self.assertEqual(p._line_contents('     '), None)

    def test_tab_0(self) -> None:
        p._line = '\taaa'
        self.assertEqual(p._line_contents(''), '\taaa')
        self.assertEqual(p._line_contents(' '), '   aaa')
        self.assertEqual(p._line_contents('  '), '  aaa')
        self.assertEqual(p._line_contents('   '), ' aaa')
        self.assertEqual(p._line_contents('    '), 'aaa')
        self.assertEqual(p._line_contents('     '), None)

    def test_tab_1(self) -> None:
        p._line = ' \taaa'
        self.assertEqual(p._line_contents(''), ' \taaa')
        self.assertEqual(p._line_contents(' '), '   aaa')
        self.assertEqual(p._line_contents('  '), '  aaa')
        self.assertEqual(p._line_contents('   '), ' aaa')
        self.assertEqual(p._line_contents('    '), 'aaa')
        self.assertEqual(p._line_contents('     '), None)

    def test_tab_2(self) -> None:
        p._line = '  \taaa'
        self.assertEqual(p._line_contents(''), '  \taaa')
        self.assertEqual(p._line_contents(' '), '   aaa')
        self.assertEqual(p._line_contents('  '), '  aaa')
        self.assertEqual(p._line_contents('   '), ' aaa')
        self.assertEqual(p._line_contents('    '), 'aaa')
        self.assertEqual(p._line_contents('     '), None)

    def test_tab_3(self) -> None:
        p._line = '   \taaa'
        self.assertEqual(p._line_contents(''), '   \taaa')
        self.assertEqual(p._line_contents(' '), '   aaa')
        self.assertEqual(p._line_contents('  '), '  aaa')
        self.assertEqual(p._line_contents('   '), ' aaa')
        self.assertEqual(p._line_contents('    '), 'aaa')
        self.assertEqual(p._line_contents('     '), None)

    def test_tab_4(self) -> None:
        p._line = '    \taaa'
        self.assertEqual(p._line_contents(''), '    \taaa')
        self.assertEqual(p._line_contents(' '), '   \taaa')
        self.assertEqual(p._line_contents('  '), '  \taaa')
        self.assertEqual(p._line_contents('   '), ' \taaa')
        self.assertEqual(p._line_contents('    '), '\taaa')
        self.assertEqual(p._line_contents('     '), '   aaa')
        self.assertEqual(p._line_contents('      '), '  aaa')
        self.assertEqual(p._line_contents('       '), ' aaa')
        self.assertEqual(p._line_contents('        '), 'aaa')
        self.assertEqual(p._line_contents('         '), None)

    def test_block_quote(self) -> None:
        p._line = '> aaa'
        self.assertEqual(p._line_contents(''), '> aaa')
        self.assertEqual(p._line_contents('>'), 'aaa')
        self.assertEqual(p._line_contents('>>'), None)
        self.assertEqual(p._line_contents(' '), None)

    def test_block_quote_without_spaces(self) -> None:
        p._line = '>aaa'
        self.assertEqual(p._line_contents(''), '>aaa')
        self.assertEqual(p._line_contents('>'), 'aaa')

    def test_block_quote_with_spaces(self) -> None:
        p._line = '   >    aaa'
        self.assertEqual(p._line_contents(''), '   >    aaa')
        self.assertEqual(p._line_contents('>'), '   aaa')

    def test_block_quote_with_tab_0(self) -> None:
        p._line = '>\taaa'
        self.assertEqual(p._line_contents(''), '>\taaa')
        self.assertEqual(p._line_contents('>'), '  aaa')
        self.assertEqual(p._line_contents('>    '), None)

    def test_block_quote_with_tab_1(self) -> None:
        p._line = '> \taaa'
        self.assertEqual(p._line_contents(''), '> \taaa')
        self.assertEqual(p._line_contents('>'), '  aaa')
        self.assertEqual(p._line_contents('>    '), None)

    def test_block_quote_with_tab_2(self) -> None:
        p._line = '>  \taaa'
        self.assertEqual(p._line_contents(''), '>  \taaa')
        self.assertEqual(p._line_contents('>'), '  aaa')
        self.assertEqual(p._line_contents('>    '), None)

    def test_block_quote_with_tab_3(self) -> None:
        p._line = '>   \taaa'
        self.assertEqual(p._line_contents(''), '>   \taaa')
        self.assertEqual(p._line_contents('>'), '  \taaa')
        self.assertEqual(p._line_contents('>    '), '  aaa')

    def test_block_quote_with_tab_4(self) -> None:
        p._line = '>    \taaa'
        self.assertEqual(p._line_contents(''), '>    \taaa')
        self.assertEqual(p._line_contents('>'), '   \taaa')
        self.assertEqual(p._line_contents('>    '), '  aaa')

    def test_block_quote_nested_without_spaces(self) -> None:
        p._line = '>>>aaa'
        self.assertEqual(p._line_contents(''), '>>>aaa')
        self.assertEqual(p._line_contents('>'), '>>aaa')
        self.assertEqual(p._line_contents('>>'), '>aaa')
        self.assertEqual(p._line_contents('>>>'), 'aaa')

    def test_block_quote_nested_with_spaces(self) -> None:
        p._line = '>    >    >    aaa'
        self.assertEqual(p._line_contents(''), '>    >    >    aaa')
        self.assertEqual(p._line_contents('>'), '   >    >    aaa')
        self.assertEqual(p._line_contents('>>'), '   >    aaa')
        self.assertEqual(p._line_contents('>>>'), '   aaa')

    def test_block_quote_and_spaces(self) -> None:
        p._line = '>    aaa'
        self.assertEqual(p._line_contents(''), '>    aaa')
        self.assertEqual(p._line_contents('>'), '   aaa')
        self.assertEqual(p._line_contents('> '), '  aaa')
        self.assertEqual(p._line_contents('>  '), ' aaa')
        self.assertEqual(p._line_contents('>   '), 'aaa')
        self.assertEqual(p._line_contents('>    '), None)

    def test_block_quote_spaces_and_tab(self) -> None:
        p._line = '> >\taaa'
        self.assertEqual(p._line_contents(''), '> >\taaa')
        self.assertEqual(p._line_contents('>'), '> aaa')
        self.assertEqual(p._line_contents('>>'), 'aaa')
        self.assertEqual(p._line_contents('>> '), None)

    def test_block_quote_empty(self) -> None:
        p._line = '>'
        self.assertEqual(p._line_contents(''), '>')
        self.assertEqual(p._line_contents('>'), '')
        self.assertEqual(p._line_contents('> '), '')
        self.assertEqual(p._line_contents('>    '), '')
        self.assertEqual(p._line_contents('>    >'), None)
        self.assertEqual(p._line_contents(' '), None)

    def test_empty_line(self) -> None:
        p._line = ''
        self.assertEqual(p._line_contents(''), '')
        self.assertEqual(p._line_contents('    '), '')
        self.assertEqual(p._line_contents('>'), None)


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.logger.addHandler(self.handler)
        super().setUp()

    def tearDown(self) -> None:
        self.logger.removeHandler(self.handler)
        self.handler.close()
        super().tearDown()

    def _debug_info(self) -> str:
        self.handler.flush()
        logs = self.stream.getvalue()
        if logs:
            return (
                '\n\n'
                f"{'~' * 25} logs {'~' * 25}\n"
                + logs.strip())
        return ''

    def assertEqual(self, first: Any, second: Any, msg: str = '') -> None:
        return super().assertEqual(first, second, msg + self._debug_info())

    # def debug_info(self, stdout: StringIO, stderr: StringIO) -> str:
        # stdout_str = stdout.getvalue().strip()
        # stderr_str = stderr.getvalue().strip()
        # info = ''
        # if stdout_str:
        #     info += '\n\n'
        #     info += f"{'-' * 25} stdout {'-' * 25}\n"
        #     info += stdout_str
        # if stderr_str:
        #     info += '\n\n'
        #     info += f"{'-' * 25} stderr {'-' * 25}\n"
        #     info += stderr_str
        # return info

#===--- Header ---===#
# ATX headings
#   https://github.github.com/gfm/#atx-headings
# Setext headings
#   https://github.github.com/gfm/#setext-headings

#===--- HtmlBlock ---===#
# HTML blocks
#   https://github.github.com/gfm/#html-blocks

#===--- Table (extension) ---===#
#   https://github.github.com/gfm/#tables-extension-

#===--- BlockQuote ---===#
#   https://github.github.com/gfm/#block-quotes

#===--- BulletList ---===#
# https://github.github.com/gfm/#lists
# https://github.github.com/gfm/#list-items
# def test_parse_bullet_list_one_item(self) -> None:
#     lines = ['- A']
#     self.assertEqual(p._parse_blocks(lines), [
#         BulletList([_Paragraph('A')])
#     ])

# list item vs code block: list item
# -    one
#
#     two

# list item vs divider: divider
# * List 1
# * * *
# * List 2

# - List 1
# - * * *
# - List 1

#===--- OrderedList ---===#
# https://github.github.com/gfm/#lists
# https://github.github.com/gfm/#list-items

#===--- TaskList ---===#
# https://github.github.com/gfm/#lists
# https://github.github.com/gfm/#list-items
# https://github.github.com/gfm/#task-list-items-extension-

#===--- Block ---===#

# Backslash escapes
#   https://github.github.com/gfm/#backslash-escapes
# Entity and numeric character references
#   https://github.github.com/gfm/#entity-and-numeric-character-references
# Code spans
#   https://github.github.com/gfm/#code-spans
# Emphasis and strong emphasis
#   https://github.github.com/gfm/#emphasis-and-strong-emphasis
# Strikethrough (extension)
#   https://github.github.com/gfm/#strikethrough-extension-
# Links
#   https://github.github.com/gfm/#links
# Link reference definitions
#   https://github.github.com/gfm/#link-reference-definitions
# Images
#   https://github.github.com/gfm/#images
# Autolinks
#   https://github.github.com/gfm/#autolinks
# Autolinks (extension)
#   https://github.github.com/gfm/#autolinks-extension-
# Raw HTML
#   https://github.github.com/gfm/#raw-html
# Disallowed raw HTML (extension)
#   https://github.github.com/gfm/#disallowed-raw-html-extension-
# Textual context
#   https://github.github.com/gfm/#textual-content

#===--- Integration tests ---===#


class ParserIntegrationTest(unittest.TestCase):
    def test_parse_empty(self) -> None:
        self.assertEqual(p.parse_lines([]), Document())

    # def test_paragraph(self) -> None:
    #     lines = ['aaa']
    #     self.assertEqual(p.parse_lines(lines), Document([
    #         Paragraph(['aaa']),
    #     ]))

    def test_code_block_fenced_inbetween_dividers(self) -> None:
        lines = ['---', '```', 'aaa', '```', '---']
        self.assertEqual(p.parse_lines(lines), Document([
            Divider(),
            CodeBlock('aaa'),
            Divider(),
        ]))

    # def test_code_block_fenced_inbetween_headers(self) -> None:
    #     lines = ['aaa', '---', '~~~', 'bbb', '~~~', '# ccc']
    #     self.assertEqual(p.parse_lines(lines), Document([
    #         Header('aaa', level=2),
    #         CodeBlock('bbb'),
    #         Header('ccc', level=1),
    #     ]))

#     def test_code_block_fenced_unclosed_in_blockquotes(self) -> None:
#         lines = ['> ```', '> aaa', '', 'bbb']
#         self.assertEqual(p.parse_lines(lines), Document([
#             BlockQuote([
#                 CodeBlock('aaa'),
#             ]),
#             Paragraph(['bbb'])
#         ]))

#     def test_code_block_fenced_unclosed_in_bullet_list(self) -> None:
#         lines = ['* ```', '  aaa', '', 'bbb']
#         self.assertEqual(p.parse_lines(lines), Document([
#             BulletList([
#                 CodeBlock('aaa'),
#             ]),
#             Paragraph(['bbb'])
#         ]))

#     def test_code_block_fenced_unclosed_in_ordered_list(self) -> None:
#         lines = ['1. ```', '   aaa', '', 'bbb']
#         self.assertEqual(p.parse_lines(lines), Document([
#             OrderedList([
#                 CodeBlock('aaa'),
#             ]),
#             Paragraph(['bbb'])
#         ]))

#     def test_bullet_list_within_block_quotes(self) -> None:
#         lines = [
#             '>> * aaa',
#             '>>',
#             '>>   bbb',
#         ]
#         self.assertEqual(p.parse_lines(lines), Document([
#             BlockQuote(BulletList([
#                 Paragraph(['aaa\nbbb']),
#             ])),
#         ]))
