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

from .quantifier import Quantifier
from .stream import Stream


a = TypeVar('a')
b = TypeVar('b')

# type Parser<a> =
#   Parser (parse: Text -> (a, Text)?)
@dataclass
class Parser(Generic[a]):
    def __init__(self, parse: Callable[[str], Optional[Tuple[a, str]]]) -> None:
        self.parse = parse

    # ParserValue (x: a) ->
    #   Parser (text -> (x, text))
    @staticmethod
    def Value(x: a) -> Parser[a]:
        return Parser(lambda text: (x, text))

    # ParserError ->
    #   Parser (_ -> Nothing)
    @staticmethod
    def Error() -> Parser[Any]:
        return Parser(lambda _: None)

    #--- regex: r'(p1)|(p2)'
    # (p1: Parser<a>) | (p2: Parser<a>): Parser<a> ->
    #   Parser (text -> match p1 text
    #     case x, rest -> x, rest
    #     case Nothing -> p2 text
    #   )
    def __or__(self, other: Parser[a]) -> Parser[a]:
        def parser_fn(text: str) -> Optional[Tuple[a, str]]:
            output = self.parse(text)
            return output if output is not None else other.parse(text)
        return Parser(parser_fn)

    # (parser: Parser<a>) flatmap (f: a -> Parser<b>): Parser<b> ->
    #   Parser (text ->
    #     match parser .parse text
    #       case x, rest -> (f x) .parse rest
    #       case Nothing -> Nothing
    #   )
    def flatmap(self, f: Callable[[a], Parser[b]]) -> Parser[b]:
        def parse(text: str) -> Optional[Tuple[b, str]]:
            output = self.parse(text)
            if output is not None:
                x, rest = output
                return f(x).parse(rest)
            return None
        return Parser(parse)

    # (parser: Parser<a>) >> (f: a -> Parser<b>): Parser<b> ->
    #   parser flatmap f
    def __rshift__(self, f: Callable[[a], Parser[b]]) -> Parser[b]:
        return self.flatmap(f)

    # (parser: Parser<a>) if (condition: a -> Bool) ->
    #   for item in parser
    #   join if condition item then Parser.Value item else Parser.Error
    def if_(self, condition: Callable[[a], bool]) -> Parser[a]:
        return (
            self >> (lambda item:
            Parser.Value(item) if condition(item) else Parser.Error())
        )

    # while (stream: a.., condition: a -> Boolean): a.. ->
    #   match steam
    #     case x :: xs ->
    #       (condition x) .then (x :: xs .while condition) .else ..
    #     case _ -> ..

    # :: (head: a, tail: Parser<a>): Parser<a> -> ...
    # :: (parser: Parser<a>): (a, Parser<a>)? ->
    #   for x in parser
    #   as x, parser
    #   or Nothing

    # while (parser: Parser<a>, condition: a -> Boolean): Parser<[a]> ->
    #   parser .while condition

    # while (parser: Parser<a>, condition: a -> Boolean): Parser<[a]> ->
    #   for x in parser if condition x
    #   for xs in parser .while condition
    #   as Token (x :: xs)
    #   or Token []
    def repeat_while(self, condition: Callable[[a], bool]) -> Parser[List[a]]:
        def parse(text: str) -> Optional[Tuple[List[a], str]]:
            # Optimization: Python does not support tail call optimizations, so
            #   recursion is not a good option. We'll use iteration instead.
            # Fix: Create a @tail_call decorator for tail call optimization.
            xs: List[a] = []
            rest = text
            while output := self.parse(text):
                x, text = output
                if not condition(x):
                    break
                rest = text
                xs += [x]
            return xs, rest
        return Parser(parse)

    # (parser: Parser<Text>) text_while (condition: Char -> Bool): Parser<Text> ->
    #   for texts in parser while condition
    #   join Parser.Value (texts join)
    def text_while(self: Parser[str], condition: Callable[[str], bool]) -> Parser[str]:
        return (
            self.repeat_while(condition) >> (lambda texts:
            Parser.Value(''.join(texts))))

    @overload
    def until_delimiter(self, delimiter: a) -> Parser[List[a]]: ...

    @overload
    def until_delimiter(self, delimiter: Callable[[a], bool]) -> Parser[List[a]]: ...

    def until_delimiter(self, delimiter: Union[a, Callable[[a], bool]]) -> Parser[List[a]]:
        # (parser: Parser<a>) until_delimiter (is_delimiter: a -> Bool): Parser<[a]> ->
        #   for xs in parser while x -> not (is_delimiter x)
        #   for _ in parser if x -> is_delimiter x
        #   join Parser.Value xs
        if callable(delimiter):
            is_delimiter: Callable[[a], bool] = delimiter # makes mypy happy
            return (
                self.repeat_while(lambda x: not is_delimiter(x)) >> (lambda xs:
                self.if_(lambda x: is_delimiter(x)) >> (lambda _:
                Parser.Value(xs))))

        # (parser: Parser<a>) until_delimiter (delimiter: a): Parser<[a]> ->
        #   parser until_delimiter x -> x == delimiter
        return self.until_delimiter(lambda x: x == delimiter)

    @overload
    def text_until_delimiter(self: Parser[str], delimiter: str) -> Parser[str]: ...

    @overload
    def text_until_delimiter(self: Parser[str], delimiter: Callable[[str], bool]) -> Parser[str]: ...

    def text_until_delimiter(self: Parser[str], delimiter: Union[str, Callable[[str], bool]]) -> Parser[str]:
        # (parser: Parser<Text>) text_until_delimiter (is_delimiter: a -> Bool): Parser<Text> ->
        #   for texts in parser until_delimiter is_delimiter
        #   join Parser.Value (texts join)
        if callable(delimiter):
            is_delimiter: Callable[[str], bool] = delimiter # makes mypy happy
            return (
                self.until_delimiter(is_delimiter) >> (lambda texts:
                Parser.Value(''.join(texts))))

        # (parser: Parser<Text>) text_until_delimiter (delimiter: a): Parser<Text> ->
        #   for texts in parser until_delimiter delimiter
        #   join Parser.Value (texts join)
        return (
            self.until_delimiter(delimiter) >> (lambda texts:
            Parser.Value(''.join(texts))))

    @overload
    def until_maybe_delimiter(self, delimiter: a) -> Parser[List[a]]: ...

    @overload
    def until_maybe_delimiter(self, delimiter: Callable[[a], bool]) -> Parser[List[a]]: ...

    def until_maybe_delimiter(self, delimiter: Union[a, Callable[[a], bool]]) -> Parser[List[a]]:
        # (parser: Parser<a>) until_maybe_delimiter (is_delimiter: a -> Bool): Parser<[a]> ->
        #   for xs in parser while x -> not (is_delimiter x)
        #   for _ in zero_or_one (parser if x -> is_delimiter x)
        #   join Parser.Value xs
        if callable(delimiter):
            is_delimiter: Callable[[a], bool] = delimiter # makes mypy happy
            return (
                self.repeat_while(lambda x: not is_delimiter(x)) >> (lambda xs:
                zero_or_one(self.if_(lambda x: is_delimiter(x))) >> (lambda _:
                Parser.Value(xs))))

        # (parser: Parser<a>) until_maybe_delimiter (delimiter: a): Parser<[a]> ->
        #   parser until_maybe_delimiter x -> x == delimiter
        return self.until_maybe_delimiter(lambda x: x == delimiter)

    @overload
    def text_until_maybe_delimiter(self: Parser[str], delimiter: str) -> Parser[str]: ...

    @overload
    def text_until_maybe_delimiter(self: Parser[str], delimiter: Callable[[str], bool]) -> Parser[str]: ...

    def text_until_maybe_delimiter(self: Parser[str], delimiter: Union[str, Callable[[str], bool]]) -> Parser[str]:
        # (parser: Parser<Text>) text_until_maybe_delimiter (is_delimiter: a -> Bool): Parser<Text> ->
        #   for texts in parser until_maybe_delimiter is_delimiter
        #   join Parser.Value (texts join)
        if callable(delimiter):
            is_delimiter: Callable[[str], bool] = delimiter # makes mypy happy
            return (
                self.until_maybe_delimiter(is_delimiter) >> (lambda texts:
                Parser.Value(''.join(texts))))

        # (parser: Parser<Text>) text_until_maybe_delimiter (delimiter: a): Parser<Text> ->
        #   for texts in parser until_maybe_delimiter delimiter
        #   join Parser.Value (texts join)
        return (
            self.until_maybe_delimiter(delimiter) >> (lambda texts:
            Parser.Value(''.join(texts))))


#--- regex: r'(parser)?'
# zero_or_one (parser: Parser<a>): Parser<[a]> ->
#   for x in parser
#   join Parser.Value ([x])
#   | Parser.Value ([])
def zero_or_one(parser: Parser[a]) -> Parser[List[a]]:
    return (
        parser >> (lambda x:
        Parser.Value([x]))
        | Parser.Value([]))


# text_zero_or_one (parser: Parser<Text>): Parser<Text> ->
#   for texts in zero_or_one parser
#   join Parser.Value (texts join)
def text_zero_or_one(parser: Parser[str]) -> Parser[str]:
    return (
        zero_or_one(parser) >> (lambda texts:
        Parser.Value(''.join(texts))))


#--- regex: r'(parser)*'
# zero_or_more (parser: Parser<a>): Parser<[a]> ->
#   parser while (_ -> True)
def zero_or_more(parser: Parser[a]) -> Parser[List[a]]:
    return parser.repeat_while(lambda _: True)


# text_zero_or_more (parser: Parser<Text>): Parser<Text> ->
#   for texts in zero_or_more parser
#   join Parser.Value (texts join)
def text_zero_or_more(parser: Parser[str]) -> Parser[str]:
    return (
        zero_or_more(parser) >> (lambda texts:
        Parser.Value(''.join(texts))))


#--- regex: r'(parser)+'
# one_or_more (parser: Parser<a>): Parser<[a]> ->
#   for x in parser
#   for xs in zero_or_more parser
#   join Parser.Value (x :: xs)
def one_or_more(parser: Parser[a]) -> Parser[List[a]]:
    return (
        parser >> (lambda x:
        zero_or_more(parser) >> (lambda xs:
        Parser.Value([x] + xs)))
    )


# text_one_or_more (parser: Parser<Text>): Parser<Text> ->
#   for texts in one_or_more parser
#   join Parser.Value (texts join)
def text_one_or_more(parser: Parser[str]) -> Parser[str]:
    return (
        one_or_more(parser) >> (lambda chars:
        Parser.Value(''.join(chars))))


#--- regex: r'(parser){,max}'
# at_most (max: Integer if max >= 0, parser: Parser<a>): Parser<[a]> ->
#   for x in parser
#   for xs in at_most (max - 1, parser)
#   join Parser.Value (x :: xs)
#   | Parser.Value ([])
def at_most(max: int, parser: Parser[a]) -> Parser[List[a]]:
    # Optimization: Python does not support tail call optimizations, so
    #   recursion is not a good option. We'll use iteration instead.
    # Fix: Create a @tail_call decorator for tail call optimization.
    if max < 0:
        raise ValueError(f"`max` must be non-negative: max={max}")
    def parse(text: str) -> Optional[Tuple[List[a], str]]:
        xs: List[a] = []
        rest = text
        for _ in range(max):
            output = parser.parse(rest)
            if output is None:
                break
            x, rest = output
            xs += [x]
        return xs, rest
    return Parser(parse)


# text_at_most (max: Integer if max >= 0, parser: Parser<Text>): Parser<Text> ->
#   for texts in at_most (max, parser)
#   join Parser.Value (texts join)
def text_at_most(max: int, parser: Parser[str]) -> Parser[str]:
    return (
        at_most(max, parser) >> (lambda texts:
        Parser.Value(''.join(texts))))


#--- regex: r'(parser){count}'
# exactly (count: Integer if count >= 0, parser: Parser<a>): Parser<[a]> ->
#   for xs in at_most (count, parser)
#   join if xs length == count then Parser.Value xs else Nothing
def exactly(count: int, parser: Parser[a]) -> Parser[List[a]]:
    if count < 0:
        raise ValueError(f"`count` must be non-negative: count={count}")
    return (
        at_most(count, parser) >> (lambda xs:
        Parser.Value(xs) if len(xs) == count else Parser.Error())
    )


# text_exactly (count: Integer if count >= 0, parser: Parser<Text>): Parser<Text> ->
#   for texts in exactly (count, parser)
#   join Parser.Value (texts join)
def text_exactly(count: int, parser: Parser[str]) -> Parser[str]:
    return (
        exactly(count, parser) >> (lambda texts:
        Parser.Value(''.join(texts))))


#--- regex: r'(parser){min,}'
# at_least (min: Integer if min >= 0, parser: Parser<a>): Parser<[a]> ->
#   for first_xs in exactly (min, parser)
#   for xs in zero_or_more parser
#   join Parser.Value (first_xs ++ xs)
def at_least(min: int, parser: Parser[a]) -> Parser[List[a]]:
    if min < 0:
        raise ValueError(f"`min` must be non-negative: min={min}")
    return (
        exactly(min, parser) >> (lambda first_xs:
        zero_or_more(parser) >> (lambda xs:
        Parser.Value(first_xs + xs)))
    )


# text_at_least (min: Integer if min >= 0, parser: Parser<a>): Parser<[a]> ->
#   for texts in exactly (count, parser)
#   join Parser.Value (texts join)
def text_at_least(min: int, parser: Parser[str]) -> Parser[str]:
    return (
        at_least(min, parser) >> (lambda texts:
        Parser.Value(''.join(texts))))


#--- regex: r'(parser){min,max}'
# between (
#   min: Integer if min >= 0
#   max: Integer if max >= min
#   parser: Parser<a>
# ): Parser<[a]> ->
#   for first_xs in exactly (min, parser)
#   for xs in at_most (max - min, parser)
#   join value (first_xs ++ xs)
def between(min: int, max: int, parser: Parser[a]) -> Parser[List[a]]:
    if min < 0:
        raise ValueError(f"`min` must be non-negative: min={min}")
    if max < min:
        raise ValueError(f"`min` must be less or equal to `max`: min={min}, max={max}")
    return (
        exactly(min, parser) >> (lambda first_xs:
        at_most(max - min, parser) >> (lambda xs:
        Parser.Value(first_xs + xs)))
    )


# text_between (
#   min: Integer if min >= 0
#   max: Integer if max >= min
#   parser: Parser<Text>
# ): Parser<Text> ->
#   for texts in between (min, max, parser)
#   join Parser.Value (texts join)
def text_between(min: int, max: int, parser: Parser[str]) -> Parser[str]:
    return (
        between(min, max, parser) >> (lambda texts:
        Parser.Value(''.join(texts))))


#--- regex: r'.'
# any_char -> Parser(text -> match text
#   case '' -> Nothing
#   case (char :: tail) -> char, tail
# )
def any_char() -> Parser[str]:
    return Parser(lambda text: (text[0], text[1:]) if text else None)


@overload
def char(ch: str) -> Parser[str]: ...

@overload
def char(ch: Iterable[str]) -> Parser[str]: ...

def char(ch: Union[str, Iterable[str]]) -> Parser[str]:
    #--- regex: r'c'
    # char (ch: Char): Parser<Char> ->
    #   any_char if (== ch)
    if type(ch) is str:
        return any_char().if_(lambda c: c == ch)

    #--- regex: r'[chars]'
    # char (chars: {Char}): Parser<Char> ->
    #   any_char if (in chars)
    chars = ch if type(ch) is set else set(ch)
    return any_char().if_(lambda c: c in chars)


@overload
def char_not(ch: str) -> Parser[str]: ...

@overload
def char_not(ch: Iterable[str]) -> Parser[str]: ...

def char_not(ch: Union[str, Iterable[str]]) -> Parser[str]:
    #--- regex: r'[^c]'
    # char_not (ch: Char): Parser<Char> ->
    #   any_char if (!= ch)
    if type(ch) is str:
        return any_char().if_(lambda c: c != ch)

    #--- regex: r'[^chars]'
    # char_not (chars: {Char}): Parser<Char> ->
    #   any_char if (not_in chars)
    chars = ch if type(ch) is set else set(ch)
    return any_char().if_(lambda c: c not in chars)


#--- regex: r'[0-9]'
# digit ->
#   any_char if is_digit
def digit() -> Parser[str]:
    return any_char().if_(str.isdigit)


#--- regex: r'[a-zA-Z]'
# letter ->
#   any_char if is_letter
def letter() -> Parser[str]:
    return any_char().if_(str.isalpha)


#--- regex: r'[a-z]'
# lowercase ->
#   any_char if is_lowercase
def lowercase() -> Parser[str]:
    return any_char().if_(str.islower)


#--- regex: r'[A-Z]'
# uppercase ->
#   any_char if is_uppercase
def uppercase() -> Parser[str]:
    return any_char().if_(str.isupper)


#--- regex: r'[a-zA-Z0-9]'
# alphanumeric ->
#   any_char if is_alphanumeric
def alphanumeric() -> Parser[str]:
    return any_char().if_(str.isalnum)


#--- regex: r'[ \t\n\r\x0b\f]'
# space ->
#   any_char if is_space
def space() -> Parser[str]:
    return any_char().if_(str.isspace)


#--- regex: r'    | {,3}\t'
# indent (spaces_per_tab = 4) ->
#   for chars in
#     exactly (spaces_per_tab, char ' ')
#     | for spaces in at_most (spaces_per_tab - 1, char ' ')
#     for tab in char '\t'
#     join Parser.Value (spaces ++ [tab])
#   join Parser.Value (chars join)
def indent(spaces_per_tab: int = 4) -> Parser[str]:
    return (
        exactly(spaces_per_tab, char(' '))
        | at_most(spaces_per_tab - 1, char(' ')) >> (lambda spaces:
        char('\t') >> (lambda tab:
        Parser.Value(spaces + [tab])))
    ) >> (lambda chars:
    Parser.Value(''.join(chars)))


# def repeat(parser: Parser[a], quantifier: Quantifier) -> Parser[List[a]]:
#     pass

# def text(parser: Parser[str], quantifier: Quantifier) -> Parser[str]:
#     pass
