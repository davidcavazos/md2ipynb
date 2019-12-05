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

from md2ipynb.util import attributes_re

from . import lines


def paragraphs(input_file='-', variables=None, include_dir=None, jinja_env=None):
  is_paragraph_done = False
  in_code_block = False
  paragraph_lines = []

  for raw_line in lines(input_file, variables, include_dir, jinja_env):
    # `raw_line` is the unmodified line.
    # `line` has custom attributes removed if any. {: #id .class attrib='value'}
    line = attributes_re.sub('', raw_line)

    # If a paragraph is marked as done, check for a trailing
    # paragraph class {: class} and then yield the paragraph.
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

    # Code block ends.
    if in_code_block:
      paragraph_lines.append(raw_line)
      if line.startswith('```'):
        in_code_block = False
        is_paragraph_done = True

    # Code block starts.
    elif not in_code_block and line.startswith('```'):
      in_code_block = True
      if len(paragraph_lines) == 1 and attributes_re.match(paragraph_lines[0]):
        paragraph_lines.append(raw_line)
      else:
        if paragraph_lines:
          yield '\n'.join(paragraph_lines)
        paragraph_lines = [raw_line]

    # Header starts.
    elif line.startswith('#'):
      if len(paragraph_lines) == 1 and attributes_re.match(paragraph_lines[0]):
        paragraph_lines.append(raw_line)
      else:
        if paragraph_lines:
          yield '\n'.join(paragraph_lines)
        paragraph_lines = [raw_line]
      is_paragraph_done = True

    # Non-empty lines are just appended to the current paragraph.
    elif raw_line:
      paragraph_lines.append(raw_line)

    # Empty line means the paragraph ended so yield it.
    else:
      if paragraph_lines:
        yield '\n'.join(paragraph_lines)
        paragraph_lines = []

  # Yield any remaining paragraph that wasn't triggered to yield before.
  if paragraph_lines:
    yield '\n'.join(paragraph_lines)
