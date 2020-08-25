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

from __future__ import annotations

# import unittest
# from typing import *

# from . import markdown_parser as md

# from .block import Block
# from .block_quote import BlockQuote
# from .code_block import CodeBlock
# from .document import Document
# from .markdown_parser import _Paragraph


# class MarkdownParserTest(unittest.TestCase):
#     def test_raw_line(self) -> None:
#         parse = md.raw_line().parse
#         self.assertEqual(parse(''), None)
#         self.assertEqual(parse('   '), ('   ', ''))
#         self.assertEqual(parse('   \n  '), ('   ', '  '))
#         self.assertEqual(parse('a'), ('a', ''))
#         self.assertEqual(parse('aaa'), ('aaa', ''))
#         self.assertEqual(parse('a\nb'), ('a', 'b'))
#         self.assertEqual(parse('a\n\nb'), ('a', '\nb'))
#         self.assertEqual(parse('\na'), ('', 'a'))
#         self.assertEqual(parse(' a'), (' a', ''))
#         self.assertEqual(parse('  a'), ('  a', ''))
#         self.assertEqual(parse('   a'), ('   a', ''))
#         self.assertEqual(parse('    a'), ('    a', ''))

#     def test_blank_line(self) -> None:
#         parse = md.blank_line().parse
#         self.assertEqual(parse(''), None)
#         self.assertEqual(parse('   '), ('   ', ''))
#         self.assertEqual(parse('   \n  '), ('   ', '  '))
#         self.assertEqual(parse('a'), None)
#         self.assertEqual(parse('aaa'), None)
#         self.assertEqual(parse('a\nb'), None)
#         self.assertEqual(parse('a\n\nb'), None)
#         self.assertEqual(parse('\na'), ('', 'a'))
#         self.assertEqual(parse(' a'), None)
#         self.assertEqual(parse('  a'), None)
#         self.assertEqual(parse('   a'), None)
#         self.assertEqual(parse('    a'), None)

#     def test_non_blank_line(self) -> None:
#         parse = md.non_blank_line().parse
#         self.assertEqual(parse(''), None)
#         self.assertEqual(parse('   '), None)
#         self.assertEqual(parse('   \n  '), None)
#         self.assertEqual(parse('a'), ('a', ''))
#         self.assertEqual(parse('aaa'), ('aaa', ''))
#         self.assertEqual(parse('a\nb'), ('a', 'b'))
#         self.assertEqual(parse('a\n\nb'), ('a', '\nb'))
#         self.assertEqual(parse('\na'), None)
#         self.assertEqual(parse(' a'), (' a', ''))
#         self.assertEqual(parse('  a'), ('  a', ''))
#         self.assertEqual(parse('   a'), ('   a', ''))
#         self.assertEqual(parse('    a'), ('    a', ''))

#     def test_text_line(self) -> None:
#         parse = md.text_line().parse
#         self.assertEqual(parse(''), None)
#         self.assertEqual(parse('   '), None)
#         self.assertEqual(parse('   \n  '), ('', '  '))
#         self.assertEqual(parse('a'), ('a', ''))
#         self.assertEqual(parse('aaa'), ('aaa', ''))
#         self.assertEqual(parse('a\nb'), ('a', 'b'))
#         self.assertEqual(parse('a\n\nb'), ('a', '\nb'))
#         self.assertEqual(parse('\na'), ('', 'a'))
#         self.assertEqual(parse(' a'), ('a', ''))
#         self.assertEqual(parse('  a'), ('a', ''))
#         self.assertEqual(parse('   a'), ('a', ''))
#         self.assertEqual(parse('    a'), (' a', ''))

#     def test_paragraph(self) -> None:
#         parse = md.paragraph().parse
#         self.assertEqual(parse('a'), (_Paragraph(['a']), ''))
#         self.assertEqual(parse('a\nb'), (_Paragraph(['a', 'b']), ''))
#         self.assertEqual(parse('a\nb\nc'), (_Paragraph(['a', 'b', 'c']), ''))
#         self.assertEqual(parse('a\n\n_'), (_Paragraph(['a']), '\n_'))
#         self.assertEqual(parse(' a \n \n_'), (_Paragraph([' a ']), ' \n_'))
#         self.assertEqual(parse('\na'), None)

#     def test_indented_code_block(self) -> None:
#         parse = md.indented_code_block().parse
#         self.assertEqual(parse(''), None)
#         self.assertEqual(parse('    '), None)
#         self.assertEqual(parse('    \n\n'), None)
#         self.assertEqual(parse('    a\n_'), (CodeBlock('a'), '_'))
#         self.assertEqual(parse('   \ta\n_'), (CodeBlock('a'), '_'))
#         self.assertEqual(parse('  \ta\n_'), (CodeBlock('a'), '_'))
#         self.assertEqual(parse(' \ta\n_'), (CodeBlock('a'), '_'))
#         self.assertEqual(parse('\ta\n_'), (CodeBlock('a'), '_'))
#         self.assertEqual(parse('a'), None)
#         self.assertEqual(
#             parse('\ta\n     b\n  \t  c\n   _'),
#             (CodeBlock('a\n b\n  c'), '   _'))
#         self.assertEqual(
#             parse('    a\n\n    b\n \n   \n    c'),
#             (CodeBlock('a\n\nb\n\n\nc'), ''))
#         self.assertEqual(
#             parse('    a\n\n    b\n \n   \n    c'),
#             (CodeBlock('a\n\nb\n\n\nc'), ''))

#     def test_fenced_code_block(self) -> None:
#         parse = md.fenced_code_block().parse

#         # Opening a code block.
#         self.assertEqual(parse(''), None)
#         self.assertEqual(parse('``'), None)
#         self.assertEqual(parse('~~'), None)
#         self.assertEqual(parse('``~'), None)
#         self.assertEqual(parse('~~`'), None)
#         self.assertEqual(parse('```'), (CodeBlock(''), ''))
#         self.assertEqual(parse('~~~'), (CodeBlock(''), ''))
#         self.assertEqual(parse('```\n'), (CodeBlock(''), ''))
#         self.assertEqual(parse('~~~\n'), (CodeBlock(''), ''))
#         self.assertEqual(parse('```\na'), (CodeBlock('a'), ''))
#         self.assertEqual(parse('~~~\na'), (CodeBlock('a'), ''))
#         self.assertEqual(parse('```\nabc'), (CodeBlock('abc'), ''))
#         self.assertEqual(parse('~~~\nabc'), (CodeBlock('abc'), ''))
#         self.assertEqual(parse('```\na\nb\nc'), (CodeBlock('a\nb\nc'), ''))
#         self.assertEqual(parse('~~~\na\nb\nc'), (CodeBlock('a\nb\nc'), ''))

#         # Closing a code block.
#         self.assertEqual(parse('```\n```'), (CodeBlock(''), ''))
#         self.assertEqual(parse('~~~\n~~~'), (CodeBlock(''), ''))
#         self.assertEqual(parse('```\n```a'), (CodeBlock('```a'), ''))
#         self.assertEqual(parse('~~~\n~~~a'), (CodeBlock('~~~a'), ''))
#         self.assertEqual(parse('```\n```\na'), (CodeBlock(''), 'a'))
#         self.assertEqual(parse('~~~\n~~~\na'), (CodeBlock(''), 'a'))
#         self.assertEqual(parse('```\n~~~\na'), (CodeBlock('~~~\na'), ''))
#         self.assertEqual(parse('~~~\n```\na'), (CodeBlock('```\na'), ''))
#         self.assertEqual(parse('```\n``` \na'), (CodeBlock(''), 'a'))
#         self.assertEqual(parse('~~~\n~~~ \na'), (CodeBlock(''), 'a'))
#         self.assertEqual(parse('```\n ```\na'), (CodeBlock(' ```\na'), ''))
#         self.assertEqual(parse('~~~\n ~~~\na'), (CodeBlock(' ~~~\na'), ''))
#         self.assertEqual(parse('```\n``````\na'), (CodeBlock(''), 'a'))
#         self.assertEqual(parse('~~~\n~~~~~~\na'), (CodeBlock(''), 'a'))
#         self.assertEqual(parse('``````\n```\na'), (CodeBlock('```\na'), ''))
#         self.assertEqual(parse('~~~~~~\n~~~\na'), (CodeBlock('~~~\na'), ''))
#         self.assertEqual(parse('``````\n``````\na'), (CodeBlock(''), 'a'))
#         self.assertEqual(parse('~~~~~~\n~~~~~~\na'), (CodeBlock(''), 'a'))

#         # Code block contents.
#         self.assertEqual(parse('```\n\n```'), (CodeBlock(''), ''))
#         self.assertEqual(parse('~~~\n\n~~~'), (CodeBlock(''), ''))
#         self.assertEqual(parse('```\n \n```'), (CodeBlock(' '), ''))
#         self.assertEqual(parse('~~~\n \n~~~'), (CodeBlock(' '), ''))
#         self.assertEqual(parse('```\n\n\n```'), (CodeBlock('\n'), ''))
#         self.assertEqual(parse('~~~\n\n\n~~~'), (CodeBlock('\n'), ''))
#         self.assertEqual(parse('```\na\n```'), (CodeBlock('a'), ''))
#         self.assertEqual(parse('~~~\na\n~~~'), (CodeBlock('a'), ''))
#         self.assertEqual(parse('```\nabc\n```'), (CodeBlock('abc'), ''))
#         self.assertEqual(parse('~~~\nabc\n~~~'), (CodeBlock('abc'), ''))
#         self.assertEqual(parse('```\na\nb\nc\n```'), (CodeBlock('a\nb\nc'), ''))
#         self.assertEqual(parse('~~~\na\nb\nc\n~~~'), (CodeBlock('a\nb\nc'), ''))

#         # Info string.
#         self.assertEqual(parse('```a`'), None)
#         self.assertEqual(parse('~~~a~'), (CodeBlock('', 'a~'), ''))
#         self.assertEqual(parse('```a'), (CodeBlock('', 'a'), ''))
#         self.assertEqual(parse('~~~a'), (CodeBlock('', 'a'), ''))
#         self.assertEqual(parse('```a\nx'), (CodeBlock('x', 'a'), ''))
#         self.assertEqual(parse('~~~a\nx'), (CodeBlock('x', 'a'), ''))
#         self.assertEqual(parse('```abc'), (CodeBlock('', 'abc'), ''))
#         self.assertEqual(parse('~~~abc'), (CodeBlock('', 'abc'), ''))
#         self.assertEqual(parse('```abc\nx'), (CodeBlock('x', 'abc'), ''))
#         self.assertEqual(parse('~~~abc\nx'), (CodeBlock('x', 'abc'), ''))
#         self.assertEqual(parse('``` a b c\nx'), (CodeBlock('x', 'a'), ''))
#         self.assertEqual(parse('~~~ a b c\nx'), (CodeBlock('x', 'a'), ''))

#         # Indent spacing.
#         # self.assertEqual(parse(' ```\n  a'), (CodeBlock(' a'), ''))
#         # self.assertEqual(parse('  ```\n   a'), (CodeBlock(' a'), ''))
#         # self.assertEqual(parse('   ```\n    a'), (CodeBlock(' a'), ''))

#     # def test_block_quote(self) -> None:
#     #     parse = md.block_quote().parse

#     #     # Opening a block quote.
#     #     self.assertEqual(parse(''), None)
#     #     self.assertEqual(parse('>'), (BlockQuote([]), ''))
#     #     self.assertEqual(parse('> '), (BlockQuote([]), ''))
#     #     self.assertEqual(parse('>  '), (BlockQuote([]), ''))
#     #     self.assertEqual(parse(' >'), None)

#     #     # Single line contents.
#     #     self.assertEqual(parse('>a'), (BlockQuote([_Paragraph(['a'])]), ''))
#     #     self.assertEqual(parse('>abc'), (BlockQuote([_Paragraph(['abc'])]), ''))
#     #     self.assertEqual(parse('> a'), (BlockQuote([_Paragraph(['a'])]), ''))
#     #     self.assertEqual(parse('> abc'), (BlockQuote([_Paragraph(['abc'])]), ''))
#     #     self.assertEqual(parse('>  a'), (BlockQuote([_Paragraph([' a'])]), ''))
#     #     self.assertEqual(parse('>  abc'), (BlockQuote([_Paragraph([' abc'])]), ''))

#     #     # Multi-line contents.
#     #     self.assertEqual(
#     #         parse('>a\n>b\n>c'),
#     #         (BlockQuote([_Paragraph(['a', 'b', 'c'])]), ''))
#     #     self.assertEqual(
#     #         parse('> a\n> b\n> c'),
#     #         (BlockQuote([_Paragraph(['a', 'b', 'c'])]), ''))
#     #     self.assertEqual(
#     #         parse('> a\n>b\n> c'),
#     #         (BlockQuote([_Paragraph(['a', 'b', 'c'])]), ''))

#     #     # Closing a block quote.
#     #     self.assertEqual(
#     #         parse('> a\n\n> b'),
#     #         (BlockQuote([_Paragraph(['a'])]), '\n> b'))

#     #     # Content blocks.
#     #     self.assertEqual(parse('>     a'), (BlockQuote([CodeBlock('a')]), ''))
#     #     self.assertEqual(parse('>```\n>a'), (BlockQuote([CodeBlock('a')]), ''))

#     #     # Followed by block quote.
#     #     self.assertEqual(
#     #         parse('>a\n> b'), (BlockQuote([_Paragraph(['a', 'b'])]), ''))
#     #     self.assertEqual(
#     #         parse('>a\n>b'), (BlockQuote([_Paragraph(['a', 'b'])]), ''))

#     #     # Followed by unordered list.
#     #     self.assertEqual(
#     #         parse('>a\n- b'), (BlockQuote([_Paragraph(['a'])]), '- b'))
#     #     self.assertEqual(
#     #         parse('>a\n+ b'), (BlockQuote([_Paragraph(['a'])]), '+ b'))
#     #     self.assertEqual(
#     #         parse('>a\n* b'), (BlockQuote([_Paragraph(['a'])]), '* b'))

#     #     # Followed by ordered list.
#     #     self.assertEqual(
#     #         parse('>a\n1. b'), (BlockQuote([_Paragraph(['a'])]), '1. b'))
#     #     self.assertEqual(
#     #         parse('>a\n1) b'), (BlockQuote([_Paragraph(['a'])]), '1) b'))

#     #     # Followed by divider.
#     #     self.assertEqual(
#     #         parse('>a\n***'), (BlockQuote([_Paragraph(['a'])]), '***'))
#     #     self.assertEqual(
#     #         parse('>a\n---'), (BlockQuote([_Paragraph(['a'])]), '---'))
#     #     self.assertEqual(
#     #         parse('>a\n___'), (BlockQuote([_Paragraph(['a'])]), '___'))

#     #     # Followed by header.
#     #     self.assertEqual(
#     #         parse('>a\n# b'), (BlockQuote([_Paragraph(['a'])]), '# b'))
#     #     self.assertEqual(
#     #         parse('>a\n## b'), (BlockQuote([_Paragraph(['a'])]), '## b'))
#     #     self.assertEqual(
#     #         parse('>a\n### b'), (BlockQuote([_Paragraph(['a'])]), '### b'))
#     #     self.assertEqual(
#     #         parse('>a\n#### b'), (BlockQuote([_Paragraph(['a'])]), '#### b'))
#     #     self.assertEqual(
#     #         parse('>a\n##### b'), (BlockQuote([_Paragraph(['a'])]), '##### b'))
#     #     self.assertEqual(
#     #         parse('>a\n###### b'), (BlockQuote([_Paragraph(['a'])]), '###### b'))
#     #     self.assertEqual(
#     #         parse('>a\nb\n='), (BlockQuote([_Paragraph(['a'])]), 'b\n='))
#     #     self.assertEqual(
#     #         parse('>a\nb\n-'), (BlockQuote([_Paragraph(['a'])]), 'b\n-'))

#     #     # Followed by code block.
#     #     self.assertEqual(
#     #         parse('>a\n    b'), (BlockQuote([_Paragraph(['a', 'b'])]), '    '))
#     #     self.assertEqual(
#     #         parse('>a\n```'), (BlockQuote([_Paragraph(['a'])]), '```'))
#     #     self.assertEqual(
#     #         parse('>a\n~~~'), (BlockQuote([_Paragraph(['a'])]), '~~~'))

#     #     # Followed by paragraph.
#     #     self.assertEqual(
#     #         parse('> a\nb\nc'),
#     #         (BlockQuote([_Paragraph(['a', 'b', 'c'])]), ''))

#     # def test_block(self) -> None:
#     #     parse = md.block().parse
#     #     self.assertEqual(parse(''), None)
#     #     self.assertEqual(parse('\n \n   \n'), None)
#     #     self.assertEqual(parse('    a'), (CodeBlock('a'), ''))
#     #     self.assertEqual(parse('```a\nb\n```'), (CodeBlock('b', 'a'), ''))
#     #     self.assertEqual(parse('a'), (_Paragraph(['a']), ''))
#     #     self.assertEqual(parse('\n\na\n\nb'), (_Paragraph(['a']), '\nb'))

#     # def test_document(self) -> None:
#     #     parse = md.document().parse
#     #     self.assertEqual(parse(''), (Document([]), ''))
#     #     self.assertEqual(
#     #         parse('a\nb\n\nc'),
#     #         (Document([_Paragraph(['a', 'b']), _Paragraph(['c'])]), ''))

#     # def test_parse(self) -> None:
#     #     self.assertEqual(md.parse(''), Document([]))
#     #     self.assertEqual(
#     #         md.parse('a\nb\n\nc'),
#     #         Document([_Paragraph(['a', 'b']), _Paragraph(['c'])]))
