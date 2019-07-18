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

from . import MarkdownLoader
from . import GithubSampleExt
from .github_sample import extract_snippet


class GithubSampleExtTest(unittest.TestCase):
  def test_github_sample(self):
    env = jinja2.Environment(loader=MarkdownLoader(), extensions=[GithubSampleExt])
    template = env.from_string('\n'.join([
        '# Github sample',
        '```',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]))
    actual = template.render()
    expected = '\n'.join([
        '# Github sample',
        '```',
        "print('Hello world!')",
        '```',
    ])
    self.assertEqual(actual, expected)

  def test_github_sample_py(self):
    env = jinja2.Environment(loader=MarkdownLoader(), extensions=[GithubSampleExt])
    template = env.from_string('\n'.join([
        '# Github sample - Python',
        '```py',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]))
    actual = template.render()
    expected = '\n'.join([
        '# Github sample - Python',
        '```py',
        "print('Hello world!')",
        '```',
    ])
    self.assertEqual(actual, expected)

  @unittest.skip('Languages other than Python are not implemented yet')
  def test_github_sample_go(self):
    env = jinja2.Environment(loader=MarkdownLoader(), extensions=[GithubSampleExt])
    template = env.from_string('\n'.join([
        '# Github samples - Go',
        '```go',
        '{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.go tag:hello_world %}',
        '```',
    ]))
    actual = template.render()
    expected = '\n'.join([
        '# Github samples - Go',
        '```go',
        '!mkdir -p examples/code',
        '```',
        '',
        '```go',
        '%%writefile examples/code/hello-world.go',
        'package main',
        '',
        'import "fmt"',
        '',
        'func main() {',
        '\tfmt.Println("Hello world!")',
        '}',
        '',
        '```',
        '',
        '```go',
        '!go run examples/code/hello-world.go',
        '```',
    ])
    self.assertEqual(actual, expected)


class ExtractSnippetTest(unittest.TestCase):
  def test_extract_snippet(self):
    actual = extract_snippet(
        source='\n'.join([
            '# Extract snippet',
            '[START region_tag]',
            "print('Hello')",
            '[END region_tag]',
        ]),
        tag='region_tag',
    )
    expected = '\n'.join([
        "print('Hello')",
    ])
    self.assertEqual(actual, expected)

  def test_extract_snippet_indented(self):
    actual = extract_snippet(
        source='\n'.join([
            '# Extract snippet indented',
            'def say_hello():',
            '  [START region_tag]',
            "  print('Hello')",
            '  if True:',
            "    print('world!')",
            '  [END region_tag]',
        ]),
        tag='region_tag',
    )
    expected = '\n'.join([
        "print('Hello')",
        'if True:',
        "  print('world!')",
    ])
    self.assertEqual(actual, expected)
