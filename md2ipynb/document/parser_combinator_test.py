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

import logging
import sys
import unittest

# from typing import *

# from . import parser as p
# from .parser import Parser
# from .stream import Stream

# #====----------------------------------------------------------------------====#
# # Python does not support tail call elimination, so ill-formed
# # recursive calls could easily result in a stack overflow error.
# # Set the recursion limit to something small to make sure all the functions
# # here are scalable to any size input.
# recursion_limit = 50

# # Functions operating in more one or more inputs should run a "long test".
# # The default Python recursion limit is 1000.
# long_test_len = 10000
# #====----------------------------------------------------------------------====#

# a = TypeVar('a')


# class ParserTest(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls) -> None:
#         logging.warning(f"Setting the recursion limit to {recursion_limit}")
#         sys.setrecursionlimit(recursion_limit)
#         return super().setUpClass()

#     def test_constructors(self) -> None:
#         def check(parser: Parser[a], expected: Optional[a]) -> None:
#             self.assertEqual(
#                 parser.parse('abc'),
#                 (expected, 'abc') if expected else None)

#         check(Parser(lambda text: (42, text)), 42)
#         check(Parser.End(), None)
#         check(Parser.Token(42), 42)
#         check(Parser.Token('x'), 'x')

#     # def test_or(self) -> None:
#     #     def check(actual: Tuple[Optional[str], Optional[str], Optional[str]], expected: Optional[str]) -> None:
#     #         x, y, z = actual
#     #         self.assertEqual(
#     #             (
#     #                 (Parser.Token(x) if x else Parser.End()) |
#     #                 (Parser.Token(y) if y else Parser.End()) |
#     #                 (Parser.Token(z) if z else Parser.End())
#     #             ).parse('abc'),
#     #             (expected, 'abc') if expected else None)

#     #     check(('aa', 'bb', 'cc'), 'aa')
#     #     check(('aa', 'bb', None), 'aa')
#     #     check(('aa', None, 'cc'), 'aa')
#     #     check(('aa', None, None), 'aa')
#     #     check((None, 'bb', 'cc'), 'bb')
#     #     check((None, 'bb', None), 'bb')
#     #     check((None, None, 'cc'), 'cc')
#     #     check((None, None, None), None)

#     # def test_any_char(self) -> None:
#     #     def check(actual: str, expected: Optional[Tuple[str, str]]) -> None:
#     #         self.assertEqual(p.any_char().parse(actual), expected)

#     #     check('', None)
#     #     check('a', ('a', ''))
#     #     check('abc', ('a', 'bc'))

#     # def test_flatmap(self) -> None:
#     #     def check(actual: Tuple[str, Callable[[str], Parser[a]]], expected: Optional[Tuple[a, str]]) -> None:
#     #         text, f = actual
#     #         self.assertEqual(p.any_char().flatmap(f).parse(text), expected)

#     #     check(('', lambda c: Parser.Token(c)), None)
#     #     check(('abc', lambda c: Parser.Token(c)), ('a', 'bc'))
#     #     check(('abc', lambda c: Parser.Token(c.upper())), ('A', 'bc'))
#     #     check(('abc', lambda _: Parser.Token(42)), (42, 'bc'))
#     #     check(('abc', lambda _: Parser.End()), None)

#     # def test_bind(self) -> None:
#     #     def check(actual: Tuple[str, Callable[[str], Parser[a]]], expected: Optional[Tuple[a, str]]) -> None:
#     #         text, f = actual
#     #         self.assertEqual((p.any_char() >> f).parse(text), expected)

#     #     check(('', lambda c: Parser.Token(c)), None)
#     #     check(('abc', lambda c: Parser.Token(c)), ('a', 'bc'))
#     #     check(('abc', lambda c: Parser.Token(c.upper())), ('A', 'bc'))
#     #     check(('abc', lambda _: Parser.Token(42)), (42, 'bc'))
#     #     check(('abc', lambda _: Parser.End()), None)

#     # def test_if(self) -> None:
#     #     def check(actual: Tuple[str, Callable[[str], bool]], expected: Optional[Tuple[str, str]]) -> None:
#     #         text, condition = actual
#     #         self.assertEqual(p.any_char().if_(condition).parse(text), expected)

#     #     check(('', lambda c: True), None)
#     #     check(('', lambda c: False), None)
#     #     check(('a', lambda c: c == 'a'), ('a', ''))
#     #     check(('a', lambda c: c != 'a'), None)
#     #     check(('abc', lambda c: c == 'a'), ('a', 'bc'))
#     #     check(('abc', lambda c: c != 'a'), None)

#     # def test_while(self) -> None:
#     #     def check(actual: str, expected: Tuple[List[str], str]) -> None:
#     #         items, rest = expected
#     #         self.assertEqual(
#     #             p.any_char().while_(lambda c: c != '_').parse(actual),
#     #             (Stream.of(items), rest))

#     #     check('', ([], ''))
#     #     check('a', (['a'], ''))
#     #     check('abc', (['a', 'b', 'c'], ''))
#     #     check('_abc', ([], '_abc'))
#     #     check('a_bc', (['a'], '_bc'))
#     #     check('ab_c', (['a', 'b'], '_c'))
#     #     check('abc_', (['a', 'b', 'c'], '_'))
#     #     check('abc' * long_test_len, (list('abc' * long_test_len), ''))

#     # def test_char(self) -> None:
#     #     parse = p.char('a').parse
#     #     check(parse(''), None)
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('abc'), ('a', 'bc'))
#     #     check(parse('_'), None)
#     #     check(parse('_bc'), None)

#     #     parse = p.char(['a', 'b']).parse
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('b'), ('b', ''))
#     #     check(parse('_'), None)

#     #     parse = p.char({'a', 'b'}).parse
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('b'), ('b', ''))
#     #     check(parse('_'), None)

#     #     def chars() -> Iterable[str]:
#     #         yield 'a'
#     #         yield 'b'
#     #     parse = p.char(chars()).parse
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('b'), ('b', ''))
#     #     check(parse('_'), None)

#     # def test_char_not(self) -> None:
#     #     parse = p.char_not('a').parse
#     #     check(parse(''), None)
#     #     check(parse('_'), ('_', ''))
#     #     check(parse('_bc'), ('_', 'bc'))
#     #     check(parse('a'), None)
#     #     check(parse('abc'), None)

#     #     parse = p.char_not(['a', 'b']).parse
#     #     check(parse('_'), ('_', ''))
#     #     check(parse('a'), None)
#     #     check(parse('b'), None)

#     #     parse = p.char_not({'a', 'b'}).parse
#     #     check(parse('_'), ('_', ''))
#     #     check(parse('a'), None)
#     #     check(parse('b'), None)

#     #     def chars() -> Iterable[str]:
#     #         yield 'a'
#     #         yield 'b'
#     #     parse = p.char_not(chars()).parse
#     #     check(parse('_'), ('_', ''))
#     #     check(parse('a'), None)
#     #     check(parse('b'), None)

#     # def test_while(self) -> None:
#     #     parse = p.any_char().repeat_while(lambda c: c != '_').parse
#     #     check(parse(''), ([], ''))
#     #     check(parse('a'), (['a'], ''))
#     #     check(parse('abc'), (['a', 'b', 'c'], ''))
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().repeat_while(lambda c: c != '_').parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_while(self) -> None:
#     #     parse = p.any_char().text_while(lambda c: c != '_').parse
#     #     check(parse(''), ('', ''))
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('abc'), ('abc', ''))
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().text_while(lambda c: c != '_').parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_until_delimiter(self) -> None:
#     #     parse = p.any_char().until_delimiter(lambda c: c == '_').parse
#     #     check(parse(''), None)
#     #     check(parse('a'), None)
#     #     check(parse('abc'), None)
#     #     check(parse('_'), ([], ''))
#     #     check(parse('_abc'), ([], 'abc'))
#     #     check(parse('a_bc'), (['a'], 'bc'))
#     #     check(parse('ab_c'), (['a', 'b'], 'c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], ''))

#     #     parse = p.any_char().until_delimiter('_').parse
#     #     check(parse(''), None)
#     #     check(parse('a'), None)
#     #     check(parse('abc'), None)
#     #     check(parse('_'), ([], ''))
#     #     check(parse('_abc'), ([], 'abc'))
#     #     check(parse('a_bc'), (['a'], 'bc'))
#     #     check(parse('ab_c'), (['a', 'b'], 'c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().until_delimiter(lambda c: c == '_').parse
#     #     check(parse(long_test + '_'), (list(long_test), ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().until_delimiter('_').parse
#     #     check(parse(long_test + '_'), (list(long_test), ''))

#     # def test_text_until_delimiter(self) -> None:
#     #     parse = p.any_char().text_until_delimiter(lambda c: c == '_').parse
#     #     check(parse(''), None)
#     #     check(parse('a'), None)
#     #     check(parse('abc'), None)
#     #     check(parse('_'), ('', ''))
#     #     check(parse('_abc'), ('', 'abc'))
#     #     check(parse('a_bc'), ('a', 'bc'))
#     #     check(parse('ab_c'), ('ab', 'c'))
#     #     check(parse('abc_'), ('abc', ''))

#     #     parse = p.any_char().text_until_delimiter('_').parse
#     #     check(parse(''), None)
#     #     check(parse('a'), None)
#     #     check(parse('abc'), None)
#     #     check(parse('_'), ('', ''))
#     #     check(parse('_abc'), ('', 'abc'))
#     #     check(parse('a_bc'), ('a', 'bc'))
#     #     check(parse('ab_c'), ('ab', 'c'))
#     #     check(parse('abc_'), ('abc', ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().text_until_delimiter(lambda c: c == '_').parse
#     #     check(parse(long_test + '_'), (long_test, ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().text_until_delimiter('_').parse
#     #     check(parse(long_test + '_'), (long_test, ''))

#     # def test_until_maybe_delimiter(self) -> None:
#     #     parse = p.any_char().until_maybe_delimiter(lambda c: c == '_').parse
#     #     check(parse(''), ([], ''))
#     #     check(parse('a'), (['a'], ''))
#     #     check(parse('abc'), (['a', 'b', 'c'], ''))
#     #     check(parse('_'), ([], ''))
#     #     check(parse('_abc'), ([], 'abc'))
#     #     check(parse('a_bc'), (['a'], 'bc'))
#     #     check(parse('ab_c'), (['a', 'b'], 'c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], ''))

#     #     parse = p.any_char().until_maybe_delimiter('_').parse
#     #     check(parse(''), ([], ''))
#     #     check(parse('a'), (['a'], ''))
#     #     check(parse('abc'), (['a', 'b', 'c'], ''))
#     #     check(parse('_'), ([], ''))
#     #     check(parse('_abc'), ([], 'abc'))
#     #     check(parse('a_bc'), (['a'], 'bc'))
#     #     check(parse('ab_c'), (['a', 'b'], 'c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().until_maybe_delimiter(lambda c: c == '_').parse
#     #     check(parse(long_test), (list(long_test), ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().until_maybe_delimiter('_').parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_until_maybe_delimiter(self) -> None:
#     #     parse = p.any_char().text_until_maybe_delimiter(lambda c: c == '_').parse
#     #     check(parse(''), ('', ''))
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('abc'), ('abc', ''))
#     #     check(parse('_'), ('', ''))
#     #     check(parse('_abc'), ('', 'abc'))
#     #     check(parse('a_bc'), ('a', 'bc'))
#     #     check(parse('ab_c'), ('ab', 'c'))
#     #     check(parse('abc_'), ('abc', ''))

#     #     parse = p.any_char().text_until_maybe_delimiter('_').parse
#     #     check(parse(''), ('', ''))
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('abc'), ('abc', ''))
#     #     check(parse('_'), ('', ''))
#     #     check(parse('_abc'), ('', 'abc'))
#     #     check(parse('a_bc'), ('a', 'bc'))
#     #     check(parse('ab_c'), ('ab', 'c'))
#     #     check(parse('abc_'), ('abc', ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().text_until_maybe_delimiter(lambda c: c == '_').parse
#     #     check(parse(long_test), (long_test, ''))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.any_char().text_until_maybe_delimiter('_').parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_zero_or_one(self) -> None:
#     #     parse = p.zero_or_one(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(''), ([], ''))
#     #     check(parse('a'), (['a'], ''))
#     #     check(parse('abc'), (['a'], 'bc'))
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a'], 'b_c'))
#     #     check(parse('abc_'), (['a'], 'bc_'))

#     # def test_text_zero_or_one(self) -> None:
#     #     parse = p.text_zero_or_one(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(''), ('', ''))
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('abc'), ('a', 'bc'))
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('a', 'b_c'))
#     #     check(parse('abc_'), ('a', 'bc_'))

#     # def test_zero_or_more(self) -> None:
#     #     parse = p.zero_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(''), ([], ''))
#     #     check(parse('a'), (['a'], ''))
#     #     check(parse('abc'), (['a', 'b', 'c'], ''))
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.zero_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_zero_or_more(self) -> None:
#     #     parse = p.text_zero_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(''), ('', ''))
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('abc'), ('abc', ''))
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.text_zero_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_one_or_more(self) -> None:
#     #     parse = p.one_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(''), None)
#     #     check(parse('a'), (['a'], ''))
#     #     check(parse('abc'), (['a', 'b', 'c'], ''))
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.one_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_one_or_more(self) -> None:
#     #     parse = p.text_one_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(''), None)
#     #     check(parse('a'), ('a', ''))
#     #     check(parse('abc'), ('abc', ''))
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.text_one_or_more(p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_at_most(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.at_most(-1, p.any_char())

#     #     parse = p.at_most(0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), ([], 'a_bc'))
#     #     check(parse('ab_c'), ([], 'ab_c'))
#     #     check(parse('abc_'), ([], 'abc_'))

#     #     parse = p.at_most(1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a'], 'b_c'))
#     #     check(parse('abc_'), (['a'], 'bc_'))

#     #     parse = p.at_most(3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.at_most(len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_at_most(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.text_at_most(-1, p.any_char())

#     #     parse = p.text_at_most(0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('', 'a_bc'))
#     #     check(parse('ab_c'), ('', 'ab_c'))
#     #     check(parse('abc_'), ('', 'abc_'))

#     #     parse = p.text_at_most(1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('a', 'b_c'))
#     #     check(parse('abc_'), ('a', 'bc_'))

#     #     parse = p.text_at_most(3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.text_at_most(len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_exactly(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.exactly(-1, p.any_char())

#     #     parse = p.exactly(0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), ([], 'a_bc'))
#     #     check(parse('ab_c'), ([], 'ab_c'))
#     #     check(parse('abc_'), ([], 'abc_'))

#     #     parse = p.exactly(1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a'], 'b_c'))
#     #     check(parse('abc_'), (['a'], 'bc_'))

#     #     parse = p.exactly(3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), None)
#     #     check(parse('ab_c'), None)
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.exactly(len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_exactly(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.text_exactly(-1, p.any_char())

#     #     parse = p.text_exactly(0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('', 'a_bc'))
#     #     check(parse('ab_c'), ('', 'ab_c'))
#     #     check(parse('abc_'), ('', 'abc_'))

#     #     parse = p.text_exactly(1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('a', 'b_c'))
#     #     check(parse('abc_'), ('a', 'bc_'))

#     #     parse = p.text_exactly(3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), None)
#     #     check(parse('ab_c'), None)
#     #     check(parse('abc_'), ('abc', '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.text_exactly(len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_at_least(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.at_least(-1, p.any_char())

#     #     parse = p.at_least(0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     parse = p.at_least(1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     parse = p.at_least(3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), None)
#     #     check(parse('ab_c'), None)
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.at_least(len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_at_least(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.text_at_least(-1, p.any_char())

#     #     parse = p.text_at_least(0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     parse = p.text_at_least(1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     parse = p.text_at_least(3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), None)
#     #     check(parse('ab_c'), None)
#     #     check(parse('abc_'), ('abc', '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.text_at_least(len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_between(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.between(-1, 1, p.any_char())
#     #     with self.assertRaises(ValueError):
#     #         p.between(1, 0, p.any_char())

#     #     parse = p.between(0, 0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), ([], 'a_bc'))
#     #     check(parse('ab_c'), ([], 'ab_c'))
#     #     check(parse('abc_'), ([], 'abc_'))

#     #     parse = p.between(0, 1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a'], 'b_c'))
#     #     check(parse('abc_'), (['a'], 'bc_'))

#     #     parse = p.between(0, 3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ([], '_abc'))
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     parse = p.between(1, 3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), (['a'], '_bc'))
#     #     check(parse('ab_c'), (['a', 'b'], '_c'))
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     parse = p.between(3, 3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), None)
#     #     check(parse('ab_c'), None)
#     #     check(parse('abc_'), (['a', 'b', 'c'], '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.between(0, len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (list(long_test), ''))

#     # def test_text_between(self) -> None:
#     #     with self.assertRaises(ValueError):
#     #         p.text_between(-1, 1, p.any_char())
#     #     with self.assertRaises(ValueError):
#     #         p.text_between(1, 0, p.any_char())

#     #     parse = p.text_between(0, 0, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('', 'a_bc'))
#     #     check(parse('ab_c'), ('', 'ab_c'))
#     #     check(parse('abc_'), ('', 'abc_'))

#     #     parse = p.text_between(0, 1, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('a', 'b_c'))
#     #     check(parse('abc_'), ('a', 'bc_'))

#     #     parse = p.text_between(0, 3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), ('', '_abc'))
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     parse = p.text_between(1, 3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), ('a', '_bc'))
#     #     check(parse('ab_c'), ('ab', '_c'))
#     #     check(parse('abc_'), ('abc', '_'))

#     #     parse = p.text_between(3, 3, p.char({'a', 'b', 'c'})).parse
#     #     check(parse('_abc'), None)
#     #     check(parse('a_bc'), None)
#     #     check(parse('ab_c'), None)
#     #     check(parse('abc_'), ('abc', '_'))

#     #     long_test = 'abc' * long_test_len
#     #     parse = p.text_between(0, len(long_test), p.char({'a', 'b', 'c'})).parse
#     #     check(parse(long_test), (long_test, ''))

#     # def test_digit(self) -> None:
#     #     parse = p.digit().parse
#     #     check(parse(''), None)
#     #     for ch in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
#     #         check(parse(ch), (ch, ''))
#     #     check(parse('123'), ('1', '23'))
#     #     check(parse('abc'), None)
#     #     check(parse('_'), None)

#     # def test_letter(self) -> None:
#     #     parse = p.letter().parse
#     #     check(parse(''), None)
#     #     for ch in ['a', 'b', 'c', 'z', 'A', 'B', 'C', 'Z']:
#     #         check(parse(ch), (ch, ''))
#     #     check(parse('abc'), ('a', 'bc'))
#     #     check(parse('123'), None)
#     #     check(parse('_'), None)

#     # def test_lowercase(self) -> None:
#     #     parse = p.lowercase().parse
#     #     check(parse(''), None)
#     #     for ch in ['a', 'b', 'c', 'z']:
#     #         check(parse(ch), (ch, ''))
#     #     check(parse('abc'), ('a', 'bc'))
#     #     check(parse('ABC'), None)
#     #     check(parse('123'), None)
#     #     check(parse('_'), None)

#     # def test_uppercase(self) -> None:
#     #     parse = p.uppercase().parse
#     #     check(parse(''), None)
#     #     for ch in ['A', 'B', 'C', 'Z']:
#     #         check(parse(ch), (ch, ''))
#     #     check(parse('ABC'), ('A', 'BC'))
#     #     check(parse('abc'), None)
#     #     check(parse('123'), None)
#     #     check(parse('_'), None)

#     # def test_alphanumeric(self) -> None:
#     #     parse = p.alphanumeric().parse
#     #     check(parse(''), None)
#     #     for ch in ['a', 'z', 'A', 'Z', '0', '9']:
#     #         check(parse(ch), (ch, ''))
#     #     check(parse('abc'), ('a', 'bc'))
#     #     check(parse('_'), None)

#     # def test_space(self) -> None:
#     #     parse = p.space().parse
#     #     check(parse(''), None)
#     #     for ch in [' ', '\t', '\n', '\r', '\x0b', '\f']:
#     #         check(parse(ch), (ch, ''))
#     #     check(parse('   '), (' ', '  '))
#     #     check(parse('a'), None)
#     #     check(parse('1'), None)
#     #     check(parse('_'), None)

#     # def test_indent(self) -> None:
#     #     parse = p.indent().parse
#     #     check(parse(''), None)
#     #     check(parse('aaa'), None)
#     #     check(parse('   aaa'), None)
#     #     check(parse('    aaa'), ('    ', 'aaa'))
#     #     check(parse('   \taaa'), ('   \t', 'aaa'))
#     #     check(parse('  \taaa'), ('  \t', 'aaa'))
#     #     check(parse(' \taaa'), (' \t', 'aaa'))
#     #     check(parse('\taaa'), ('\t', 'aaa'))
