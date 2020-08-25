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

from ..bullet_list import BulletList
from ..list_item import ListItem

# from .parser import Parser
# from .parser import _Paragraph
# from .parser_test import ParserTestCase

# p = Parser()


# https://github.github.com/gfm/#lists
# https://github.github.com/gfm/#list-items
# class ParserBulletListTest(ParserTestCase):
#     def test_empty(self) -> None:
#         lines = [
#             '-', '', '- ', '',
#             '+', '', '+ ', '',
#             '*', '', '* ', '',
#         ]
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BulletList(),
#             BulletList(),
#             BulletList(),
#             BulletList(),
#             BulletList(),
#             BulletList(),
#         ])

#     def test_one_item(self) -> None:
#         lines = ['- aaa', '', '+ bbb', '', '* ccc']
#         self.assertEqual(list(p.parse_blocks(lines)), [
#             BulletList([
#                 ListItem([_Paragraph('aaa')]),
#             ]),
#             BulletList([
#                 ListItem([_Paragraph('bbb')]),
#             ]),
#             BulletList([
#                 ListItem([_Paragraph('ccc')]),
#             ]),
#         ])

#     # def test_multiple_items(self) -> None:
#     #     p.reset([
#     #         '- aa', '- ab', '- ac', '',
#     #         '+ ba', '+ bb', '+ bc', '',
#     #         '* ca', '* cb', '* cc'])
#     #     self.assertEqual(p._parse_blocks(), [
#     #         BulletList([_Paragraph('aa'), _Paragraph('ab'), _Paragraph('ac')]),
#     #         BulletList([_Paragraph('ba'), _Paragraph('bb'), _Paragraph('bc')]),
#     #         BulletList([_Paragraph('ca'), _Paragraph('cb'), _Paragraph('cc')]),
#     #     ])

#     # -  aaa
#     #    -  bbb
#     #       -  ccc
#     #
#     # BulletList([
#     #   _Paragraph('aaa'),
#     #   BulletList([
#     #       _Paragraph('bbb'),
#     #       BulletList([
#     #           _Paragraph('ccc'),
#     #       ]),
#     #   ]),
#     # ])

#     # -   aaa
#     #    -   bbb
#     #       -   ccc
#     #
#     # BulletList([_Paragraph('aaa'), _Paragraph('bbb - ccc')])

#     # *    aaa
#     #      * bbb
#     # 	 * ccc
#     #
#     # BullettList([
#     #   _Paragraph('aaa'),
#     #   BulletList([
#     #       _Paragraph('bbb'),
#     #       _Paragraph('ccc'),
#     #   ]),
#     # ])

#     # list item vs code block: list item
#     # -    one
#     #
#     #     two

#     # list item vs divider: divider
#     # * List 1
#     # * * *
#     # * List 2

#     # - List 1
#     # - * * *
#     # - List 1
