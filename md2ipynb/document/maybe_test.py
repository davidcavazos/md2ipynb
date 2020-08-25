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

import unittest
import logging
import sys

from dataclasses import dataclass, field
from typing import (
    List,
    Optional,
    Tuple,
    TypeVar,
)

from .maybe import Maybe, while_

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

a = TypeVar('a')


class MaybeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.warning(f"Setting the recursion limit to {recursion_limit}")
        sys.setrecursionlimit(recursion_limit)
        return super().setUpClass()

    def test_constructors(self) -> None:
        self.assertEqual(Maybe.Nothing(), Maybe.Nothing())
        self.assertEqual(Maybe.Value(1), Maybe.Value(1))
        self.assertNotEqual(Maybe.Value(1), Maybe.Nothing())
        self.assertNotEqual(Maybe.Value(1), Maybe.Value(0))

    def test_py(self) -> None:
        def check(actual: Maybe[int], expected: Optional[int]) -> None:
            self.assertEqual(actual.py(), expected)

        check(Maybe.Nothing(), None)
        check(Maybe.Value(1), 1)

    def test_from_optional(self) -> None:
        def check(actual: Optional[int], expected: Optional[int]) -> None:
            self.assertEqual(Maybe.of(actual).py(), expected)

        check(None, None)
        check(1, 1)

    def test_to_string(self) -> None:
        def check(actual: Optional[a], expected: str) -> None:
            self.assertEqual(str(Maybe.of(actual)), expected)

        check(None, 'None')
        check(1, '1')
        check('a', "'a'")

    def test_match(self) -> None:
        def check(actual: Optional[a], expected: str) -> None:
            self.assertEqual(
                Maybe.of(actual).match(
                    lambda x: repr(x),
                    lambda: 'nothing'),
                expected)

        check(None, 'nothing')
        check(1, '1')
        check('a', "'a'")

    def test_flatmap(self) -> None:
        def check(actual: Optional[int], expected: Optional[int]) -> None:
            self.assertEqual(
                Maybe.of(actual).flatmap(
                    lambda x: Maybe.Value(x + 1)).py(),
                expected)

        check(None, None)
        check(1, 2)
        check(3, 4)

    def test_bind(self) -> None:
        def check(actual: Optional[int], expected: Optional[int]) -> None:
            self.assertEqual(
                (Maybe.of(actual) >> (lambda x: Maybe.Value(x + 1))).py(),
                expected)

        check(None, None)
        check(1, 2)
        check(3, 4)

    def test_or(self) -> None:
        def check(actual: Tuple[Optional[int], Optional[int]], expected: Optional[int]) -> None:
            maybe, other = actual
            self.assertEqual(
                (Maybe.of(maybe) | Maybe.of(other)).py(),
                expected)

        check((None, None), None)
        check((None, 0), 0)
        check((None, 42), 42)
        check((0, None), 0)
        check((42, None), 42)
        check((0, 42), 0)
        check((42, 0), 42)

    def test_else(self) -> None:
        def check(actual: Tuple[Optional[int], int], expected: int) -> None:
            maybe, other = actual
            self.assertEqual(Maybe.of(maybe).else_(other), expected)

        check((None, 0), 0)
        check((None, 42), 42)
        check((0, 42), 0)
        check((42, 0), 42)

    def test_filter(self) -> None:
        def check(actual: Tuple[Optional[int], bool], expected: Optional[int]) -> None:
            maybe, condition = actual
            self.assertEqual(
                Maybe.of(maybe).filter(lambda _: condition).py(),
                expected)

        check((None, True), None)
        check((0, True), 0)
        check((42, True), 42)
        check((None, False), None)
        check((0, False), None)
        check((42, False), None)

    def test_while(self) -> None:
        def check(actual: Optional[int], expected: List[int], until: int) -> None:
            self.assertEqual(
                while_(
                    Maybe.of(actual),
                    lambda x: x <= until,
                    lambda x: Maybe.Value(x + 1),
                ).py(),
                expected)

        check(None, [], until=2)
        check(0, [0, 1, 2], until=2)
        check(1, [1, 2], until=2)
        check(2, [2], until=2)
        check(3, [], until=2)
        check(0, list(range(long_test_len+1)), until=long_test_len)
