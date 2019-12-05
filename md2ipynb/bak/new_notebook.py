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
import md2ipynb
import nbformat


def new_notebook(
    input_file,
    variables=None,
    imports=None,
    include_dir=None,
    notebook_title=None,
    keep_classes=None,
    filter_classes=None,
    shell=None,
    docs_url=None,
    docs_logo_url=None,
    github_ipynb_url=None,
    kernel='python3',
    steps=None,
    jinja_env=None,
):

  sections = md2ipynb.read.sections(input_file, variables, include_dir, jinja_env)
  paragraphs = md2ipynb.apply(sections, [
      (md2ipynb.steps.imports, imports, variables, include_dir, jinja_env),
      md2ipynb.steps.flatten,
      (md2ipynb.steps.filter_classes, keep_classes, filter_classes),
  ])
  paragraphs = md2ipynb.apply(paragraphs, steps)
  cells = list(md2ipynb.apply(paragraphs, [
      md2ipynb.steps.paragraphs_to_cells,
      (md2ipynb.steps.view_the_docs, docs_url, docs_logo_url),
      (md2ipynb.steps.open_in_colab, github_ipynb_url),
  ]))

  for cell in cells:
    if notebook_title:
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
