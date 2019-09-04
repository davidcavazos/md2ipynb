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

from md2ipynb.util import class_re

from . import lines


def paragraphs(input_file='-', variables=None, jinja_env=None):
  is_paragraph_done = False
  in_code_block = False
  paragraph_lines = []
  for raw_line in lines(input_file, variables, jinja_env):
    line = class_re.sub('', raw_line)
    if is_paragraph_done:
      is_paragraph_done = False
      if paragraph_lines:
        trailing_paragraph_class = raw_line and not line
        if trailing_paragraph_class:
          paragraph_lines.append(raw_line)
        yield '\n'.join(paragraph_lines)
        paragraph_lines = []
        if trailing_paragraph_class:
          continue

    if in_code_block:
      paragraph_lines.append(raw_line)
      if line.startswith('```'):
        in_code_block = False
        is_paragraph_done = True

    elif not in_code_block and line.startswith('```'):
      in_code_block = True
      if len(paragraph_lines) == 1 and class_re.match(paragraph_lines[0]):
        paragraph_lines.append(raw_line)
      else:
        if paragraph_lines:
          yield '\n'.join(paragraph_lines)
        paragraph_lines = [raw_line]

    elif line.startswith('#'):
      if len(paragraph_lines) == 1 and class_re.match(paragraph_lines[0]):
        paragraph_lines.append(raw_line)
      else:
        if paragraph_lines:
          yield '\n'.join(paragraph_lines)
        paragraph_lines = [raw_line]
      is_paragraph_done = True

    elif raw_line:
      paragraph_lines.append(raw_line)

    else:  # raw_line is empty.
      if paragraph_lines:
        yield '\n'.join(paragraph_lines)
        paragraph_lines = []

  if paragraph_lines:
    yield '\n'.join(paragraph_lines)
