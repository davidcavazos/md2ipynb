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

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
)

from .monad import Monad


a = TypeVar('a')
b = TypeVar('b')


@dataclass
class _Next(Generic[a]):
    def __init__(self, first: a, next: Callable[[], Stream[a]]) -> None:
        self._first = first
        self._next = next

    def first(self) -> a:
        return self._first

    def next(self) -> Callable[[], Stream[a]]:
        return self._next


@dataclass
class _End:
    pass


# type Stream<a> as ...
# type [a] =
#   :: (first: a, next: a..)
#   []
@dataclass
class Stream(Generic[a]):
    _data: Union[_Next[a], _End]

    @staticmethod
    def of(iterable: Iterable[a]) -> Stream[a]:
        it = iter(iterable)
        try:
            x = next(it)
            return Stream.Next(x, lambda: Stream.of(it))
        except StopIteration:
            return Stream.End()

    @staticmethod
    def Next(first: a, next: Callable[[], Stream[a]]) -> Stream[a]:
        return Stream(_Next(first, next))

    @staticmethod
    def End() -> Stream[a]:
        return Stream(_End())

    def copy(self) -> Stream[a]:
        return self.match(
            lambda: Stream.End(),
            lambda x, xs: Stream.Next(x, xs))

    def iter(self) -> Iterable[a]:
        xs = self
        while isinstance(s := xs._data, _Next):
            x = s.first()
            yield x
            xs = s.next()()

    def __repr__(self) -> str:
        return repr(list(self.iter()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stream):
            return NotImplemented
        # return repr(self) == repr(other)
        xs, ys = self._data, other._data
        while True:
            if isinstance(xs, _End) and isinstance(ys, _End):
                return True
            if isinstance(xs, _Next) and isinstance(ys, _Next):
                if xs.first() != ys.first():
                    return False
                xs, ys = xs.next()()._data, ys.next()()._data
                continue
            return False
        return True

    #===--- Syntax sugar ---===#

    # match stream
    #   case [] -> on_end
    #   case x :: xs -> on_next (x, xs)
    def match(self, on_end: Callable[[], b], on_next: Callable[[a, Callable[[], Stream[a]]], b]) -> b:
        s = self._data
        if isinstance(s, _Next):
            return on_next(s.first(), s.next())
        assert isinstance(s, _End)
        return on_end()

    #===--- Interface methods (have return type, must be implemented) ---===#

    #===--- General methods (must only access interface methods) ---===#

    # join (prefix: [a], postfix: [a]): [a] ->
    #   match prefix
    #     case [] -> postfix
    #     case x :: xs -> x :: xs .join postfix
    def join(self, postfix: Callable[[], Stream[a]]) -> Stream[a]:
        return self.match(
            lambda: postfix(),
            lambda x, xs: Stream.Next(x, lambda: xs().join(postfix)))

    # match stream
    #   case [] -> on_end
    #   case x :: xs -> on_next x xs
    def match_rec(self, on_end: Callable[[], b], on_next: Callable[[a, Callable[[], Stream[a]]], b]) -> b:
        s = self._data
        if isinstance(s, _Next):
            return on_next(s.first(), s.next())
        assert isinstance(s, _End)
        return on_end()

    # fold (stream: [a], f: a, a -> a): a? ->
    #   match stream
    #     case [] -> Nothing
    #     case x :: [] -> x
    #     case x :: xs -> f x (xs .fold f)
    def fold(self, f: Callable[[a, Callable[[], a]], a]) -> Optional[a]:
        # case [] -> Nothing
        if isinstance(self._data, _End):
            return None

        # case x :: _ -> a
        def _fold1(stream: Stream[a], f: Callable[[a, Callable[[], a]], a]) -> a:
            assert isinstance(stream._data, _Next)
            x, xs = stream._data.first(), stream._data.next()()

            # case x :: [] -> x
            if isinstance(xs._data, _End):
                return x
            result = x

            # case x :: xs -> f x, (xs .fold f)
            while isinstance(s := xs._data, _Next):
                # If `result` is a recursive type like Stream.Next,
                # return a lazy recursion.
                if isinstance(result, Stream) and isinstance(result._data, _Next):
                    return f(result, lambda: _fold1(xs, f)) # type: ignore
                # Otherwise, do an eager loop.
                result = f(result, lambda: s.first())
                xs = s.next()()
            return result

        return _fold1(self, f)

    # (stream: [a]) .map (f: a -> b): [b] ->
    #   match stream
    #     case [] -> []
    #     case x :: xs -> f x :: xs .map f
    def map(self: Stream[a], f: Callable[[a], b]) -> Stream[b]:
        return self.match(
            lambda: Stream.End(),
            lambda x, xs: Stream.Next(f(x), lambda: xs().map(f)))

    # (stream: [[a]]) .flatten: [a] ->
    #   stream .fold [], (xs, ys -> xs .join ys)
    def flatten(self: Stream[Stream[b]]) -> Stream[b]:
        return self.fold(lambda xs, ys: xs.join(ys)) or Stream.End()

    # (stream: [a]) .flatmap (f: a -> [b]): [b] ->
    #   stream .map f .flatten
    def flatmap(self, f: Callable[[a], Stream[b]]) -> Stream[b]:
        return self.map(f).flatten()

    def __rshift__(self, f: Callable[[a], Stream[b]]) -> Stream[b]:
        return self.flatmap(f)

    # (left: [a]) .or (right: [a]): [a] ->
    #   match stream1
    #     case [] -> right
    #     case x :: xs -> left
    def __or__(self, other: Stream[a]) -> Stream[a]:
        return self.match(
            lambda: other,
            lambda x, xs: Stream.Next(x, xs))

    # (stream: [a]) .filter (condition: a -> Bool): [a] ->
    #   stream .flatmap (x -> if (condition x) .then [x] .else [])
    def filter(self, condition: Callable[[a], bool]) -> Stream[a]:
        return self.flatmap(lambda x:
            Stream.Next(x, lambda: Stream.End())
            if condition(x) else Stream.End())

    # (stream: [a]) .while (condition: a -> Bool): [a] ->
    #   match stream
    #     case [] -> []
    #     case x :: xs ->
    #       if (condition x) .then (x :: xs .while condition) .else []
    def while_(self, condition: Callable[[a], bool]) -> Stream[a]:
        return self.match(
            lambda: Stream.End(),
            lambda x, xs:
                Stream.Next(x, lambda: xs().while_(condition))
                if condition(x) else Stream.End())

    # type Qunatifier =
    #   Exactly (count: UInteger)
    #   AtLeast (min: UInteger)
    #   AtMost (max: UInteger)
    #   Between (min: UInteger, max: UInteger) where min <= max

    # (stream: [a]) .take (quantifier: Quantifier): [a]? ->
    #   match stream, quantifier
    #     case _, Exactly n -> stream .take (Exactly n)
    #     case [], AtLeast n -> if n == 0 .then [] .else Nothing
    #     case x :: xs, AtLeast n ->
    #       if n >= 1 .then x :: xs .take (AtLeast (n - 1)) .else Nothing
    #     case [], AtMost n -> []
    #     case x :: xs, AtMost n ->
    #       if 
    #     case _, Between (n, m) ->
    #       for first in stream .take (AtLeast n)
    #       for rest in 

    # (stream: [a]) .trim (quantifier: Quantifier)

    # (stream: [a]) .split (condition: a -> Bool): [a], [a] ->
    #   stream .fold (
    #     [], []
    #     (left, right), x ->
    #       if (condition x) .then
    #         left ++ [x], right
    #       .else
    #         left, x :: right
    #   )

    #   match stream
    #     case []      = [], []
    #     case x :: xs =
    #       if (condition x) .then
    #         ys, zs = xs .split condition
    #         x :: ys, zs
    #       .else
    #         [], stream

    # (stream: [a]) .take (count: UInteger): [a]? ->
    #   match count, stream
    #     case 0, _       = []
    #     case n, x :: xs = x :: xs .take (n - 1)

    # (stream: [a]) .take_at_least (min_count: UInteger): [a]? ->
    #   match min_count, stream
    #     case 0, _       = stream
    #     case 1, x :: xs = stream
    #     case n, x :: xs = x :: xs .take_at_least (n - 1)

    # (stream: [a]) .take_at_most (max_count: UInteger): [a] ->
    #   match max_count, stream
    #     case 0, _       = []
    #     case n, []      = []
    #     case n, x :: xs = x :: xs .take_at_most (n - 1)

    # (stream: [a]) .take_between (min: UInteger, max: UInteger): [a] ->
    #     where min <= max =
    #   
