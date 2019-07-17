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

import base64
import re
import requests

GITHUB_SAMPLE_RE = re.compile(
    r'{%\s*'                                    # {%
    r'github_sample\s+'                         # github_sample
    r'/([^/]+)/([^/]+)/blob/([^/]+)/([\w/.-]+)' # /owner/repo/blob/branch/path
    r'\s+tag:(\w+)'                             # tag:region_tag
    r'\s*%}'                                    # %}
)


def github_samples(source):
  for m in GITHUB_SAMPLE_RE.finditer(source):
    owner, repo, branch, path, tag = m.groups()
    url = 'https://raw.githubusercontent.com/{}/{}/{}/{}'.format(owner, repo, branch, path)
    req = requests.get(url, params={'ref': branch})
    if req.status_code == requests.codes.ok:
      snippet = extract_snippet(req.text, tag)
      source = source.replace(m.group(0), snippet, 1)
  return source.rstrip()


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
