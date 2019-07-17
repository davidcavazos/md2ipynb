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

from . import lines


def paragraphs(input_file='-', variables=None, jinja_env=None):
  in_code_block = False
  paragraph = []
  for line in lines(input_file, variables, jinja_env):
    if in_code_block:
      paragraph.append(line)
      if line.endswith('```'):
        in_code_block = False
        if paragraph:
          yield '\n'.join(paragraph)
        paragraph = []
    elif not in_code_block and line.startswith('```'):
      in_code_block = True
      if paragraph:
        yield '\n'.join(paragraph)
      paragraph = [line]
    elif not line and paragraph:
      yield '\n'.join(paragraph)
      paragraph = []
    elif line.startswith('#'):
      if paragraph:
        yield '\n'.join(paragraph)
      paragraph = []
      yield line
    elif line:
      paragraph.append(line)
  if paragraph:
    yield '\n'.join(paragraph)
