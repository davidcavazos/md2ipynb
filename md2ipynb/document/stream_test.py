# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding coiterright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a coiter of the License at
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
    Callable,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
)

from . import stream
from .stream import Stream

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
b = TypeVar('b')


class StreamTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.warning(f"Setting the recursion limit to {recursion_limit}")
        sys.setrecursionlimit(recursion_limit)
        return super().setUpClass()

    def test_constructors(self) -> None:
        self.assertEqual(Stream.End(), Stream.End())

        def check(actual: Stream[int], expected: List[int]) -> None:
            self.assertEqual(list(actual.iter()), expected)

        check(Stream.End(), [])
        check(Stream.Next(1, lambda: Stream.End()), [1])
        check(
            Stream.Next(
                1, lambda: Stream.Next(
                    2, lambda: Stream.Next(
                        3, lambda: Stream.End()))),
            [1, 2, 3])
        self.assertNotEqual(Stream.End(), [1])
        self.assertNotEqual(Stream.Next(1, lambda: Stream.End()), [])

    def test_from_iterable(self) -> None:
        def check(actual: Iterable[int], expected: List[int]) -> None:
            self.assertEqual(list(Stream.of(actual).iter()), expected)

        check([], [])
        check([1], [1])
        check([1, 2, 3], [1, 2, 3])
        check(range(1, 4), [1, 2, 3])

        def generator() -> Iterable[int]:
            yield 1
            yield 2
            yield 3
        check(generator(), [1, 2, 3])

        check(range(long_test_len), list(range(long_test_len)))

    def test_to_string(self) -> None:
        def check(actual: Iterable[int], expected: str) -> None:
            self.assertEqual(str(Stream.of(actual)), expected)

        check([], '[]')
        check([1], '[1]')
        check([1, 2, 3], '[1, 2, 3]')
        check(list(range(long_test_len)), repr(list(range(long_test_len))))

    def test_match(self) -> None:
        def check(actual: Iterable[int], expected: str) -> None:
            self.assertEqual(Stream.of(actual).match(
                lambda: 'empty', lambda x, xs: f'{x} :: {xs()}'), expected)

        check([], 'empty')
        check([1], '1 :: []')
        check([1, 2, 3], '1 :: [2, 3]')
        check(range(long_test_len), f"0 :: {list(range(1, long_test_len))}")

    def test_join(self) -> None:
        def check(actual: Tuple[Iterable[int], Iterable[int]], expected: List[int]) -> None:
            items1, items2 = actual
            self.assertEqual(list(Stream.of(items1).join(
                lambda: Stream.of(items2)).iter()),
                expected)

        check(([], []), [])
        check(([], [1]), [1])
        check(([], [1, 2, 3]), [1, 2, 3])
        check(([1], []), [1])
        check(([1], [2]), [1, 2])
        check(([1], [2, 3, 4]), [1, 2, 3, 4])
        check(([1, 2, 3], []), [1, 2, 3])
        check(([1, 2, 3], [4]), [1, 2, 3, 4])
        check(([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6])
        check(([], range(long_test_len)),
              list(range(long_test_len)))
        check((range(long_test_len), []),
              list(range(long_test_len)))
        check((range(long_test_len), range(long_test_len)),
              list(range(long_test_len)) + list(range(long_test_len)))

    def test_fold(self) -> None:
        def check(items: Iterable[a], f: Callable[[a, Callable[[], a]], a], expected: Optional[a]) -> None:
            self.assertEqual(Stream.of(items).fold(f), expected)

        def add(x: int, y: Callable[[], int]) -> int:
            return x + y()
        check([], add, None)
        check([1], add, 1)
        check([1, 2, 3], add, 6)
        check(range(long_test_len), add, sum(range(long_test_len)))

        def sub(x: int, y: Callable[[], int]) -> int:
            return x - y()
        check([], sub, None)
        check([1], sub, 1)
        check([1, 2, 3], sub, -4)
        check(range(long_test_len), sub, -sum(range(long_test_len)))

        def check_join(nested_items: List[List[int]], expected: Optional[List[int]]) -> None:
            def join(x: Stream[int], y: Callable[[], Stream[int]]) -> Stream[int]:
                return x.join(y)
            items = [Stream.of(xs) for xs in nested_items]
            check(items, join, None if expected is None else Stream.of(expected))
        check_join([], None)
        check_join([[]], [])
        check_join([[], [], []], [])
        check_join([[1]], [1])
        check_join([[1], [], []], [1])
        check_join([[1], [2], [3]], [1, 2, 3])
        check_join([[1], [2, 3, 4]], [1, 2, 3, 4])
        check_join([[1, 2, 3]], [1, 2, 3])
        check_join([[1, 2, 3], []], [1, 2, 3])
        check_join([[1, 2, 3], [4], [5]], [1, 2, 3, 4, 5])

        empties: List[List[int]] = [[] for _ in range(long_test_len)]
        values = [[i] for i in range(long_test_len)] # [[0], [1], [2], ..]
        chain = list(range(long_test_len))           # [0, 1, 2, ..]
        ones_and_empties = [[1] if i % 2 == 0 else []  # [[1], [], [1], ..]
                            for i in range(long_test_len)]
        half_chain_of_ones = [1 for i in range(long_test_len // 2)] # [1, 1, ..]

        check_join(empties, [])
        check_join(values, chain)
        check_join(empties + [chain], chain)
        check_join([chain] + empties, chain)
        check_join(ones_and_empties, half_chain_of_ones)
        check_join([chain for _ in range(10)], chain * 10)

    def test_map(self) -> None:
        def check(actual: Iterable[int], expected: List[int]) -> None:
            self.assertEqual(list(Stream.of(actual).map(
                lambda x: x * 2).iter()),
                expected)

        check([], [])
        check([1], [2])
        check([1, 2, 3], [2, 4, 6])
        check(range(long_test_len), [x * 2 for x in range(long_test_len)])

    def test_flatten(self) -> None:
        def check(actual: Iterable[Iterable[int]], expected: List[int]) -> None:
            self.assertEqual(list(
                Stream.of(Stream.of(xs) for xs in actual).flatten().iter()),
                expected)

        check([], [])
        check([[], [1]], [1])
        check([[1], []], [1])
        check([[1], [2, 3, 4]], [1, 2, 3, 4])
        check([[1, 2, 3]], [1, 2, 3])
        check([[], [1, 2, 3]], [1, 2, 3])
        check([[1, 2, 3], []], [1, 2, 3])
        check([[1, 2, 3], [4]], [1, 2, 3, 4])
        check([[1, 2, 3], [4, 5, 6]], [1, 2, 3, 4, 5, 6])
        check([[], range(long_test_len)],
              list(range(long_test_len)))
        check([range(long_test_len), []],
              list(range(long_test_len)))
        check([range(long_test_len), range(long_test_len)],
              list(range(long_test_len)) + list(range(long_test_len)))
        check([[] for _ in range(long_test_len)], [])
        check([[1] for _ in range(long_test_len)],
              [1 for _ in range(long_test_len)])

    def test_flatmap(self) -> None:
        def check(actual: Tuple[Iterable[int], Callable[[int], Stream[int]]], expected: List[int]) -> None:
            items, f = actual
            self.assertEqual(list(Stream.of(items).flatmap(f).iter()), expected)

        _next: Callable[[int], Stream[int]] = lambda x: Stream.of([x, x * 2])
        check(([], _next), [])
        check(([1], _next), [1, 2])
        check(([1, 2, 3], _next), [1, 2, 2, 4, 3, 6])
        check((range(long_test_len), _next),
              [y for x in range(long_test_len) for y in [x, x * 2]])

        _end: Callable[[int], Stream[int]] = lambda _: Stream.End()
        check(([], _end), [])
        check(([1], _end), [])
        check(([1, 2, 3], _end), [])
        check((range(long_test_len), _end), [])

    def test_bind(self) -> None:
        def check(actual: Tuple[Iterable[int], Callable[[int], Stream[int]]], expected: List[int]) -> None:
            items, f = actual
            self.assertEqual(list((Stream.of(items) >> f).iter()), expected)

        _next: Callable[[int], Stream[int]] = lambda x: Stream.of([x, x * 2])
        check(([], _next), [])
        check(([1], _next), [1, 2])
        check(([1, 2, 3], _next), [1, 2, 2, 4, 3, 6])
        check((range(long_test_len), _next),
              [y for x in range(long_test_len) for y in [x, x * 2]])

        _end: Callable[[int], Stream[int]] = lambda _: Stream.End()
        check(([], _end), [])
        check(([1], _end), [])
        check(([1, 2, 3], _end), [])
        check((range(long_test_len), _end), [])


    def test_or(self) -> None:
        def check(actual: Tuple[Iterable[int], Iterable[int]], expected: List[int]) -> None:
            items1, items2 = actual
            self.assertEqual(
                list((Stream.of(items1) | Stream.of(items2)).iter()),
                expected)

        check(([], []), [])
        check(([], [1]), [1])
        check(([], [1, 2, 3]), [1, 2, 3])
        check(([1], []), [1])
        check(([1, 2, 3], []), [1, 2, 3])
        check(([1], [2]), [1])
        check(([1, 2, 3], [4, 5, 6]), [1, 2, 3])
        check((range(long_test_len), range(long_test_len)),
              list(range(long_test_len)))

    def test_filter(self) -> None:
        def check(actual: Tuple[Iterable[int], Set[int]], expected: List[int]) -> None:
            items, options = actual
            self.assertEqual(
                list(Stream.of(items).filter(lambda x: x in options).iter()),
                expected)

        check(([], set()), [])
        check(([1], set()), [])
        check(([1, 2, 3], set()), [])
        check(([], {3, 1}), [])
        check(([1], {3, 1}), [1])
        check(([1, 2, 3], {3, 1}), [1, 3])

    def test_while(self) -> None:
        def check(actual: Iterable[int], expected: List[int], until: int) -> None:
            self.assertEqual(
                list(Stream.of(actual).while_(lambda x: x <= until).iter()),
                expected)

        check([], [], until=2)
        check([0], [0], until=2)
        check([0, 1, 2, 3, 2], [0, 1, 2], until=2)
        check([3, 1, 2, 3, 2], [], until=2)
        check(range(long_test_len), list(range(long_test_len)),
              until=long_test_len)
