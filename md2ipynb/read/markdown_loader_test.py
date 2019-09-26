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
import tempfile
import unittest

from unittest.mock import patch

from . import GithubSampleExt
from . import MarkdownLoader

expected_file = 'test/hello-expected.md'
variables_file = 'test/hello-variables.json'

with open(expected_file) as f:
  expected = f.read().rstrip()
with open(variables_file) as f:
  variables = json.load(f)

env = jinja2.Environment(loader=MarkdownLoader(), extensions=[GithubSampleExt])


def render_string(source, variables=None, env=env):
  with tempfile.NamedTemporaryFile('w') as f:
    f.write(source)
    f.seek(0)
    template = env.get_template(f.name)
  return template.render(variables or {})

class MarkdownLoaderTest(unittest.TestCase):
  def test_from_file_markdown(self):
    template = env.get_template('test/hello.md')
    actual = template.render(variables)
    self.assertEqual(expected, actual)

  def test_from_file_html(self):
    with open('test/hello-html-expected.md') as f:
      expected = f.read().strip()
    template = env.get_template('test/hello.html')
    actual = template.render(variables)
    self.assertEqual(expected, actual)

  def test_include(self):
    actual = render_string('\n'.join([
        "{% include 'test/title.md' %}",
        '',
        'Hello {{name}}!',
        '',
        '```py',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]), variables)
    self.assertEqual(expected, actual)

  def test_include_searchpath(self):
    env = jinja2.Environment(loader=MarkdownLoader('test/'),
                             extensions=[GithubSampleExt])
    actual = render_string('\n'.join([
        "{% include 'title.md' %}",
        '',
        'Hello {{name}}!',
        '',
        '```py',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]), variables, env)
    self.assertEqual(expected, actual)

  def test_include_not_found(self):
    template = env.from_string("{% include 'non-existent-file.md' %}")
    with self.assertRaises(jinja2.exceptions.TemplateNotFound):
      template.render()

  def test_remove_html_comments(self):
    expected = '\n'.join([
        'line 1',
        'line 2',
        'line 3',
    ])
    actual = render_string('\n'.join([
        '<!-- single line comment -->',
        'line 1',
        'line <!-- embedded comment --> 2',
        '<!--',
        'multi',
        'line',
        'comment',
        '-->',
        'line 3',
        '<!-- ending comment -->',
    ]))
    self.assertEqual(expected, actual)


  def test_code_block(self):
    expected = '\n'.join([
        '```',
        "# Hello world in Python.",
        "print('Hello from Python!')",
        '```',
    ])
    actual = render_string('\n'.join([
        '```',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]))
    self.assertEqual(expected, actual)

  def test_code_block_ending_inline(self):
    expected = '\n'.join([
        '```',
        "# Hello world in Python.",
        "print('Hello from Python!')",
        '```',
    ])
    actual = render_string('\n'.join([
        '```',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}```',
    ]))
    self.assertEqual(expected, actual)

  def test_jekyll_liquid_include_static(self):
    expected = '\n'.join([
        '# Include static',
        '# Include static',
    ])
    actual = render_string('\n'.join([
        '{% include test/include-static.md %}',
        '{% include "test/include-static.md" %}',
    ]))
    self.assertEqual(expected, actual)

  def test_jekyll_liquid_include_argument(self):
    expected = '\n'.join([
        '# Include argument',
        '# Include argument',
    ])
    actual = render_string('\n'.join([
        '{% include test/include-argument.md title="Include argument" %}',
        '{% include "test/include-argument.md" title="Include argument" %}',
    ]))
    self.assertEqual(expected, actual)

  def test_jekyll_liquid_include_argument_variable(self):
    expected = '\n'.join([
        '',
        '# Include argument variable',
        '# Include argument variable',
    ])
    actual = render_string('\n'.join([
        '{% capture var %}Include argument variable{% endcapture %}',
        '{% include test/include-argument.md title=var %}',
        '{% include "test/include-argument.md" title=var %}',
    ]))
    self.assertEqual(expected, actual)
