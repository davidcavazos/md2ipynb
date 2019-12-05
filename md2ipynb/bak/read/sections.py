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

from . import paragraphs


def sections(input_file='-', variables=None, include_dir=None, jinja_env=None, start_on_header=True):
  header_found = False
  section = []
  for paragraph in paragraphs(input_file, variables, include_dir, jinja_env):
    if paragraph[0].startswith('#'):
      if section and (not start_on_header or header_found):
        yield section
      section = []
      header_found = True
    section.append(paragraph)
  if section:
    yield section
