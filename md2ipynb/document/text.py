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

from .element import Element
from .text_style import TextStyle


@dataclass
class Text(Element):
    value: str
    style: TextStyle = TextStyle.body1

    @staticmethod
    def h1(value: str) -> Text:
        return Text(value, style=TextStyle.h1)

    @staticmethod
    def h2(value: str) -> Text:
        return Text(value, style=TextStyle.h2)

    @staticmethod
    def h3(value: str) -> Text:
        return Text(value, style=TextStyle.h3)

    @staticmethod
    def h4(value: str) -> Text:
        return Text(value, style=TextStyle.h4)

    @staticmethod
    def h5(value: str) -> Text:
        return Text(value, style=TextStyle.h5)

    @staticmethod
    def h6(value: str) -> Text:
        return Text(value, style=TextStyle.h6)

    @staticmethod
    def subtitle1(value: str) -> Text:
        return Text(value, style=TextStyle.subtitle1)

    @staticmethod
    def subtitle2(value: str) -> Text:
        return Text(value, style=TextStyle.subtitle2)

    @staticmethod
    def body1(value: str) -> Text:
        return Text(value, style=TextStyle.body1)

    @staticmethod
    def body2(value: str) -> Text:
        return Text(value, style=TextStyle.body2)

    @staticmethod
    def button(value: str) -> Text:
        return Text(value, style=TextStyle.button)

    @staticmethod
    def caption(value: str) -> Text:
        return Text(value, style=TextStyle.caption)

    @staticmethod
    def overline(value: str) -> Text:
        return Text(value, style=TextStyle.overline)
