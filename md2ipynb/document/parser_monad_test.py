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

from typing import *

from . import parser_monad as p
from .parser_monad import Parser

#====----------------------------------------------------------------------====#
# Python does not support tail call elimination, so ill-formed
# recursive calls could easily result in a stack overflow error.
# Set the recursion limit to something small to make sure all the functions
# here are scalable to any size input.
recursion_limit = 50

# Functions operating in more one or more inputs should run a "long test".
# The default Python recursion limit is 1000.
long_test_len = 10000
#====----------------------------------------------------------------------====#


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.warning(f"Setting the recursion limit to {recursion_limit}")
        sys.setrecursionlimit(recursion_limit)
        return super().setUpClass()

    def test_constructors(self) -> None:
        p_value = Parser(lambda _: ('a', 'bc')).parse
        self.assertEqual(p_value(''), ('a', 'bc'))
        self.assertNotEqual(p_value(''), ('_', 'bc'))
        self.assertNotEqual(p_value(''), ('a', '__'))

        p_nothing: Parser[Any] = Parser(lambda _: None)
        self.assertEqual(p_nothing.parse(''), None)

        x = Parser.Value('x').parse
        self.assertEqual(x('abc'), ('x', 'abc'))
        self.assertNotEqual(x('abc'), ('_', 'abc'))
        self.assertNotEqual(x('abc'), ('x', '___'))

        e = Parser.Error().parse
        self.assertEqual(e('abc'), None)

    def test_or(self) -> None:
        x1 = Parser.Value('x1')
        x2 = Parser.Value('x2')
        x3 = Parser.Value('x3')
        e1 = Parser.Error()
        e2 = Parser.Error()
        e3 = Parser.Error()
        self.assertEqual((x1 | x2).parse('_'), ('x1', '_'))
        self.assertEqual((x1 | e2).parse('_'), ('x1', '_'))
        self.assertEqual((e1 | x2).parse('_'), ('x2', '_'))
        self.assertEqual((e1 | e2).parse('_'), None)
        self.assertEqual((e1 | e2 | x3).parse('_'), ('x3', '_'))
        self.assertEqual((e1 | e2 | e3).parse('_'), None)

    def test_any_char(self) -> None:
        parse = p.any_char().parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('a', 'bc'))

    def test_flatmap(self) -> None:
        parse = (
            p.any_char().flatmap(lambda c:
            Parser.Value(c.upper()))
        ).parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('abc'), ('A', 'bc'))

        str_to_int = (
            p.any_char().flatmap(lambda _:
            Parser.Value(42))
        ).parse
        self.assertEqual(str_to_int(''), None)
        self.assertEqual(str_to_int('abc'), (42, 'bc'))

    def test_bind(self) -> None:
        parse = (
            p.any_char() >> (lambda c:
            Parser.Value(c.upper()))
        ).parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('abc'), ('A', 'bc'))

        str_to_int = (
            p.any_char() >> (lambda _:
            Parser.Value(42))
        ).parse
        self.assertEqual(str_to_int(''), None)
        self.assertEqual(str_to_int('abc'), (42, 'bc'))

    def test_if(self) -> None:
        parse = p.any_char().if_(lambda c: c == 'a').parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('_'), None)
        self.assertEqual(parse('abc'), ('a', 'bc'))

    def test_char(self) -> None:
        parse = p.char('a').parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('a', 'bc'))
        self.assertEqual(parse('_'), None)
        self.assertEqual(parse('_bc'), None)

        parse = p.char(['a', 'b']).parse
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('b'), ('b', ''))
        self.assertEqual(parse('_'), None)

        parse = p.char({'a', 'b'}).parse
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('b'), ('b', ''))
        self.assertEqual(parse('_'), None)

        def chars() -> Iterable[str]:
            yield 'a'
            yield 'b'
        parse = p.char(chars()).parse
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('b'), ('b', ''))
        self.assertEqual(parse('_'), None)

    def test_char_not(self) -> None:
        parse = p.char_not('a').parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('_'), ('_', ''))
        self.assertEqual(parse('_bc'), ('_', 'bc'))
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('abc'), None)

        parse = p.char_not(['a', 'b']).parse
        self.assertEqual(parse('_'), ('_', ''))
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('b'), None)

        parse = p.char_not({'a', 'b'}).parse
        self.assertEqual(parse('_'), ('_', ''))
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('b'), None)

        def chars() -> Iterable[str]:
            yield 'a'
            yield 'b'
        parse = p.char_not(chars()).parse
        self.assertEqual(parse('_'), ('_', ''))
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('b'), None)

    def test_while(self) -> None:
        parse = p.any_char().repeat_while(lambda c: c != '_').parse
        self.assertEqual(parse(''), ([], ''))
        self.assertEqual(parse('a'), (['a'], ''))
        self.assertEqual(parse('abc'), (['a', 'b', 'c'], ''))
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        long_test = 'abc' * long_test_len
        parse = p.any_char().repeat_while(lambda c: c != '_').parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_while(self) -> None:
        parse = p.any_char().text_while(lambda c: c != '_').parse
        self.assertEqual(parse(''), ('', ''))
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('abc', ''))
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        long_test = 'abc' * long_test_len
        parse = p.any_char().text_while(lambda c: c != '_').parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_until_delimiter(self) -> None:
        parse = p.any_char().until_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('abc'), None)
        self.assertEqual(parse('_'), ([], ''))
        self.assertEqual(parse('_abc'), ([], 'abc'))
        self.assertEqual(parse('a_bc'), (['a'], 'bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], 'c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], ''))

        parse = p.any_char().until_delimiter('_').parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('abc'), None)
        self.assertEqual(parse('_'), ([], ''))
        self.assertEqual(parse('_abc'), ([], 'abc'))
        self.assertEqual(parse('a_bc'), (['a'], 'bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], 'c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().until_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(long_test + '_'), (list(long_test), ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().until_delimiter('_').parse
        self.assertEqual(parse(long_test + '_'), (list(long_test), ''))

    def test_text_until_delimiter(self) -> None:
        parse = p.any_char().text_until_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('abc'), None)
        self.assertEqual(parse('_'), ('', ''))
        self.assertEqual(parse('_abc'), ('', 'abc'))
        self.assertEqual(parse('a_bc'), ('a', 'bc'))
        self.assertEqual(parse('ab_c'), ('ab', 'c'))
        self.assertEqual(parse('abc_'), ('abc', ''))

        parse = p.any_char().text_until_delimiter('_').parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('abc'), None)
        self.assertEqual(parse('_'), ('', ''))
        self.assertEqual(parse('_abc'), ('', 'abc'))
        self.assertEqual(parse('a_bc'), ('a', 'bc'))
        self.assertEqual(parse('ab_c'), ('ab', 'c'))
        self.assertEqual(parse('abc_'), ('abc', ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().text_until_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(long_test + '_'), (long_test, ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().text_until_delimiter('_').parse
        self.assertEqual(parse(long_test + '_'), (long_test, ''))

    def test_until_maybe_delimiter(self) -> None:
        parse = p.any_char().until_maybe_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(''), ([], ''))
        self.assertEqual(parse('a'), (['a'], ''))
        self.assertEqual(parse('abc'), (['a', 'b', 'c'], ''))
        self.assertEqual(parse('_'), ([], ''))
        self.assertEqual(parse('_abc'), ([], 'abc'))
        self.assertEqual(parse('a_bc'), (['a'], 'bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], 'c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], ''))

        parse = p.any_char().until_maybe_delimiter('_').parse
        self.assertEqual(parse(''), ([], ''))
        self.assertEqual(parse('a'), (['a'], ''))
        self.assertEqual(parse('abc'), (['a', 'b', 'c'], ''))
        self.assertEqual(parse('_'), ([], ''))
        self.assertEqual(parse('_abc'), ([], 'abc'))
        self.assertEqual(parse('a_bc'), (['a'], 'bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], 'c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().until_maybe_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().until_maybe_delimiter('_').parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_until_maybe_delimiter(self) -> None:
        parse = p.any_char().text_until_maybe_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(''), ('', ''))
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('abc', ''))
        self.assertEqual(parse('_'), ('', ''))
        self.assertEqual(parse('_abc'), ('', 'abc'))
        self.assertEqual(parse('a_bc'), ('a', 'bc'))
        self.assertEqual(parse('ab_c'), ('ab', 'c'))
        self.assertEqual(parse('abc_'), ('abc', ''))

        parse = p.any_char().text_until_maybe_delimiter('_').parse
        self.assertEqual(parse(''), ('', ''))
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('abc', ''))
        self.assertEqual(parse('_'), ('', ''))
        self.assertEqual(parse('_abc'), ('', 'abc'))
        self.assertEqual(parse('a_bc'), ('a', 'bc'))
        self.assertEqual(parse('ab_c'), ('ab', 'c'))
        self.assertEqual(parse('abc_'), ('abc', ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().text_until_maybe_delimiter(lambda c: c == '_').parse
        self.assertEqual(parse(long_test), (long_test, ''))

        long_test = 'abc' * long_test_len
        parse = p.any_char().text_until_maybe_delimiter('_').parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_zero_or_one(self) -> None:
        parse = p.zero_or_one(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(''), ([], ''))
        self.assertEqual(parse('a'), (['a'], ''))
        self.assertEqual(parse('abc'), (['a'], 'bc'))
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a'], 'b_c'))
        self.assertEqual(parse('abc_'), (['a'], 'bc_'))

    def test_text_zero_or_one(self) -> None:
        parse = p.text_zero_or_one(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(''), ('', ''))
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('a', 'bc'))
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('a', 'b_c'))
        self.assertEqual(parse('abc_'), ('a', 'bc_'))

    def test_zero_or_more(self) -> None:
        parse = p.zero_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(''), ([], ''))
        self.assertEqual(parse('a'), (['a'], ''))
        self.assertEqual(parse('abc'), (['a', 'b', 'c'], ''))
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        long_test = 'abc' * long_test_len
        parse = p.zero_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_zero_or_more(self) -> None:
        parse = p.text_zero_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(''), ('', ''))
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('abc', ''))
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        long_test = 'abc' * long_test_len
        parse = p.text_zero_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_one_or_more(self) -> None:
        parse = p.one_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), (['a'], ''))
        self.assertEqual(parse('abc'), (['a', 'b', 'c'], ''))
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        long_test = 'abc' * long_test_len
        parse = p.one_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_one_or_more(self) -> None:
        parse = p.text_one_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('a'), ('a', ''))
        self.assertEqual(parse('abc'), ('abc', ''))
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        long_test = 'abc' * long_test_len
        parse = p.text_one_or_more(p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_at_most(self) -> None:
        with self.assertRaises(ValueError):
            p.at_most(-1, p.any_char())

        parse = p.at_most(0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), ([], 'a_bc'))
        self.assertEqual(parse('ab_c'), ([], 'ab_c'))
        self.assertEqual(parse('abc_'), ([], 'abc_'))

        parse = p.at_most(1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a'], 'b_c'))
        self.assertEqual(parse('abc_'), (['a'], 'bc_'))

        parse = p.at_most(3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        long_test = 'abc' * long_test_len
        parse = p.at_most(len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_at_most(self) -> None:
        with self.assertRaises(ValueError):
            p.text_at_most(-1, p.any_char())

        parse = p.text_at_most(0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('', 'a_bc'))
        self.assertEqual(parse('ab_c'), ('', 'ab_c'))
        self.assertEqual(parse('abc_'), ('', 'abc_'))

        parse = p.text_at_most(1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('a', 'b_c'))
        self.assertEqual(parse('abc_'), ('a', 'bc_'))

        parse = p.text_at_most(3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        long_test = 'abc' * long_test_len
        parse = p.text_at_most(len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_exactly(self) -> None:
        with self.assertRaises(ValueError):
            p.exactly(-1, p.any_char())

        parse = p.exactly(0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), ([], 'a_bc'))
        self.assertEqual(parse('ab_c'), ([], 'ab_c'))
        self.assertEqual(parse('abc_'), ([], 'abc_'))

        parse = p.exactly(1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a'], 'b_c'))
        self.assertEqual(parse('abc_'), (['a'], 'bc_'))

        parse = p.exactly(3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), None)
        self.assertEqual(parse('ab_c'), None)
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        long_test = 'abc' * long_test_len
        parse = p.exactly(len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_exactly(self) -> None:
        with self.assertRaises(ValueError):
            p.text_exactly(-1, p.any_char())

        parse = p.text_exactly(0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('', 'a_bc'))
        self.assertEqual(parse('ab_c'), ('', 'ab_c'))
        self.assertEqual(parse('abc_'), ('', 'abc_'))

        parse = p.text_exactly(1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('a', 'b_c'))
        self.assertEqual(parse('abc_'), ('a', 'bc_'))

        parse = p.text_exactly(3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), None)
        self.assertEqual(parse('ab_c'), None)
        self.assertEqual(parse('abc_'), ('abc', '_'))

        long_test = 'abc' * long_test_len
        parse = p.text_exactly(len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_at_least(self) -> None:
        with self.assertRaises(ValueError):
            p.at_least(-1, p.any_char())

        parse = p.at_least(0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        parse = p.at_least(1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        parse = p.at_least(3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), None)
        self.assertEqual(parse('ab_c'), None)
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        long_test = 'abc' * long_test_len
        parse = p.at_least(len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_at_least(self) -> None:
        with self.assertRaises(ValueError):
            p.text_at_least(-1, p.any_char())

        parse = p.text_at_least(0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        parse = p.text_at_least(1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        parse = p.text_at_least(3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), None)
        self.assertEqual(parse('ab_c'), None)
        self.assertEqual(parse('abc_'), ('abc', '_'))

        long_test = 'abc' * long_test_len
        parse = p.text_at_least(len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_between(self) -> None:
        with self.assertRaises(ValueError):
            p.between(-1, 1, p.any_char())
        with self.assertRaises(ValueError):
            p.between(1, 0, p.any_char())

        parse = p.between(0, 0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), ([], 'a_bc'))
        self.assertEqual(parse('ab_c'), ([], 'ab_c'))
        self.assertEqual(parse('abc_'), ([], 'abc_'))

        parse = p.between(0, 1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a'], 'b_c'))
        self.assertEqual(parse('abc_'), (['a'], 'bc_'))

        parse = p.between(0, 3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ([], '_abc'))
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        parse = p.between(1, 3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), (['a'], '_bc'))
        self.assertEqual(parse('ab_c'), (['a', 'b'], '_c'))
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        parse = p.between(3, 3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), None)
        self.assertEqual(parse('ab_c'), None)
        self.assertEqual(parse('abc_'), (['a', 'b', 'c'], '_'))

        long_test = 'abc' * long_test_len
        parse = p.between(0, len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (list(long_test), ''))

    def test_text_between(self) -> None:
        with self.assertRaises(ValueError):
            p.text_between(-1, 1, p.any_char())
        with self.assertRaises(ValueError):
            p.text_between(1, 0, p.any_char())

        parse = p.text_between(0, 0, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('', 'a_bc'))
        self.assertEqual(parse('ab_c'), ('', 'ab_c'))
        self.assertEqual(parse('abc_'), ('', 'abc_'))

        parse = p.text_between(0, 1, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('a', 'b_c'))
        self.assertEqual(parse('abc_'), ('a', 'bc_'))

        parse = p.text_between(0, 3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), ('', '_abc'))
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        parse = p.text_between(1, 3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), ('a', '_bc'))
        self.assertEqual(parse('ab_c'), ('ab', '_c'))
        self.assertEqual(parse('abc_'), ('abc', '_'))

        parse = p.text_between(3, 3, p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse('_abc'), None)
        self.assertEqual(parse('a_bc'), None)
        self.assertEqual(parse('ab_c'), None)
        self.assertEqual(parse('abc_'), ('abc', '_'))

        long_test = 'abc' * long_test_len
        parse = p.text_between(0, len(long_test), p.char({'a', 'b', 'c'})).parse
        self.assertEqual(parse(long_test), (long_test, ''))

    def test_digit(self) -> None:
        parse = p.digit().parse
        self.assertEqual(parse(''), None)
        for ch in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.assertEqual(parse(ch), (ch, ''))
        self.assertEqual(parse('123'), ('1', '23'))
        self.assertEqual(parse('abc'), None)
        self.assertEqual(parse('_'), None)

    def test_letter(self) -> None:
        parse = p.letter().parse
        self.assertEqual(parse(''), None)
        for ch in ['a', 'b', 'c', 'z', 'A', 'B', 'C', 'Z']:
            self.assertEqual(parse(ch), (ch, ''))
        self.assertEqual(parse('abc'), ('a', 'bc'))
        self.assertEqual(parse('123'), None)
        self.assertEqual(parse('_'), None)

    def test_lowercase(self) -> None:
        parse = p.lowercase().parse
        self.assertEqual(parse(''), None)
        for ch in ['a', 'b', 'c', 'z']:
            self.assertEqual(parse(ch), (ch, ''))
        self.assertEqual(parse('abc'), ('a', 'bc'))
        self.assertEqual(parse('ABC'), None)
        self.assertEqual(parse('123'), None)
        self.assertEqual(parse('_'), None)

    def test_uppercase(self) -> None:
        parse = p.uppercase().parse
        self.assertEqual(parse(''), None)
        for ch in ['A', 'B', 'C', 'Z']:
            self.assertEqual(parse(ch), (ch, ''))
        self.assertEqual(parse('ABC'), ('A', 'BC'))
        self.assertEqual(parse('abc'), None)
        self.assertEqual(parse('123'), None)
        self.assertEqual(parse('_'), None)

    def test_alphanumeric(self) -> None:
        parse = p.alphanumeric().parse
        self.assertEqual(parse(''), None)
        for ch in ['a', 'z', 'A', 'Z', '0', '9']:
            self.assertEqual(parse(ch), (ch, ''))
        self.assertEqual(parse('abc'), ('a', 'bc'))
        self.assertEqual(parse('_'), None)

    def test_space(self) -> None:
        parse = p.space().parse
        self.assertEqual(parse(''), None)
        for ch in [' ', '\t', '\n', '\r', '\x0b', '\f']:
            self.assertEqual(parse(ch), (ch, ''))
        self.assertEqual(parse('   '), (' ', '  '))
        self.assertEqual(parse('a'), None)
        self.assertEqual(parse('1'), None)
        self.assertEqual(parse('_'), None)

    def test_indent(self) -> None:
        parse = p.indent().parse
        self.assertEqual(parse(''), None)
        self.assertEqual(parse('aaa'), None)
        self.assertEqual(parse('   aaa'), None)
        self.assertEqual(parse('    aaa'), ('    ', 'aaa'))
        self.assertEqual(parse('   \taaa'), ('   \t', 'aaa'))
        self.assertEqual(parse('  \taaa'), ('  \t', 'aaa'))
        self.assertEqual(parse(' \taaa'), (' \t', 'aaa'))
        self.assertEqual(parse('\taaa'), ('\t', 'aaa'))
