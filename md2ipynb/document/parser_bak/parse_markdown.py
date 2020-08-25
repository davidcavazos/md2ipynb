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

from dataclasses import dataclass, field

# from . import parse

# from ..block import Block
# from ..element import Element

# from ..document import Document

# from ..code_block import CodeBlock
# from ..divider import Divider
# from ..header import Header
# from ..html_block import HtmlBlock
# from ..table import Table
# from ..paragraph import Paragraph

# from ..block_quote import BlockQuote
# from ..list_item import ListItem
# from ..bullet_list import BulletList
# from ..ordered_list import OrderedList
# from ..task_list import TaskList

# from ..comment import Comment
# from ..image import Image
# from ..link import Link
# from ..text import Text


# @dataclass
# class _Paragraph(Block):
#     content: str


# _indent_tab_re = re.compile(r'([ >]{,3})\t')
# _indent_block_quote_re = re.compile(r' {,3}>')
# # _indent_re = re.compile(r'    |\t| \t|  \t|   \t')

# _code_block_open_re = re.compile(r' {0,3}(?:(```+)([^`]*)|(~~~+)(.*))$')
# _code_block_close_re = re.compile(r' {0,3}(```+|~~~+)\s*$')

# # BlockQuote
# _block_quote_re = re.compile(r'^ {0,3}> ?(.*)$')

# # BulletList
# _bullet_list_re = re.compile(r'^( {0,3})([*+-])(?:[ \t](.*))?$')

# # CodeBlock (indented)
# _code_block_indent_re = re.compile(r'^(?:    | {0,3}\t)(.*)$')

# # CodeBlock (fenced)
# _code_block_backticks_re = re.compile(r'^ {0,3}(`{3,})([^`]*)$')
# _code_block_tildes_re = re.compile(r'^ {0,3}(~{3,})(.*)$')

# # Divider (horizontal rule)
# _divider_re = re.compile(r'^ {0,3}([-*_])[ \t]*\1[ \t]*\1(?:\1|[ \t])*$')

# # Header
# _header_re = re.compile(r'^ {0,3}(#{1,6})\s(.*?)#*$')
# _header_setext_re = re.compile(r'^ {0,3}(=+|-+)\s*$')

# _paragraph_trim_re = re.compile(r'([ \t])\s+')

# def parse_lines(
#     lines: Iterable[str],
#     source_name: str = '<source>',
#     block_extensions: Optional[Iterable[Parser.BlockParserType]] = None,
#     inline_extensions: Optional[Iterable[Parser.InlineParserType]] = None,
# ) -> Document:
#     return Document(Parser(block_extensions, inline_extensions).parse_blocks(
#         lines=lines,
#         source_name=source_name,
#     ))

# TODO: add parse_file
# TODO: add parse_text


# class Parser:
#     # These accept Parser as inputs, but Python doesn't allow to use the name
#     # Parser yet since the class hasn't finished declaring.
#     BlockParserType = Callable[[Any], Optional[Block]]
#     InlineParserType = Callable[[Any], Optional[Element]]

#     def __init__(
#         self,
#         block_extensions: Optional[Iterable[Parser.BlockParserType]] = None,
#         inline_extensions: Optional[Iterable[Parser.InlineParserType]] = None,
#     ) -> None:
#         self._reset([])
#         self._block_parsers: List[Parser.BlockParserType] = [
#             parse_block_quote,
#             parse_bullet_list,
#             parse_code_block_fenced,
#             parse_code_block_indented,
#             parse_divider,
#             *(block_extensions or []),
#         ]
#         self._inline_parsers: List[Parser.InlineParserType] = [
#             *(inline_extensions or []),
#         ]

#     def _reset(
#             self,
#             lines: Iterable[str],
#             source_name: str = '<source>',
#             row_idx: int = 0,
#     ) -> None:

#         self.paragraph: List[str] = []
#         self._lines = list(lines)
#         self._source_name = source_name
#         self._i = 0

#         self._row_idx = row_idx
#         self._debug_stack: List[str] = []

#     def parse_blocks(
#             self,
#             lines: Iterable[str],
#             source_name: str = '<source>',
#             row_idx: int = 0
#     ) -> Iterable[Block]:
#         self._reset(lines, source_name=source_name, row_idx=row_idx)
#         self._debug(f"===--- {repr(self.line())} ---===")
#         self._call(f"parse_blocks")
#         self.paragraph = []
#         line = self.line()
#         while line is not None:
#             if not line.strip():
#                 if self.paragraph:
#                     paragraph = _Paragraph(self._paragraph_text(self.paragraph))
#                     self._debug(f"* yield (paragraph break) {paragraph}")
#                     yield paragraph
#                     self.paragraph = []
#                 line = self.next()
#                 continue

#             # Try to parse a block, this can interrupt a paragraph.
#             block = self._parse_block()
#             if block is not None:
#                 if self.paragraph:
#                     paragraph = _Paragraph(
#                         self._paragraph_text(self.paragraph))
#                     self._debug(
#                         f"* yield (paragraph interrupt) {paragraph}")
#                     yield paragraph
#                     self.paragraph = []
#                 self._debug(f"* yield (block) {block}")
#                 yield block
#                 line = self.line()
#                 continue

#             if not self.paragraph:
#                 self.paragraph.append(line)
#                 self._debug(f"Paragraph: start {repr(self.paragraph[-1])}")
#             elif line.endswith('  '):
#                 self.paragraph.append(line)
#                 self._debug(f"Paragraph: hard line break {repr(self.paragraph[-1])}")
#             else:
#                 self.paragraph[-1] += ' ' + line
#                 self._debug(f"Paragraph: soft line break {repr(self.paragraph[-1])}")
#             line = self.next()

#         if self.paragraph:
#             paragraph = _Paragraph(self._paragraph_text(self.paragraph))
#             self._debug(f"* yield (paragraph end) {paragraph}")
#             yield paragraph

#     def _parse_block(self) -> Optional[Block]:
#         for block_parser in self._block_parsers:
#             block = block_parser(self)
#             if block:
#                 return block
#         return None

#     @staticmethod
#     def _paragraph_text(lines: List[str]) -> str:
#         lines = [_paragraph_trim_re.sub(r'\1', line.strip()) for line in lines]
#         return '\n'.join(lines)

#     def line(self, lookahead: int = 0) -> Optional[str]:
#         i = self._i + lookahead
#         return self._lines[i] if i < len(self._lines) else None

#     def next(self) -> Optional[str]:
#         self._i += 1
#         self._row_idx += 1
#         self._debug(f"===--- {repr(self.line())} ---===")
#         return self.line()

#     # Debugging helper methods.
#     def _call(self, function_name: str, args: Optional[Dict[str, Any]] = None) -> None:
#         args = args or {}
#         indent = '  ' * len(self._debug_stack)
#         message = ', '.join(
#             f"{name}={repr(value)}" for name, value in args.items())
#         logging.debug(f"{indent}{function_name}:{self._row_idx}: {message}")
#         self._debug_stack.append(function_name)

#     def _return(self, return_value: Any = None) -> Any:
#         if return_value is not None:
#             self._debug(f"return {repr(return_value)}")
#         self._debug_stack.pop()
#         return return_value

#     def _debug(self, message: Any) -> None:
#         indent = '  ' * len(self._debug_stack)
#         logging.debug(f"{indent}> {message}")


# def parse_block_quote(p: Parser) -> Optional[BlockQuote]:
#     # Check if it matches.
#     line = p.line()
#     if line is None:
#         return None
#     m = _block_quote_re.match(line)
#     if not m:
#         return None

#     # Match started.
#     p._call("BlockQuote")
#     lines: List[str] = [m[1]]
#     p._debug(f"start {repr(lines[-1])}")
#     line = p.next()
#     while line is not None:
#         m = _block_quote_re.match(line)
#         if m:
#             lines.append(m[1])
#             p._debug(f"append {repr(lines[-1])}")
#         else:
#             p._debug(f"break")
#             break
#         line = p.next()

#     p._debug(f"{'~' * 20} BlockQuote start {'~' * 20}")
#     p._debug(f"  lines={lines}")
#     logging.debug('')
#     blocks = list(Parser().parse_blocks(lines, p._source_name, p._row_idx))
#     logging.debug('')
#     p._debug(f"{'~' * 20} BlockQuote end {'~' * 20}")
#     return p._return(BlockQuote(blocks))


# def parse_bullet_list(p: Parser) -> Optional[BulletList]:
#     # Check if it matches.
#     line = p.line()
#     if line is None:
#         return None
#     m = _bullet_list_re.match(line)
#     if not m:
#         return None

#     # Match started.
#     p._call("BulletList")
#     indent = m[1]
#     marker = m[2]
#     p._debug(f"indent={repr(indent)}, marker={repr(marker)}")
#     lines: List[str] = [m[3]]
#     p._debug(f"start {repr(lines[-1])}")
#     line = p.next()
#     while line is not None:
#         print('\n\nTODO: parse list items')
#         print('mypy md2ipynb/document/**/*.py && python setup.py test -v -s md2ipynb.document.parser.parser_bullet_list_test')
#         input()
#         m = _bullet_list_re.match(line)
#         if m:
#             lines.append(m[1])
#             p._debug(f"append {repr(lines[-1])}")
#         else:
#             p._debug(f"break")
#             break
#         line = p.next()

#     p._debug(f"{'~' * 20} BulletList start {'~' * 20}")
#     p._debug(f"  lines={lines}")
#     logging.debug('')
#     items: List[ListItem] = []
#     # blocks = list(Parser().parse_blocks(lines, p._source_name, p._row_idx))
#     logging.debug('')
#     p._debug(f"{'~' * 20} BulletList end {'~' * 20}")
#     return p._return(BulletList(items))


# def parse_code_block_fenced(p: Parser) -> Optional[Block]:
#     # Check if it matches.
#     line = p.line()
#     if line is None:
#         return None
#     m = _code_block_backticks_re.match(line)
#     if not m:
#         m = _code_block_tildes_re.match(line)
#     if not m:
#         return None

#     # Match started.
#     p._call("FencedCodeBlock")
#     delimiter = m[1]
#     info_string = m[2].strip()
#     language = (info_string.split() or [''])[0]
#     p._debug(f"start {repr(delimiter)} lang={repr(language)}")

#     lines: List[str] = []
#     line = p.next()
#     while line is not None:
#         trimmed_line = line.strip()
#         if len(delimiter) <= len(trimmed_line) and \
#                 trimmed_line == delimiter[0] * len(trimmed_line):
#             p._debug("end")
#             p.next()
#             break
#         lines.append(line)
#         p._debug(f"append {repr(lines[-1])}")
#         line = p.next()

#     return p._return(CodeBlock('\n'.join(lines), language))


# def parse_code_block_indented(p: Parser) -> Optional[Block]:
#     # Check if it matches.
#     line = p.line()
#     if line is None or not line.strip():
#         return None
#     m = _code_block_indent_re.match(line)
#     if not m:
#         return None
#     if p.paragraph:
#         # Indented code blocks cannot interrupt paragraphs.
#         return None

#     # Match started.
#     p._call("IndentedCodeBlock")
#     lines: List[str] = [m[1]]
#     p._debug(f"start {repr(lines[-1])}")
#     line = p.next()
#     while line is not None:
#         m = _code_block_indent_re.match(line)
#         if m:
#             lines.append(m[1])
#             p._debug(f"append {repr(lines[-1])}")
#         elif not line.strip():
#             lines.append('')
#             p._debug(f"empty line {repr(lines[-1])}")
#         else:
#             p._debug(f"break")
#             break
#         line = p.next()

#     while lines[-1].strip() == '':
#         line = lines.pop()
#         p._debug(f"pop {repr(line)}")

#     return p._return(CodeBlock('\n'.join(lines)))


# def parse_divider(p: Parser) -> Optional[Divider]:
#     # Check if it matches.
#     line = p.line()
#     if line is None:
#         return None
#     m = _divider_re.match(line)
#     if not m:
#         return None

#     # Match started.
#     p.next()
#     return Divider()
