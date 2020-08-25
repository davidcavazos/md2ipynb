# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownershi The ASF licenses this file
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

from .parser import (Parser, State, SyntaxError)
from .result import Result

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
error = TypeVar('error')


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.warning(f"Setting the recursion limit to {recursion_limit}")
        sys.setrecursionlimit(recursion_limit)
        return super().setUpClass()

    def test_char(self) -> None:
        state = State('abc', 0, 1, 1, 'char')
        def check(ch: str, expected: Result[Tuple[str, State], error]) -> None:
            self.assertEqual(Parser.char(ch)._run(state), expected)

        check('a', Result.Ok(('a', state._with(position=1, col=2))))
        check('_', Result.Error(SyntaxError(
            "expected character '_', but got 'a'", state)))
        with self.assertRaises(ValueError):
            Parser.char('')
        with self.assertRaises(ValueError):
            Parser.char('abc')

    def test_pipe(self) -> None:
        def check(ch: str, expected: Result[a, error]) -> None:
            self.assertEqual(Parser.char(ch) >> )

    def test_parse(self) -> None:
        def check(ch: str, text: str, expected: Result[a, error]) -> None:
            self.assertEqual(Parser.char(ch).parse(text), expected)

        check('a', 'abc', Result.Ok('a'))
        check('_', 'abc', Result.Error(SyntaxError(
            "expected character '_', but got 'a'", State('abc', 0, 1, 1, ''))))
