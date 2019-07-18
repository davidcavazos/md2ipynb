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

import fileinput
import jinja2

from . import MarkdownLoader
from . import github_samples


def lines(input_file='-', variables=None, jinja_env=None):
  if isinstance(input_file, str):
    # If input_file is '-', fileinput.input() will read from stdin.
    # Otherwise, it will open the file path.
    lines = [line.rstrip() for line in fileinput.input(input_file)]
  else:
    lines = [line.rstrip() for line in input_file]

  if not jinja_env:
    jinja_env = jinja2.Environment(loader=MarkdownLoader())

  source = github_samples('\n'.join(lines))
  input_template = jinja_env.from_string(source)
  source = input_template.render(variables or {})
  for line in source.splitlines():
    yield line.rstrip()
