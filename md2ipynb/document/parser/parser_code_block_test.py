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

from ..code_block import CodeBlock

from .parser import Parser
from .parser import _Paragraph
from .parser_test import ParserTestCase

p = Parser()


# https://github.github.com/gfm/#indented-code-blocks
class ParserCodeBlockIndentedTest(ParserTestCase):
    def test_one_line(self) -> None:
        p.reset(['    aaa'])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa'),
        ])

    def test_multiline(self) -> None:
        p.reset(['    aaa', '    bbb', '      ccc  '])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\nbbb\n  ccc  '),
        ])

    def test_keep_spaces(self) -> None:
        p.reset(['    aaa', '', '    ', '      ', '      bbb  '])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\n\n\n  \n  bbb  '),
        ])

    def test_tab_indents(self) -> None:
        p.reset(['\taaa', '\t\tbbb', '   \tccc', '    \tddd', '     \teee'])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\n\tbbb\nccc\n\tddd\n \teee'),
        ])

    def test_trim_empty_lines(self) -> None:
        p.reset(['', '    ', '        ', '    aaa', '        ', '    ', ''])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa'),
        ])

    def test_code_block_vs_divider(self) -> None:
        p.reset(['    ***'])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('***'),
        ])

    def test_close_block(self) -> None:
        p.reset(['    aaa', '   bbb', '    ccc', '', '    ddd'])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa'),
            _Paragraph('bbb ccc'),
            CodeBlock('ddd'),
        ])

    def test_negatives(self) -> None:
        p.reset([
            '   a   a   a', '',
            '   b    b        b', '',
            '   c\tc\tc',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            _Paragraph('a   a   a'),
            _Paragraph('b    b        b'),
            _Paragraph('c\tc\tc'),
        ])


# https://github.github.com/gfm/#fenced-code-blocks
class ParserCodeBlockFencedTest(ParserTestCase):
    def test_empty(self) -> None:
        p.reset([
            '```', '```',
            '~~~', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock(''),
            CodeBlock(''),
        ])

    def test_one_line(self) -> None:
        p.reset([
            '```', 'aaa', '```',
            '~~~', 'bbb', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa'),
            CodeBlock('bbb'),
        ])

    def test_multiline(self) -> None:
        p.reset([
            '```', 'aaa', 'bbb', 'ccc', '```',
            '~~~', 'ddd', 'eee', 'fff', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\nbbb\nccc'),
            CodeBlock('ddd\neee\nfff'),
        ])

    def test_leading_spaces(self) -> None:
        p.reset([
            ' ```', ' aaa', ' ```',
            '  ~~~', '  bbb', '  ~~~',
            '   ```', '   ccc', ' ```',
            ' ~~~', 'ddd', '   ~~~',
            '   ```', 'eee', ' ```',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock(' aaa'),
            CodeBlock('  bbb'),
            CodeBlock('   ccc'),
            CodeBlock('ddd'),
            CodeBlock('eee'),
        ])

    def test_keep_spaces(self) -> None:
        p.reset([
            '```', '', ' ', 'aaa', '', '  ', '\t', '  bbb  ', '```',
            '~~~', '', ' ', 'ccc', '', '  ', '\t', '  ddd  ', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('\n \naaa\n\n  \n\t\n  bbb  '),
            CodeBlock('\n \nccc\n\n  \n\t\n  ddd  '),
        ])

    def test_interrupt_paragraphs(self) -> None:
        p.reset([
            'aaa',
            '```', 'bbb', '```',
            'ccc',
            '~~~', 'ddd', '~~~',
            'eee',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            _Paragraph('aaa'),
            CodeBlock('bbb'),
            _Paragraph('ccc'),
            CodeBlock('ddd'),
            _Paragraph('eee'),
        ])

    def test_close(self) -> None:
        p.reset([
            '```', 'aaa', '~~~', '```',
            '~~~', 'bbb', '```', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\n~~~'),
            CodeBlock('bbb\n```'),
        ])

    def test_close_length(self) -> None:
        p.reset([
            '````', 'aaa', '```', '``````',
            '~~~~', 'bbb', '~~~', '~~~~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\n```'),
            CodeBlock('bbb\n~~~'),
        ])

    def test_unclosed_backticks(self) -> None:
        p.reset(['```', 'aaa', '', 'bbb'])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\n\nbbb'),
        ])

    def test_unclosed_tildes(self) -> None:
        p.reset(['~~~', 'aaa', '', 'bbb'])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('aaa\n\nbbb'),
        ])

    def test_info_string(self) -> None:
        p.reset([
            '```aaa', 'bbb', '```',
            '~~~ccc', 'ddd', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('bbb', language='aaa'),
            CodeBlock('ddd', language='ccc'),
        ])

    def test_info_string_strip(self) -> None:
        p.reset([
            '```    aaa    ', 'bbb', '```',
            '~~~    ccc    ', 'ddd', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('bbb', language='aaa'),
            CodeBlock('ddd', language='ccc'),
        ])

    def test_info_string_first_word(self) -> None:
        p.reset([
            '```  aaa  startline=1 $%@#$', 'bbb', '```',
            '~~~  ccc  startline=1 $%@#$', 'ddd', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('bbb', language='aaa'),
            CodeBlock('ddd', language='ccc'),
        ])

    def test_tilde_with_backticks_and_tildes(self) -> None:
        p.reset(['~~~ aaa ``` ~~~', 'bbb', '~~~'])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('bbb', language='aaa'),
        ])

    def test_info_string_close(self) -> None:
        p.reset([
            '``` aaa', 'bbb', '``` ccc', '```',
            '~~~ ddd', 'eee', '~~~ fff', '~~~',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            CodeBlock('bbb\n``` ccc', language='aaa'),
            CodeBlock('eee\n~~~ fff', language='ddd'),
        ])

    def test_fenced_negatives(self) -> None:
        p.reset([
            '``', 'aaa', '``', '',
            '~~', 'bbb', '~~', '',
            '```ccc`', '',
        ])
        self.assertEqual(list(p._parse_blocks()), [
            _Paragraph('`` aaa ``'),
            _Paragraph('~~ bbb ~~'),
            _Paragraph('```ccc`'),
        ])
