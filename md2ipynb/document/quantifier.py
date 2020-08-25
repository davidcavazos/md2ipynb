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

from dataclasses import dataclass
from typing import (
    Generic,
    TypeVar,
)

a = TypeVar('a')

# type Quantifier<a> =
#   Quantifier (take: Stream<a> -> (Stream<a>, Stream<a>))
@dataclass
class Quantifier(Generic[a]):
    pass

# all ->
#   Quantifier >> stream -> (stream, [..])

# at_least (min: UInteger) ->

# at_most (max: UInteger) ->

# between (min: UInteger, max: UInteger if min <= max) ->
#   for first_xs in at_least min
#   for last_xs in at_most (max - min)
#   do first_xs :: last_xs

# exactly (count: UInteger) ->
#   between (count, count)

#   match count
#     case 0 -> Quantifier >> stream -> ([..], stream)
#     case _ -> Quantifier >> stream ->
#       match stream
#         case [..] -> ([..], [..])
#         case x :: xs -> (x :: exactly (count - 1), xs)

# while (condition: a -> Boolean)
# until_delimiter (delimiter: a -> Boolean)
# until_delimiter (delimiter: a)