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

"""Script to generate Jupyter notebooks from a markdown page.

[START run_hello_world_simple]
pip install -U md2nb

md2nb example/pages/hello-world.md \
  --var name:md2nb \
  --imports \
    example/templates/setup-py.md:0 \
    example/templates/cleanup.md:-1
[END run_hello_world_simple]
"""

import base64
import jinja2
import json
import logging
import nbformat
import os
import re
import requests

from collections.abc import Iterable

DEFAULT_LANG = 'py'
DEFAULT_SHELL = ['bash', 'sh']
DEFAULT_LANG_PATTERN = [
    r'^```%s',
    r'^{:.%s}',
    r'^{:.language-%s}',
    r'^{:.shell-%s}',
]
DEFAULT_KERNEL = 'python3'

# NOTE: the default steps are defined at the bottom of the file.

# TODOS:
# - ignore comment html cells
# - shell code blocks
# - if cell.source.startswith('#@title'):
#     metadata['cellView'] = 'form'


def code_block(source):
  GITHUB_SAMPLE_RE = re.compile(
      r'{%\s*github_sample\s+/([^/]+)/([^/]+)/blob/([^/]+)/([\w/.-]+)\s+tag:(\w+)\s*%}')
  first_tag = ''
  for m in GITHUB_SAMPLE_RE.finditer(source):
    owner, repo, branch, path, tag = m.groups()
    if not first_tag:
      first_tag = tag
    url = 'https://api.github.com/repos/{}/{}/input_files/{}'.format(owner, repo, path)
    req = requests.get(url, params={'ref': branch})
    if req.status_code == requests.codes.ok:
      req = req.json()
      input_file = base64.b64decode(req['input_file']).decode('utf-8')
      snippet = extract_snippet(input_file, tag)
      source = source.replace(m.group(0), snippet)
  return source.rstrip(), first_tag


def shell_code_block(source):
  return '\n'.join([
      '!{}'.format(line) if line and not line.startswith('#') else line
      for line in source.splitlines()
  ])


def extract_snippet(input_file, tag):
  tag_start_re = re.compile(r'\[\s*START\s+{}\s*\]'.format(tag))
  tag_end_re = re.compile(r'\[\s*END\s+{}\s*\]'.format(tag))
  
  started = False
  min_indent = float('Inf')
  snippet = []
  for line in input_file.splitlines():
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


def error_message(message, re_match, line_number, line):
  return '\n'.join([
      "line {}: {}'".format(line_number, message),
      '',
      line,
      ' '*re_match.start() + '~'*len(re_match.group(0)),
      '',
  ])


def main(argv=None):
  import argparse

  parser = argparse.ArgumentParser()

  # Required arguments.
  parser.add_argument('input_file', help='Path to a markdown file to convert.')

  # Optional arguments.
  parser.add_argument(
      '-o', '--output_file',
      help='Path of the output notebook to write.',
  )

  parser.add_argument(
      '--fatal-errors',
      action='store_true',
      help='Setting this will raise an exception on the first error.',
  )

  parser.add_argument(
      '--var',
      type=lambda value: value.split(':', 1),
      default=[],
      nargs='+',
      help='Sets a variable in the format "name:value".',
  )

  parser.add_argument(
      '--filter-ignore',
      default=[],
      nargs='+',
      help='Regular expression(s) to ignore paragraphs that match.',
  )

  parser.add_argument(
      '--filter-keep',
      default=[],
      nargs='+',
      help='Regular expression(s) to keep "ignored" paragraphs that match.',
  )

  parser.add_argument(
      '--replace',
      type=lambda value: value[1:].split(value[0], 1),
      default=[],
      nargs='+',
      help='Regular expression(s) to replace with another text. '
           'The first character will act as the delimiter between '
           'the "old" and "new" strings. '
           'Examples: "/old/new" "|old|new" "@old@new"',
  )

  parser.add_argument(
      '--lang',
      default=[],
      nargs='+',
      help='Language(s) to include in code blocks as regular expressions.',
  )

  parser.add_argument(
      '--shell',
      default=[],
      nargs='+',
      help='Shell command language(s) to include in code blocks '
           'as regular expressions.',
  )

  parser.add_argument(
      '--no-start-on-header',
      action='store_false',
      dest='start_on_header',
      help='Enables to convert content before the first header too.',
  )

  parser.add_argument(
      '--imports',
      type=lambda value: value.split(':', 1),
      default=[],
      nargs='+',
      help='File(s) to import at a certain section index. '
           'Sections are delimited by headers. '
           'Negative indices start from the last section. '
           'Must be in the format "path/to/file.md:index"'
           'Examples: "templates/setup.md:0" "templates/cleanup.md:-1"',
  )

  parser.add_argument(
      '--docs-url',
      help='URL to the source docs page for the "View the Docs" button.',
  )

  parser.add_argument(
      '--docs-logo-url',
      help='URL to the logo to be shown for the "View the Docs" button.',
  )

  parser.add_argument(
      '--ipynb-github-url',
      help='GitHub URL of the ipynb file for the "Open in Colab" button.',
  )

  parser.add_argument(
      '--notebook-title',
      help='Notebook title to show on Colab.',
  )

  parser.add_argument(
      '--kernel',
      default=DEFAULT_KERNEL,
      help='Notebook kernel to use, defaults to "python3".',
  )

  args = parser.parse_args(argv)

  # Input validation.
  try:
    variables = dict(args.var)
  except ValueError:
    parser.error('variables must be in the format "name:value", '
                 'use --help for more information.')

  try:
    replace = dict(args.replace)
  except ValueError:
    parser.error('replace must be in the format "/old/new" or "|old|new", '
                 'use --help for more information.')

  try:
    imports = {}
    for path, index in args.imports:
      index = int(index)
      if index not in imports:
        imports[index] = []
      imports[index].append(path)
  except ValueError:
    parser.error('imports must be in the format "path/to/file.md:index", '
                 'use --help for more information.')


if __name__ == '__main__':
  main()
