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

import re
import requests

from jinja2 import TemplateSyntaxError
from jinja2 import lexer
from jinja2 import nodes
from jinja2.ext import Extension

github_file_cache = {}


class GithubSampleExt(Extension):
  # Format: /<owner>/<repo>/blob/<branch>/<path>
  github_path_re = re.compile(
      r'^/([^/]+)/([^/]+)/blob/([^/]+)/([\w/.-]+)$')

  # A set of names that trigger the extension.
  tags = set(['github_sample'])

  def parse(self, parser):
    lineno = next(parser.stream).lineno

    github_path = ''
    tag = None
    last_token_type = None
    for token in parser.stream:
      if last_token_type == lexer.TOKEN_NAME and token.value == 'tag':
        parser.stream.expect(lexer.TOKEN_COLON)
        tag = parser.stream.expect(lexer.TOKEN_NAME).value
        break
      github_path += token.value
      last_token_type = token.type

    m = self.github_path_re.match(github_path)
    if not m:
      raise TemplateSyntaxError(
          'Github file path must be in the format '
          '/<owner>/<repo>/blob/<branch>/<path>, '
          'found {}'.format(repr(github_path)),
          lineno, parser.name, parser.filename)

    owner, repo, branch, path = m.groups()
    call = self.call_method('_github_sample', [
        nodes.Const(owner),
        nodes.Const(repo),
        nodes.Const(branch),
        nodes.Const(path),
        nodes.Const(tag),
    ])
    return nodes.CallBlock(call, [], [], []).set_lineno(lineno)

  def _github_sample(self, owner, repo, branch, path, tag, caller):
    url = 'https://raw.githubusercontent.com/{}/{}/{}/{}'.format(
        owner, repo, branch, path)
    if url in github_file_cache:
      github_file = github_file_cache[url]
    else:
      req = requests.get(url, params={'ref': branch})
      assert req.status_code == requests.codes.ok, '{} {}, contents:\n{}'.format(
          req, url, req.text)
      github_file = req.text
      github_file_cache[url] = github_file
    return extract_snippet(github_file, tag)


def extract_snippet(source, tag):
  tag_start_re = re.compile(r'\[\s*START\s+{}\s*\]'.format(tag))
  tag_end_re = re.compile(r'\[\s*END\s+{}\s*\]'.format(tag))

  started = False
  min_indent = float('Inf')
  snippet = []
  for line in source.splitlines():
    if not started and tag_start_re.search(line):
      started = True
    elif started:
      if tag_end_re.search(line):
        break
      snippet.append(line)
      if line.strip():
        indent = len(line) - len(line.lstrip())
        min_indent = min(indent, min_indent)

  if min_indent != float('Inf'):
    snippet = [line[min_indent:] for line in snippet]
  return '\n'.join(snippet)
