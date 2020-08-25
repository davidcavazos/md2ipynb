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

# from dataclasses import dataclass
# from typing import *

# from . import parser_monad as p
# from .parser_monad import Parser

# from .block import Block
# from .document import Document

# from .block_quote import BlockQuote
# from .code_block import CodeBlock


# @dataclass
# class _Paragraph(Block):
#     lines: List[str]


# # parse (text: String): Document ->
# #   match document.parse text
# #     case Nothing -> Document ([])
# #     case (doc, _) -> doc
# def parse(text: str) -> Document:
#     output = document().parse(text)
#     if output is None:
#         return Document([])
#     doc, _ = output
#     return doc


# # document ->
# #   for blocks in zero_or_more block
# #   as Parser.Value (Document blocks)
# def document() -> Parser[Document]:
#     return (
#         p.zero_or_more(block()) >> (lambda blocks:
#         Parser.Value(Document(blocks))))


# # block ->
# #   for _ in zero_or_more blank_line
# #   as
# #     # Container blocks.
# #     block_quote
# #     or list
# #     # or task_list (extension)
# #
# #     # Leaf blocks.
# #     or divider
# #     or header
# #     or indented_code_block
# #     or fenced_code_block
# #     or html
# #     or link_definition
# #     # or table (extension)
# #     or paragraph
# def block() -> Parser[Block]:
#     return (
#         p.zero_or_more(blank_line()) >> (lambda _:
#             indented_code_block()
#             | fenced_code_block()
#             | paragraph()))


# # block_quote ->
# #   for items in
# #     for first_line in text_line if line -> line starts_with '>'
# #     for lines in
# #       zero_or_more
# #       text_line if line -> line starts_with '>'
# #     let trim_prefix line -> line trim_any ['> ', '>']
# #     let blocks, _ =
# #       zero_or_more block
# #       parse
# #         (trim_prefix first_line :: lines map trim_prefix) join '\n'
# #         or ([], '')
# #     as Parser.Value blocks
# #   as Parser.Value (BlockQuote items)
# def block_quote() -> Parser[Block]:
#     def trim_prefix(line: str) -> str:
#         return (
#             line[2:] if line.startswith('> ') else
#             line[1:] if line.startswith('>') else
#             line)

#     return (
#         (
#                 text_line().if_(lambda line: line.startswith('>'))
#             >> (lambda first_line:
#                 p.zero_or_more(
#                 text_line().if_(lambda line: line.startswith('>')))
#             >> (lambda lines:
#                 Parser.Value((
#                     p.zero_or_more(block())
#                     .parse('\n'.join([
#                         trim_prefix(first_line),
#                         *[trim_prefix(line) for line in lines],
#                     ]))
#                     or ([], '')
#                 )[0])))
#         )
#         >> (lambda items:
#             Parser.Value(BlockQuote(items))))


# # indented_code_block ->
# #   for lines in one_or_more
# #     for newlines in zero_or_more blank_line
# #     for _ in indent
# #     for line in non_blank_line
# #     as Parser.Value
# #       '\n' * (newlines length)
# #       append line
# #   as Parser.Value (CodeBlock (lines join))
# def indented_code_block() -> Parser[Block]:
#     return (
#             p.one_or_more(
#                 p.zero_or_more(blank_line()) >> (lambda newlines:
#                 p.indent() >> (lambda _:
#                 non_blank_line() >> (lambda line:
#                 Parser.Value(
#                     '\n' * len(newlines)
#                     + line)))))
#         >> (lambda lines:
#             Parser.Value(CodeBlock('\n'.join(lines)))))


# # fenced_code_block ->
# #   for indent in text_at_most (3, char ' ')
# #   for open in
# #     text_at_least (3, char '`')
# #     or text_at_least (3, char '~')
# #   for language in
# #     for info_string in raw_line or Parser.Value('')
# #     as
# #       if open[0] == '`' and info_string has '`'
# #       then Parser.Error
# #       else Parser.Value (info_string trim >> split >> get (0, ''))
# #   for lines in raw_line until_delimiter line ->
# #     let close = line trim_right
# #     close == open[0] * close length
# #     and close length >= open length
# #   do Parser.Value
# #     CodeBlock (lines join '\n', language)
# def fenced_code_block() -> Parser[Block]:

#     return (
#             p.text_at_most(3, p.char(' '))
#         >> (lambda indent:
#             (p.text_at_least(3, p.char('`'))
#             | p.text_at_least(3, p.char('~')))
#         >> (lambda open:
#             ((raw_line() | Parser.Value('')) >> (lambda info_string:
#             Parser.Error()
#             if open[0] == '`' and '`' in info_string
#             else Parser.Value((info_string.strip().split() or [''])[0])))
#         >> (lambda language:
#             raw_line().until_maybe_delimiter(lambda line:
#                 line.rstrip() == open[0] * len(line.rstrip())
#                 and len(line.rstrip()) >= len(open))
#         >> (lambda lines:
#             Parser.Value(CodeBlock('\n'.join(lines), language)))))))


# # paragraph ->
# #   for lines in one_or_more non_blank_line
# #   as Parser.Value (_Paragraph lines)
# def paragraph() -> Parser[Block]:
#     return (
#         p.one_or_more(non_blank_line()) >> (lambda lines:
#         Parser.Value(_Paragraph(lines))))


# # blank_line ->
# #   raw_line if line -> line.strip == ''
# def blank_line() -> Parser[str]:
#     return raw_line().if_(lambda line: line.strip() == '')


# # non_blank_line ->
# #   raw_line if line -> line strip != ''
# def non_blank_line() -> Parser[str]:
#     return raw_line().if_(lambda line: line.strip() != '')


# # text_line ->
# #   for _ in text_at_most (3, char ' ')
# #   for line in raw_line
# #   do Parser.Value line
# def text_line() -> Parser[str]:
#     return (
#         p.text_at_most(3, p.char(' ')) >> (lambda _:
#         raw_line() >> (lambda line:
#         Parser.Value(line))))


# # raw_line ->
# #   for text in text_one_or_more (char_not '\n')
# #   for _ in zero_or_more (char '\n')
# #   as Parser.Value (text)
# #   or for _ in char '\n'
# #   as Parser.Value ''
# def raw_line() -> Parser[str]:
#     return (
#         p.text_one_or_more(p.char_not('\n')) >> (lambda text:
#         p.zero_or_one(p.char('\n')) >> (lambda _:
#         Parser.Value(text)))
#         | p.char('\n') >> (lambda _:
#         Parser.Value('')))
