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

from . import new_notebook

variables = {
    'title': 'Hello world',
    'name': 'md2ipynb',
}

expected_source = '\n'.join([
    '# Hello world',
    '',
    'Hello md2ipynb!',
])

def md_cell(source, id=''):
  return nbformat.v4.new_markdown_cell(source, metadata={'id': id})


def code_cell(source, id=''):
  return nbformat.v4.new_code_cell(source, metadata={'id': id})


def nb_metadata(name):
  return {
      'colab': {
          'name': name,
          'toc_visible': True,
      },
      'kernelspec': {
          'name': 'python3',
          'display_name': 'python3',
      },
  }


class NewNotebookTest(unittest.TestCase):
  def test_new_notebook_hello_world(self):
    actual = new_notebook('test/variables.md', variables)
    expected = nbformat.v4.new_notebook(
        cells=[
            md_cell(expected_source, 'hello-world'),
        ],
        metadata=nb_metadata('Hello world'),
    )
    self.assertEqual(actual, expected)
