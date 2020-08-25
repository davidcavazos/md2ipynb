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
c = TypeVar('c')
error = TypeVar('error')


class ResultTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.warning(f"Setting the recursion limit to {recursion_limit}")
        sys.setrecursionlimit(recursion_limit)
        return super().setUpClass()

    def test_constructors(self) -> None:
        self.assertEqual(Result.Ok(42), Result.Ok(42))
        self.assertNotEqual(Result.Ok(42), Result.Ok(0))
        self.assertEqual(Result.Ok('hello'), Result.Ok('hello'))

        self.assertEqual(Result.Error(42), Result.Error(42))
        self.assertNotEqual(Result.Error(42), Result.Error(0))
        self.assertEqual(Result.Error('hello'), Result.Error('hello'))

        self.assertNotEqual(Result.Ok(42), Result.Error(42))

    def test_match(self) -> None:
        def check(actual: Result[a, error], expected: str) -> None:
            self.assertEqual(
                actual.match(
                    lambda value: f"value: {value}",
                    lambda error: f"error: {error}"),
                expected)
        check(Result.Ok(42), 'value: 42')
        check(Result.Ok('hello'), 'value: hello')
        check(Result.Error(42), 'error: 42')
        check(Result.Error('hello'), 'error: hello')

    def test_map(self) -> None:
        def check(actual: Result[a, error], f: Callable[[a], b], expected: Result[b, error]) -> None:
            self.assertEqual(actual.map(f), expected)
        check(Result.Ok(2), lambda x: x * 2, Result.Ok(4))
        check(Result.Ok('hello'), str.upper, Result.Ok('HELLO'))
        check(Result.Error(42), lambda _: _, Result.Error(42)) # type: ignore
