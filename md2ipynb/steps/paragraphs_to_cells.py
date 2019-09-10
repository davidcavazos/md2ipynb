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

import nbformat
import re

invalid_cell_id_chars = re.compile(r'[^\w]+')


def paragraphs_to_cells(paragraphs):
  used_ids = set()
  def cell_id(name):
    if not name:
      return ''
    name = invalid_cell_id_chars.sub('-', name.lower()).strip('-')
    if name not in used_ids:
      used_ids.add(name)
      return name
    i = 2
    while True:
      numbered = '{}-{}'.format(name, i)
      if numbered not in used_ids:
        used_ids.add(numbered)
        return numbered
      i += 1

  last_header = '_'
  contents = []
  for paragraph in paragraphs:
    lines = paragraph.splitlines()
    if not lines:
      continue

    if lines[0].startswith('#'):
      if contents:
        yield nbformat.v4.new_markdown_cell(
            source='\n\n'.join(contents),
            metadata={'id': cell_id(last_header)},
        )
      contents = [paragraph]
      last_header = lines[0].lstrip('#').strip()
    elif lines[0].startswith('```') and lines[-1].startswith('```'):
      if contents:
        yield nbformat.v4.new_markdown_cell(
            source='\n\n'.join(contents),
            metadata={'id': cell_id(last_header)},
        )
        contents = []
      source = '\n'.join(lines[1:-1])
      metadata={'id': cell_id(last_header + '-code')}
      if '#@title' in source or '#@param' in source:
        metadata.update({'cellView': 'form'})
      yield nbformat.v4.new_code_cell(
          source=source,
          metadata=metadata,
      )
    else:
      contents.append(paragraph)
  if contents:
    yield nbformat.v4.new_markdown_cell(
        source='\n\n'.join(contents),
        metadata={'id': cell_id(last_header)},
    )