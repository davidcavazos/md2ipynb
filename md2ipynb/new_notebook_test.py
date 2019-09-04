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

import json
import nbformat
import unittest

from . import new_notebook

source_file = 'test/hello.md'
variables_file = 'test/hello-variables.json'

with open(variables_file) as f:
  variables = json.load(f)


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


def as_dict(nb):
  return json.loads(nbformat.writes(nb))

class NewNotebookTest(unittest.TestCase):
  def test_new_notebook_hello_world(self):
    expected = as_dict(nbformat.v4.new_notebook(
        cells=[
            md_cell('\n'.join([
                '# ' + variables['title'],
                '',
                'Hello {}!'.format(variables['name']),
            ]), 'hello-world'),
            code_cell('\n'.join([
                "# Hello world in Python.",
                "print('Hello from Python!')",
            ]), 'hello-world-code'),
        ],
        metadata=nb_metadata(variables['title']),
    ))
    actual = as_dict(new_notebook(source_file, variables))
    self.maxDiff = None
    self.assertEqual(expected, actual)
