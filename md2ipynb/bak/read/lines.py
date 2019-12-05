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
import tempfile
from io import StringIO

from . import MarkdownLoader
from . import GithubSampleExt


def lines(input_file='-', variables=None, include_dir=None, jinja_env=None):
  if not jinja_env:
    jinja_env = jinja2.Environment(
        loader=MarkdownLoader(include_dir),
        extensions=[GithubSampleExt],
    )

  # Read from a file, stdin or an iterable without any trailing newlines.
  if isinstance(input_file, str):
    # If input_file is '-', fileinput.input() will read from stdin.
    # Otherwise, it will open the file path.
    lines = [line.rstrip() for line in fileinput.input(input_file)]
  else:
    lines = [line.rstrip() for line in input_file]

  # jinja_env.from_string() doesn't apply the MarkdownLoader,
  # so we create a named temporary file instead.
  with tempfile.NamedTemporaryFile('w') as f:
    f.write('\n'.join(lines))
    f.seek(0)
    input_template = jinja_env.get_template(f.name)

  # Render the template and yield the lines.
  source = input_template.render(variables or {})
  for line in source.splitlines():
    yield line.rstrip()
