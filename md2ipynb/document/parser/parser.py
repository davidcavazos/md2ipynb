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

import logging
import math
import re

from dataclasses import dataclass, field
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from ..block import Block
from ..element import Element

from ..document import Document

from ..code_block import CodeBlock
from ..divider import Divider
# from ..header import Header
# from ..html_block import HtmlBlock
# from ..table import Table
from ..paragraph import Paragraph

from ..block_quote import BlockQuote
# from ..bullet_list import BulletList
# from ..ordered_list import OrderedList
# from ..task_list import TaskList

# from ..comment import Comment
# from ..image import Image
# from ..link import Link
from ..text import Text

_indent_tab_re = re.compile(r'([ >]{,3})\t')
_indent_block_quote_re = re.compile(r' {,3}>')
# _indent_re = re.compile(r'    |\t| \t|  \t|   \t')

_code_block_open_re = re.compile(r' {0,3}(?:(```+)([^`]*)|(~~~+)(.*))$')
_code_block_close_re = re.compile(r' {0,3}(```+|~~~+)\s*$')


@dataclass
class _Paragraph(Block):
    content: str


class Parser:
    def __init__(self) -> None:
        self.reset([])

    def reset(self, lines: Iterable[str], source_name: str = '<source>') -> None:
        def with_lookahead(elements: Iterable[str]) -> Iterable[Tuple[Optional[str], Optional[str]]]:
            iterable = iter(elements)
            previous = current = next(iterable, None)
            while current is not None:
                current = next(iterable, None)
                yield previous, current
                previous = current
            yield None, None

        self._lines = iter(with_lookahead(lines))
        self._source_name = source_name
        self._row = 0
        self._line: Optional[str] = None
        self._next_line: Optional[str] = None

        self._debug_stack: List[str] = []
        _, _ = self._next()

    def parse(self, filename: str) -> Document:
        self._call('parse', {'filename': filename})
        with open(filename) as f:
            return self._return(self.parse_lines(f, filename))

    def parse_string(self, source: str, source_name: str = '<source>') -> Document:
        self._call('parse_string', {
            'source': source, 'source_name': source_name})
        return self._return(self.parse_lines(source.splitlines(), source_name))

    def parse_lines(self, lines: Iterable[str], source_name: str = '<source>') -> Document:
        self._call('parse_lines', {
            'lines': lines, 'source_name': source_name})
        self.reset(lines, source_name)
        return self._return(Document(self._parse_blocks()))

    def _parse_blocks(self, indents: str = '') -> Iterable[Block]:
        self._call('parse_blocks', {'indents': indents})
        lines: List[str] = []
        line = self._line_contents(indents)
        while line is not None:
            line_trimmed = line.strip()
            if line_trimmed == '':
                if lines:
                    p = _Paragraph('\n'.join(lines))
                    self._debug(f"* yield {p} (paragraph break)")
                    yield p
                    lines = []
                else:
                    self._debug(f"skipping empty line: {repr(self._line)}")
                line, _ = self._next(indents)
                continue

            block: Optional[Block] = None
            if not lines:
                # CANNOT interrupt paragraphs.
                block = self._parse_code_block_indented(indents + '    ')
            if not block:
                # CAN interrupt paragraphs.
                block = (
                    self._parse_code_block_fenced(indents, line)
                )

            if block:
                if lines:
                    p = _Paragraph('\n'.join(lines))
                    self._debug(f"* yield {p} (paragraph interrupt)")
                    yield p
                    lines = []
                self._debug(f"* yield {block}")
                yield block
            elif not lines:
                lines.append(line_trimmed)
                self._debug(f"paragraph start: {repr(lines[-1])}")
            elif line.endswith('  '):
                lines.append(line_trimmed)
                self._debug(f"hard line break: {repr(lines[-1])}")
            else:
                lines[-1] += ' ' + line_trimmed
                self._debug(f"soft line break: {repr(lines[-1])}")
            line, _ = self._next(indents)

        if lines:
            p = _Paragraph('\n'.join(lines))
            self._debug(f"* yield {p} (end of block)")
            yield p
            lines = []
        self._return()

    def _parse_code_block_indented(self, indents: str) -> Optional[CodeBlock]:
        line = self._line_contents(indents)
        if line is None or line.strip() == '':
            return None

        self._call('parse_code_block_indented', {'indents': indents})
        self._debug(f"start: {repr(line)}")
        lines: List[str] = [line]
        next_line = self._line_contents(indents, self._next_line)
        while next_line is not None:
            line, next_line = self._next(indents)
            if line is not None:
                self._debug(f"append: {repr(line)}")
                lines.append(line)

        while lines[-1].strip() == '':
            line = lines.pop()
            self._debug(f"pop: {repr(line)}")
        return self._return(CodeBlock('\n'.join(lines)))

    def _parse_code_block_fenced(self, indents: str, first_line: str) -> Optional[CodeBlock]:
        m = _code_block_open_re.match(first_line)
        if m is None:
            return None

        self._call('parse_code_block_fenced', {
                   'indents': indents, 'first_line': first_line})
        delim1, info_str1, delim2, info_str2 = m.groups()
        open_delim, info_str = (delim1, info_str1) \
            if delim1 is not None else (delim2, info_str2)
        language = (info_str.split() or [''])[0]
        self._debug(
            f"open_delim={repr(open_delim)}, language={repr(language)}")

        lines: List[str] = []
        line, _ = self._next(indents)
        while line is not None:
            m = _code_block_close_re.match(line)
            if m is not None and m[1].startswith(open_delim):
                self._debug(f"close: {repr(line)}")
                break
            self._debug(f"append: {repr(line)}")
            lines.append(line)
            line, _ = self._next(indents)

        return self._return(CodeBlock('\n'.join(lines), language))

    def _line_contents(self, indents: str, line: Optional[str] = None) -> Optional[str]:
        line = line or self._line
        if line is None:
            return None

        i = 0
        while line and indents:
            # Try to expand any tabs into spaces.
            if i % 4 == 0:
                m = _indent_tab_re.match(line)
                if m:
                    line = line.replace(m[0], m[1] + ' ' * (4 - len(m[1])), 1)

            # Remove 0 to 3 leading spaces from block quotes.
            m = _indent_block_quote_re.match(line)
            if m:
                line = line.replace(m[0], '>', 1)

            # Break at the first mismatch.
            if line[0] != indents[0]:
                return None

            # Advance on the line inputs and the indents inputs.
            line = line[1:]
            if indents[0] == '>' and line and line[0] == ' ':
                line = line[1:]
                i += 1
            indents = indents[1:]
            i += 1

        # Blank lines may not represent an indentation level close.
        if line.strip() == '' and indents.strip() == '':
            return line

        # If there are indents left, the indentation level is over.
        if indents:
            return None
        return line

    def _next(self, indents: str = '') -> Tuple[Optional[str], Optional[str]]:
        self._row += 1
        self._line, self._next_line = next(self._lines, (None, None))
        line = self._line_contents(indents, self._line)
        next_line = self._line_contents(indents, self._next_line)
        self._debug(f"next_line: {repr(line)}, raw={repr(self._line)}, next={repr(next_line)}")
        return line, next_line

    # Debugging helper methods.
    def _call(self, function_name: str, args: Optional[Dict[str, Any]] = None) -> None:
        args = args or {}
        indent = '  ' * len(self._debug_stack)
        message = ', '.join(
            f"{name}={repr(value)}" for name, value in args.items())
        logging.debug(f"{indent}{function_name}:{self._row}: {message}")
        self._debug_stack.append(function_name)

    def _return(self, return_value: Any = None) -> Any:
        if return_value is not None:
            self._debug(f"return {repr(return_value)}")
        self._debug_stack.pop()
        return return_value

    def _debug(self, message: Any) -> None:
        indent = '  ' * len(self._debug_stack)
        logging.debug(f"{indent}> {message}")
