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

import jinja2

from md2ipynb import read


def imports(sections, imports=None, variables=None, include_dir=None, jinja_env=None):
  def sections_from_imports(import_index):
    for input_file in imports[import_index]:
      for import_section in read.sections(input_file, variables, include_dir, jinja_env):
        yield import_section

  sections = list(sections)
  if imports is None:
    imports = {}

  # Normalize imports to the form: `{non_negative_index: [file1, file2, ...]}`.
  for index, input_file in imports.items():
    if index < 0:
      imports[len(sections)+index+1] = input_file
      del imports[index]

  # Iterate over all the sections, inserting any imports if needed.
  for i, section in enumerate(sections):
    if i in imports:
      for import_section in sections_from_imports(i):
        yield import_section
    yield section

  # Include imports that go at the end.
  i = len(sections)
  if i in imports:
    for import_section in sections_from_imports(i):
      yield import_section
