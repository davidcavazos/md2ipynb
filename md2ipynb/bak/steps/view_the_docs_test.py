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

import nbformat
import unittest

from . import view_the_docs


def md_cell(source, id=''):
  return nbformat.v4.new_markdown_cell(source, metadata={'id': id})


def code_cell(source, id=''):
  return nbformat.v4.new_code_cell(source, metadata={'id': id})


class ViewTheDocsTest(unittest.TestCase):
  def test_view_the_docs(self):
    expected = [
        md_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  'View the docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-top',
        ),
        md_cell('content', id='H1'),
        md_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  'View the docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-bottom',
        ),
    ]
    actual = list(view_the_docs(
        cells=[md_cell('content', id='H1')],
        docs_url='www.docs-url.com',
    ))
    self.assertEqual(expected, actual)

  def test_view_the_docs_logo(self):
    expected = [
        md_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  '<img src="www.docs-url.com/logo.png" width="32" height="32" />'
                  'View the docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-top',
        ),
        md_cell('content', id='H1'),
        md_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  '<img src="www.docs-url.com/logo.png" width="32" height="32" />'
                  'View the docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-bottom',
        ),
    ]
    actual = list(view_the_docs(
        cells=[md_cell('content', id='H1')],
        docs_url='www.docs-url.com',
        docs_logo_url='www.docs-url.com/logo.png',
    ))
    self.assertEqual(expected, actual)
