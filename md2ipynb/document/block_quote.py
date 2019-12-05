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

import re
from dataclasses import dataclass, field
from typing import List

from .block import Block

_block_quote_re = re.compile(r' {0,3}> ?')


@dataclass
class BlockQuote(Block):
    items: List[Block] = field(default_factory=list)

    @staticmethod
    def matches(line: str) -> bool:
        return bool(_block_quote_re.match(line))

    @staticmethod
    def strip_delimiters(line: str) -> str:
        m = _block_quote_re.match(line)
        if not m:
            return line
        return line[m.end():]
