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
import unittest

from . import open_in_colab

def md_cell(source, id=''):
  return nbformat.v4.new_markdown_cell(source, metadata={'id': id})


def code_cell(source, id=''):
  return nbformat.v4.new_code_cell(source, metadata={'id': id})


class OpenInColabTest(unittest.TestCase):
  def test_open_in_colab(self):
    expected = [
        md_cell(
            '<a href="https://colab.research.google.com/github/user/repo/blob/master/notebook.ipynb" target="_parent">'
              '<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/>'
            '</a>',
            id='view-in-github',
        ),
        md_cell('content', id='H1'),
    ]
    actual = list(open_in_colab(
        cells=[md_cell('content', id='H1')],
        ipynb_github_url='https://github.com/user/repo/blob/master/notebook.ipynb',
    ))
    self.assertEqual(expected, actual)
