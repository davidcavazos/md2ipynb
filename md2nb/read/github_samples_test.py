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

import unittest

from . import github_samples
from .github_samples import extract_snippet


class GithubSamplesTest(unittest.TestCase):
  def test_github_samples(self):
    actual = github_samples('\n'.join([
        '# Github samples',
        '```',
        '{% github_sample /davidcavazos/md2nb/blob/master/examples/code/hello-world.py tag:hello_world %}',
        '```',
    ]))
    expected = '\n'.join([
        '# Github samples',
        '```',
        "print('Hello world!')",
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
