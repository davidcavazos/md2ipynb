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

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from .monad import Monad


a = TypeVar('a')
b = TypeVar('b')


@dataclass
class _Value(Generic[a]):
    _value: a

    def value(self) -> a:
        return self._value


@dataclass
class _Nothing:
    pass


# type Maybe<a> as Monad<a> =
#   Value (x: a)
#   Nothing
@dataclass(repr=False)
class Maybe(Monad[a]):
    #===--- Interface constructors (no return type, default type) ---===#
    _maybe: Union[_Value[a], _Nothing]

    @staticmethod
    def of(value: Optional[a]) -> Maybe[a]:
        return Maybe(_Value(value) if value is not None else _Nothing())

    @staticmethod
    def Value(x: a) -> Maybe[a]:
        return Maybe(_Value(x)) 

    @staticmethod
    def Nothing() -> Maybe[a]:
        return Maybe(_Nothing())

    def py(self) -> Optional[a]:
        return self._maybe.value() if isinstance(self._maybe, _Value) else None

    #===--- Syntax sugar ---===#

    # match maybe
    #   case Value x -> on_value x
    #   case Nothing -> on_nothing
    def match(self, on_value: Callable[[a], b], on_nothing: Callable[[], b]) -> b:
        if isinstance(self._maybe, _Value):
            return on_value(self._maybe.value())
        assert isinstance(self._maybe, _Nothing)
        return on_nothing()

    #===--- Interface methods (have return type, must be implemented) ---===#

    # flatmap (maybe: a?, f: a -> b?): b? ->
    #   match maybe
    #     case Value x -> f x
    #     case Nothing -> Nothing
    def flatmap(self, f: Callable[[a], Maybe[b]]) -> Maybe[b]:
        if isinstance(self._maybe, _Value):
            return f(self._maybe.value())
        assert isinstance(self._maybe, _Nothing)
        return Maybe.Nothing()

    def __rshift__(self, f: Callable[[a], Maybe[b]]) -> Maybe[b]:
        return self.flatmap(f)

    #===--- General methods (must only access interface methods) ---===#

    # or (maybe1: a?, Maybe2: a?): a? ->
    #   match maybe
    #     case Value x -> maybe1
    #     case Nothing -> maybe2
    def __or__(self, other: Maybe[a]) -> Maybe[a]:
        return self.match(
            lambda x: Maybe.Value(x),
            lambda: other)

    # else (maybe: a?, other: a): a ->
    #   match maybe
    #     case Value x -> x
    #     Nothing -> other
    def else_(self, other: a) -> a:
        return self.match(lambda x: x, lambda: other)

    # filter (maybe: a?, condition: a -> Boolean): a? ->
    #   maybe .flatmap (x -> if (condition x) .then (Value x) .else Nothing)
    def filter(self, condition: Callable[[a], bool]) -> Maybe[a]:
        return self.flatmap(
            lambda x: Maybe.Value(x) if condition(x) else Maybe.Nothing())


@dataclass
class _Next(Generic[a]):
    def __init__(self, first: a, next: Callable[[], Stream[a]]) -> None:
        self._first = first
        self._next = next

    def first(self) -> a:
        return self._first

    def next(self) -> Stream[a]:
        return self._next()


@dataclass
class _End:
    pass


# type Stream<a> as Maybe<(first: a, next: Stream<a>)> =
#   :: (first: a, next: Stream<a>)
#   End
@dataclass
class Stream(Monad[_Next[a]]):
    _stream: Union[_Next[a], _End]

    @overload
    def __init__(self, stream: Union[_Next[a], _End]) -> None: ...

    @overload
    def __init__(self, stream: Iterable[a]) -> None: ...

    def __init__(self, stream: Union[_Next[a], _End, Iterable[a]]) -> None:
        self._maybe = _Nothing()
        if isinstance(stream, (_Next, _End)):
            self._stream = stream
        else:
            it = iter(stream)
            try:
                x = next(it)
                self._stream = _Next(x, lambda: Stream(it))
            except StopIteration:
                self._stream = _End()

    @staticmethod
    def End() -> Stream[a]:
        return Stream(_End())

    @staticmethod
    def Next(first: a, next: Callable[[], Stream[a]]) -> Stream[a]:
        return Stream(_Next(first, next))

    def py(self) -> List[a]:
        result: List[a] = []
        xs = self
        while isinstance(xs._stream, _Next):
            x, xs = xs._stream.first(), xs._stream.next()
            result += [x]
        return result

    #===--- Syntax sugar ---===#

    # match maybe
    #   case x :: xs -> on_next (x, xs)
    #   case .. -> on_end
    def match_stream(self,
              on_next: Callable[[a, Stream[a]], b],
              on_end: Callable[[], b]) -> b:
        if isinstance(self._stream, _Next):
            return on_next(self._stream.first(), self._stream.next())
        assert isinstance(self._stream, _End)
        return on_end()

    # while (stream: a.., condition: a -> Boolean): a.. ->
    #   match stream
    #     case x :: xs ->
    #       if (condition x)
    #       .then (x :: xs .while condition)
    #       .else ..
    #     case .. -> ..
    def while_(self, condition: Callable[[a], bool]) -> Stream[a]:
        return self.match_stream(
            lambda x, xs:
                Stream.Next(x, lambda: xs.while_(condition))
                if condition(x) else Stream.End(),
            lambda: Stream.End())


# while (maybe: a?, condition: a -> Boolean, next: a -> a?): a.. ->
#   match maybe
#     case Value x ->
#       if (condition x) .then (x :: (next x) .while (condition, next)) .else ..
#     case Nothing -> ..
def while_(first: Maybe[a], condition: Callable[[a], bool], next: Callable[[a], Maybe[a]]) -> Stream[a]:
    return first.match(
        lambda x:
            Stream.Next(x, lambda: while_(next(x), condition, next))
            if condition(x) else Stream.End(),
        lambda: Stream.End())
