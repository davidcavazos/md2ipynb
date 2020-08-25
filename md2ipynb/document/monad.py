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
    TypeVar,
    Union,
)


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


# interface Monad<a> =
#   Value (x: a)
#   Nothing
#   flatmap (monad: Monad<a>, f: a -> Monad<b>): Monad<b>
@dataclass
class Monad(Generic[a]):
    @staticmethod
    def of(x: Any) -> Monad[a]:
        raise NotImplementedError('Monad.of')

    @staticmethod
    def Value(x: a) -> Monad[a]:
        raise NotImplementedError('Monad.Value')

    @staticmethod
    def Nothing() -> Monad[a]:
        raise NotImplementedError('Monad.Nothing')

    # def flatmap(self, f: Callable[[a], Monad[b]]) -> Monad[b]:
    #     raise NotImplementedError('Monad._flatmap')

    def py(self) -> Any:
        raise NotImplementedError('Monad.py')

    def __repr__(self) -> str:
        return repr(self.py())