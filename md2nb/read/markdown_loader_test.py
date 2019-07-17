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
import unittest

from unittest.mock import patch

from . import MarkdownLoader

with open('examples/pages/hello-world.md') as f:
  source = f.read()

variables = {
    'title': 'Hello world',
    'name': 'md2nb',
}

expected = '''\
# Hello world

Hello md2nb!'''


class MarkdownLoaderTest(unittest.TestCase):
  def test_from_file(self):
    env = jinja2.Environment(loader=MarkdownLoader())
    template = env.get_template('examples/pages/hello-world.md')
    self.assertEqual(template.render(variables), expected)

  def test_from_string(self):
    env = jinja2.Environment(loader=MarkdownLoader())
    template = env.from_string('\n'.join([
        '# {{ title }}',
        '',
        'Hello {{name}}!',
    ]))
    self.assertEqual(template.render(variables), expected)

  def test_include(self):
    env = jinja2.Environment(loader=MarkdownLoader())
    template = env.from_string('\n'.join([
        "{% include 'examples/templates/title.md' %}",
        '',
        'Hello {{name}}!',
    ]))
    self.assertEqual(template.render(variables), expected)

  def test_include_searchpath(self):
    env = jinja2.Environment(loader=MarkdownLoader('examples/templates'))
    template = env.from_string('\n'.join([
        "{% include 'title.md' %}",
        '',
        'Hello {{name}}!',
    ]))
    self.assertEqual(template.render(variables), expected)

  def test_include_not_found(self):
    env = jinja2.Environment(loader=MarkdownLoader())
    template = env.from_string("{% include 'non-existent-file.md' %}")
    with self.assertRaises(jinja2.exceptions.TemplateNotFound):
      template.render()
