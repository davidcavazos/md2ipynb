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
import json
import unittest

from unittest.mock import patch

from . import GithubSampleExt
from . import MarkdownLoader

source_file = 'test/hello.md'
expected_file = 'test/hello-expected.md'
variables_file = 'test/hello-variables.json'

env = jinja2.Environment(loader=MarkdownLoader(), extensions=[GithubSampleExt])
with open(source_file) as f:
  source = f.read().rstrip()
with open(expected_file) as f:
  expected = f.read().rstrip()
with open(variables_file) as f:
  variables = json.load(f)


class MarkdownLoaderTest(unittest.TestCase):
  def test_from_file(self):
    template = env.get_template(source_file)
    actual = template.render(variables)
    self.assertEqual(expected, actual)

  def test_from_string(self):
    template = env.from_string(source)
    actual = template.render(variables)
    self.assertEqual(expected, actual)

  def test_include(self):
    template = env.from_string('\n'.join([
        "{% include 'test/title.md' %}",
        '',
        'Hello {{name}}!',
        '',
        '```py',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]))
    actual = template.render(variables)
    self.assertEqual(expected, actual)

  def test_include_searchpath(self):
    env = jinja2.Environment(loader=MarkdownLoader('examples/templates'),
                             extensions=[GithubSampleExt])
    template = env.from_string('\n'.join([
        "{% include 'title.md' %}",
        '',
        'Hello {{name}}!',
        '',
        '```py',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]))
    actual = template.render(variables)
    self.assertEqual(expected, actual)

  def test_include_not_found(self):
    template = env.from_string("{% include 'non-existent-file.md' %}")
    with self.assertRaises(jinja2.exceptions.TemplateNotFound):
      template.render()
