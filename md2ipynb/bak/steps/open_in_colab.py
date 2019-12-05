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


def open_in_colab(cells, ipynb_github_url=None, **kwargs):
  if ipynb_github_url:
    if ipynb_github_url.startswith('https://'):
      ipynb_github_url = ipynb_github_url[len('https://'):]
    if ipynb_github_url.startswith('github.com/'):
      ipynb_github_url = ipynb_github_url[len('github.com/'):]
    yield nbformat.v4.new_markdown_cell(
        '<a href="https://colab.research.google.com/github/{}" target="_parent">'
          '<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/>'
        '</a>'.format(ipynb_github_url),
        metadata={'id': 'view-in-github'},
    )

  for cell in cells:
    yield cell
