#!/usr/bin/env python

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

import argparse

import nbformat
import os

from . import new_notebook


def main(argv=None):
  parser = argparse.ArgumentParser()

  # Required arguments.
  parser.add_argument('input_file', help='Path to the markdown file to convert')

  # Optional arguments.
  parser.add_argument(
      '-o', '--output_file',
      help='Path of the output notebook to write.',
  )

  parser.add_argument(
      '--var',
      type=lambda value: value.split(':', 1),
      nargs='+',
      help='Sets a variable in the format "name:value".',
  )

  parser.add_argument(
      '--imports',
      type=lambda value: value.split(':', 1),
      nargs='+',
      help='File(s) to import at a certain section index. '
           'Sections are delimited by headers. '
           'Negative indices start from the last section. '
           'Must be in the format "path/to/file.md:index"'
           'Examples: "templates/setup.md:0" "templates/cleanup.md:-1"',
  )

  parser.add_argument(
      '--notebook-title',
      help='Notebook title to show on Colab.',
  )

  parser.add_argument(
      '--lang',
      help='Language to include for code blocks.',
  )

  parser.add_argument(
      '--lang-shell',
      nargs='+',
      help='Shell command language(s) to include for code blocks '
           'as regular expressions.',
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
      '--github-ipynb-url',
      help='GitHub URL of the ipynb file for the "Open in Colab" button.',
  )

  parser.add_argument(
      '--kernel',
      help='Notebook kernel to use, defaults to "python3".',
  )

  args = parser.parse_args()

  try:
    variables = dict(args.var or [])
  except ValueError:
    parser.error('variables must be in the format "name:value", '
                 'use --help for more information.')

  try:
    imports = {}
    for path, index in args.imports or []:
      index = int(index)
      if index not in imports:
        imports[index] = []
      imports[index].append(path)
  except ValueError:
    parser.error('imports must be in the format "path/to/file.md:index", '
                 'use --help for more information.')

  notebook = new_notebook(
      args.input_file,
      variables=variables,
      imports=imports,
      notebook_title=args.notebook_title,
      lang=args.lang,
      lang_shell=args.lang_shell,
      docs_url=args.docs_url,
      docs_logo_url=args.docs_logo_url,
      github_ipynb_url=args.github_ipynb_url,
      kernel=args.kernel,
  )

  if args.output_file:
    with open(args.output_file, 'w') as f:
      nbformat.write(notebook, f)
  else:
    print(nbformat.writes(notebook))


if __name__ == '__main__':
  main()
