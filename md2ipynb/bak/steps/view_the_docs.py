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


def view_the_docs(cells, docs_url=None, docs_logo_url=None):
  if docs_url:
    docs_logo_html = ''
    if docs_logo_url:
      docs_logo_html = \
          '<img src="{}" width="32" height="32" />'.format(docs_logo_url)
    view_the_docs_html = (
        '<table align="left">'
          '<td>'
            '<a target="_blank" href="{}">'
              '{}View the docs'
            '</a>'
          '</td>'
        '</table>'
    ).format(docs_url, docs_logo_html)

    yield nbformat.v4.new_markdown_cell(
        source=view_the_docs_html,
        metadata={'id': 'view-the-docs-top'},
    )

  for cell in cells:
    yield cell

  if docs_url:
    yield nbformat.v4.new_markdown_cell(
        source=view_the_docs_html,
        metadata={'id': 'view-the-docs-bottom'},
    )
