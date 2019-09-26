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

import html2md
import jinja2
import os
import re


class MarkdownLoader(jinja2.BaseLoader):
  def __init__(self, searchpath=None):
    self.searchpath = searchpath or '.'

  def get_source(self, env, name):
    path = os.path.join(self.searchpath, name)
    if not os.path.exists(path):
      raise jinja2.TemplateNotFound(path)

    mtime = os.path.getmtime(path)
    with open(path) as f:
      source = f.read()
      if '<body>' not in source:
        source = '<body>{}</body>'.format(source)
      source = html2md.convert(source)

    # Normalize source code before applying any templating logic.
    source = remove_html_comments(source)
    source = normalize_inline_code_block(source)
    source = jekyll_liquid_capture(source)
    source = jekyll_liquid_include(source)
    return source, path, lambda: mtime == os.path.getmtime(path)

  
def replace(source, regex, fn):
  replacements = {
      m.group(0): fn(m)
      for m in regex.finditer(source)
  }
  for old, new in replacements.items():
    source = source.replace(old, new)
  return source


def remove_html_comments(source):
  html_comments_re = re.compile(r'''
      (\s*)?                # 0: whitespaces before
      <!--(?:(?!-->).)*-->  # <!-- comment -->
      (\s*)?                # 1: whitespaces after
  ''', re.VERBOSE | re.DOTALL)
  def fn(m):
    if '\n' in (m[0] or '') + (m[1] or ''):
      return '\n'
    return ' '
  return replace(source, html_comments_re, fn).strip('\n')


def normalize_inline_code_block(source):
  code_block_re = re.compile(r'''
      ^((?:{:\s*[^}]+})?```)  # group 1: initial ``` OR {:.class}```
      ((?:(?!(?:```$)).)*?)   # group 2: everything until \n```
      \n?```$                 # ending ```
  ''', re.VERBOSE | re.MULTILINE | re.DOTALL)

  # Normalize inline code block finish backticks into next line, example:
  # ```
  # {% github_sample path/to/file tag:tag % }```
  return code_block_re.sub(r'\1\2\n```', source)


def jekyll_liquid_capture(source):
  jekyll_liquid_capture_re = re.compile(r'''
      {%\s*capture\s+(?P<name>\w+)\s*%}         # {% capture variable_name %}
      (?P<body>(?:(?!{%\s*endcapture\s*%}).)*)  # Everything until endcapture
      {%\s*endcapture\s*%}                      # {% endcapture %}
  ''', re.VERBOSE | re.DOTALL)

  def fn(m):
    return (
        '{{% set {} %}}'
        '{}'
        '{{% endset %}}'
    ).format(m['name'], m['body'])
  return replace(source, jekyll_liquid_capture_re, fn)


def jekyll_liquid_include(source):
  jekyll_liquid_include_re = re.compile(r'''
      {%\s*include\s+
      (?P<file>"[^"]*"|[^\s]+)\s+                     # include_file
      (?P<args>(?:\w+\s*=\s*(?:"[^"]*"|[^\s]+)\s+)*)  # arg="text" arg=variable
      \s*%}
  ''', re.VERBOSE)

  jekyll_liquid_include_arg_re = re.compile(r'''
      (?P<name>\w+)\s*=\s*(?P<value>"[^"]*"|[^\s]+)   # arg="text" arg=variable
  ''', re.VERBOSE)

  def fn(m):
    include_file = m['file'].strip('\'"')
    args = [
        '"{}": {}'.format(arg['name'], arg['value'])
        for arg in jekyll_liquid_include_arg_re.finditer(m['args'])
    ]
    return (
        '{{% with include={{{}}} %}}'
        '{{% include "{}" %}}'
        '{{% endwith %}}'
    ).format(', '.join(args), include_file)
  return replace(source, jekyll_liquid_include_re, fn)
