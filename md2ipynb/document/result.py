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
from typing import *

a = TypeVar('a')
b = TypeVar('b')
error = TypeVar('error')


@dataclass
class Result(Generic[a, error]):
    @staticmethod
    def Ok(x: a) -> Result[a, error]:
        return _Ok(x)

    @staticmethod
    def Error(e: error) -> Result[a, error]:
        return _Error(e)

    def match(self, on_value: Callable[[a], b], on_error: Callable[[error], b]) -> b:
        if isinstance(self, _Ok):
            return on_value(self.x)
        assert isinstance(self, _Error)
        return on_error(self.e)

    def map(self, f: Callable[[a], b]) -> Result[b, error]:
        ''' map : (a -> b) (Result a error) -> Result b error
            map f (Ok x) = Ok (f x)
            map _ (Error e) = Error e '''
        return self.match(
            lambda x: Result.Ok(f(x)),
            lambda e: Result.Error(e))


@dataclass
class _Ok(Result[a, error]):
    x: a


@dataclass
class _Error(Result[a, error]):
    e: error
