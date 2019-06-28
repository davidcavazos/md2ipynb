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
python docs_nbgen.py example/pages/hello-world.md \
  --var name:docs-nbgen \
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


def run(input_file, output_file=None, steps=None, steps_post=None, **kwargs):
  if output_file is None:
    if isinstance(input_file, str):
      output_file = os.path.splitext(input_file)[0] + '.ipynb'
    else:
      output_file = 'notebook.ipynb'

  notebook = new_notebook(input_file, steps, steps_post, **kwargs)

  print('Writing notebook to ' + output_file)
  with open(output_file, 'w') as f:
    nbformat.write(notebook, f)


def new_notebook(inputs, steps=None, steps_post=None,
                 notebook_title=None, kernel=DEFAULT_KERNEL, **kwargs):
  if steps_post is None:
    steps_post = DEFAULT_STEPS_POST

  sections = run_steps(inputs, steps, **kwargs)
  cells = list(run_steps(sections, steps_post, **kwargs))
  for cell in cells:
    if notebook_title is not None:
      break
    first_line = cell.source.splitlines()[0]
    if first_line.startswith('#'):
      notebook_title = first_line.strip('# ')

  # Create the notebook with all the cells.
  metadata = {
    'colab': {"toc_visible": True},
    'kernelspec': {'name': kernel, 'display_name': kernel},
  }
  if notebook_title:
    metadata['colab']['name'] = notebook_title

  return nbformat.v4.new_notebook(cells=cells, metadata=metadata)


def new_markdown_cell(source, **kwargs):
  for key in [key for key, value in kwargs.items() if value is None]:
    del kwargs[key]
  return nbformat.v4.new_markdown_cell(source, metadata=kwargs)


def new_code_cell(source, **kwargs):
  for key in [key for key, value in kwargs.items() if value is None]:
    del kwargs[key]
  return nbformat.v4.new_code_cell(source, metadata=kwargs)


def run_steps(inputs, steps=None, **kwargs):
  if steps is None:
    steps = DEFAULT_STEPS

  # Add `steps` into the **kwargs if any step needs it, like `imports`.
  kwargs['steps'] = list(steps)

  steps = list(steps)
  while steps:
    step = steps.pop(0)
    inputs = step(inputs, **kwargs)

  for line in inputs:
    yield line


def read_lines(input_file, **kwargs):
  if isinstance(input_file, str):
    with open(input_file) as f:
      for line in f:
        yield line
  else:
    for line in input_file:
      yield line


# TODO: separate this into two phases:
#   1. HTML code blocks to markdown
#   2. HTML headers (not inside code blocks) to markdown
def html_to_markdown(lines, **kwargs):
  html_header_re = re.compile(r'^\s*<h(\d+)>\s*(.*?)\s*</h\1>\s*$')
  html_code_block_re = re.compile(r'<pre(?:\s+class="([^"]*)")?[^>]*>')

  in_html_code_block = False
  for line in lines:
    line = line.rstrip()

    if not in_html_code_block:
      # Normalize HTML headers.
      m = html_header_re.search(line)
      if m:
        header_number = m.group(1)
        header_text = m.group(2)
        line = '#'*int(header_number) + ' ' + header_text

      # Normalize HTML code blocks.
      m = html_code_block_re.search(line)
      if m:
        in_html_code_block = True
        full_match = m.group(0)
        classes = m.group(1) or ''
        pre_line, line = line.split(full_match, 1)
        if pre_line:
          yield pre_line
          yield ''
        yield '```' + classes

    if in_html_code_block:
      if '</pre>' in line:
        in_html_code_block = False
        pre_line, line = line.split('</pre>', 1)
        yield pre_line
        yield '```'

    yield line


def jinja_variables(lines, variables=None, fatal_errors=False, **kwargs):
  if variables is None:
    variables = {}

  variables_re = re.compile(r'{{\s*([^\s}]+)\s*}}')
  for i, line in enumerate(lines):
    m = variables_re.search(line)
    if m:
      full_match = m.group(0)
      var_name = m.group(1)
      if var_name in variables:
        line = line.replace(full_match, str(variables[var_name]))
      else:
        message = error_message(
            "undefined variable '{}'".format(var_name), m, i+1, line)
        if fatal_errors:
          raise NameError(message)
        else:
          logging.warning(message)
    yield line


def lines_to_paragraphs(lines, **kwargs):
  in_code_block = False
  paragraph = []
  for line in lines:
    if in_code_block:
      paragraph.append(line)
      if line.endswith('```'):
        in_code_block = False
        if paragraph:
          yield '\n'.join(paragraph)
        paragraph = []
    elif not in_code_block and line.startswith('```'):
      in_code_block = True
      if paragraph:
        yield '\n'.join(paragraph)
      paragraph = [line]
    elif not line and paragraph:
      yield '\n'.join(paragraph)
      paragraph = []
    elif line.startswith('#'):
      if paragraph:
        yield '\n'.join(paragraph)
      paragraph = []
      yield line
    elif line:
      paragraph.append(line)
  if paragraph:
    yield '\n'.join(paragraph)


def re_filter(paragraphs, filter_ignore=None, filter_keep=None, **kwargs):
  def to_regex(pattern):
    if isinstance(pattern, str):
      return re.compile(pattern, re.DOTALL)
    elif isinstance(pattern, Iterable):
      pattern = '|'.join([r'(?:{})'.format(p) for p in pattern])
      return re.compile(pattern, re.DOTALL)
    return pattern

  filter_ignore = to_regex(filter_ignore)
  filter_keep = to_regex(filter_keep)
  for paragraph in paragraphs:
    if filter_ignore and filter_ignore.search(paragraph):
      if filter_keep and filter_keep.search(paragraph):
        yield paragraph
    else:
      yield paragraph


def re_replace(paragraphs, replace=None, replace_count=0, **kwargs):
  if replace is None:
    replace = {}

  replace = {
      re.compile(pattern, re.DOTALL): text
      for pattern, text in replace.items()
  }

  for paragraph in paragraphs:
    for pattern, text in replace.items():
      paragraph = re.sub(pattern, text, paragraph, replace_count)
    if paragraph:
      yield paragraph


def language(paragraphs, lang=None, shell=None, lang_pattern=None, **kwargs):
  def as_str_list(value, default):
    if value is None:
      value = default
    if isinstance(value, str):
      value = [value]
    return value
  lang = as_str_list(lang, DEFAULT_LANG)
  shell = as_str_list(shell, DEFAULT_SHELL)
  lang_pattern = as_str_list(lang_pattern, DEFAULT_LANG_PATTERN)

  for paragraph in paragraphs:
    yield paragraph


def paragraphs_to_sections(paragraphs, start_on_header=True, **kwargs):
  header_found = False
  section = []
  for paragraph in paragraphs:
    if paragraph[0].startswith('#'):
      if section and (not start_on_header or header_found):
        yield section
      section = []
      header_found = True
    section.append(paragraph)
  if section:
    yield section


def imports(sections, imports=None, steps=None, **kwargs):
  sections = list(sections)
  if imports is None:
    imports = {}
  if steps is None:
    steps = [lambda inputs, **kwargs: [inputs]]

  # Normalize imports to the form: `non_negative_index: [file1, file2, ...]`
  for index, inputs in imports.items():
    if index < 0:
      imports[len(sections)+index+1] = inputs
      del imports[index]

  for i, section in enumerate(sections):
    if i in imports:
      for inputs in imports[i]:
        for result in run_steps(inputs, steps, **kwargs):
          yield result
    yield section

  i = len(sections)
  if i in imports:
    for inputs in imports[i]:
      for result in run_steps(inputs, steps, **kwargs):
        yield result


def flatten(lists, **kwargs):
  for sublist in lists:
    for element in sublist:
      yield element


def paragraphs_to_cells(paragraphs, **kwargs):
  invalid_cell_id_chars = re.compile(r'[^\w]+')

  used_ids = set()
  def cell_id(name):
    if not name:
      return None
    name = invalid_cell_id_chars.sub('-', name.lower()).strip('-')
    if name not in used_ids:
      used_ids.add(name)
      return name
    i = 2
    while True:
      numbered = '{}-{}'.format(name, i)
      if numbered not in used_ids:
        used_ids.add(name)
        return numbered
      i += 1

  last_header = None
  contents = []
  for paragraph in paragraphs:
    if paragraph.startswith('#'):
      if contents:
        yield new_markdown_cell('\n\n'.join(contents), id=cell_id(last_header))
      contents = [paragraph]
      last_header = paragraph.splitlines()[0].lstrip('# ')
    elif paragraph.startswith('```') and paragraph.endswith('```'):
      if contents:
        yield new_markdown_cell('\n\n'.join(contents), id=cell_id(last_header))
        contents = []
      yield new_code_cell('\n'.join(paragraph.splitlines()[1:-1]),
                          id=cell_id(last_header + '-code'))
    else:
      contents.append(paragraph)
  if contents:
    yield new_markdown_cell('\n\n'.join(contents), id=cell_id(last_header))


def view_the_docs(cells, docs_url=None, docs_logo_url=None, **kwargs):
  docs_logo_html = ''
  if docs_logo_url:
    docs_logo_html = \
        '<img src="{}" width="32" height="32" />'.format(docs_logo_url)
  view_the_docs_html = (
      '<table align="left">'
        '<td>'
          '<a target="_blank" href="{}">'
            '{}View the Docs'
          '</a>'
        '</td>'
      '</table>'
  ).format(docs_url, docs_logo_html)

  if docs_url:
    yield new_markdown_cell(view_the_docs_html, id='view-the-docs-top')

  for cell in cells:
    yield cell

  if docs_url:
    yield new_markdown_cell(view_the_docs_html, id='view-the-docs-bottom')


def open_in_colab(cells, ipynb_github_url=None, **kwargs):
  if ipynb_github_url:
    if ipynb_github_url.startswith('https://'):
      ipynb_github_url = ipynb_github_url[len('https://'):]
    if ipynb_github_url.startswith('github.com/'):
      ipynb_github_url = ipynb_github_url[len('github.com/'):]
    yield new_markdown_cell(
        '<a href="https://colab.research.google.com/github/{}" target="_parent">'
          '<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" />'
        '</a>'
        .format(ipynb_github_url),
        id='open-in-colab',
    )

  for cell in cells:
    yield cell


def github_samples(inputs):
  GITHUB_SAMPLE_RE = re.compile(
      r'{%\s*github_sample\s+/([^/]+)/([^/]+)/blob/([^/]+)/([\w/.-]+)\s+tag:(\w+)\s*%}')


def code_block(source):
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

  run(
      input_file=args.input_file,
      output_file=args.output_file,
      fatal_errors=args.fatal_errors,
      variables=variables,
      filter_ignore=args.filter_ignore,
      filter_keep=args.filter_keep,
      replace=replace,
      lang=args.lang,
      shell=args.shell,
      start_on_header=args.start_on_header,
      imports=imports,
      docs_url=args.docs_url,
      docs_logo_url=args.docs_logo_url,
      ipynb_github_url=args.ipynb_github_url,
      notebook_title=args.notebook_title,
      kernel=args.kernel,
  )


DEFAULT_STEPS = [
    read_lines,
    html_to_markdown,
    jinja_variables,
    lines_to_paragraphs,
    re_filter,
    re_replace,
    language,
    paragraphs_to_sections,
    imports,
]

DEFAULT_STEPS_POST = [
    flatten,
    paragraphs_to_cells,
    view_the_docs,
    open_in_colab,
]

if __name__ == '__main__':
  main()
