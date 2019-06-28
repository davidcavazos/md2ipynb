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

from docs_nbgen import *



class DocsNbGenTest(unittest.TestCase):
  # run_steps
  def test_run(self):
    def lowercase(lines, **kwargs):
      for line in lines:
        yield line.lower()

    def remove(lines, text='Hello', **kwargs):
      for line in lines:
        yield line.replace(text, '')

    actual = list(run_steps(
        inputs=['Hello World', 'Say hello'],
        steps=[remove, lowercase],
    ))
    expected = [' world', 'say hello']
    self.assertEqual(actual, expected)

  def test_run_order(self):
    def lowercase(lines, **kwargs):
      for line in lines:
        yield line.lower()

    def remove(lines, text='Hello', **kwargs):
      for line in lines:
        yield line.replace(text, '')

    actual = list(run_steps(
        inputs=['Hello World', 'Say hello'],
        steps=[lowercase, remove],
        text='hello',
    ))
    expected = [' world', 'say ']
    self.assertEqual(actual, expected)

  # read_lines
  def test_read_lines_from_filename(self):
    actual = list(read_lines('test/read_lines.md'))
    expected = ['line 1  \n', '\n', 'line 2  \n', 'line 3  \n']
    self.assertEqual(actual, expected)

  def test_read_lines_from_file_object(self):
    with open('test/read_lines.md') as f:
      actual = list(read_lines(f))
    expected = ['line 1  \n', '\n', 'line 2  \n', 'line 3  \n']
    self.assertEqual(actual, expected)

  def test_read_lines_from_iterator(self):
    actual = list(read_lines(['line {}'.format(i+1) for i in range(3)]))
    expected = ['line 1', 'line 2', 'line 3']
    self.assertEqual(actual, expected)

  # html_to_markdown
  def test_html_to_markdown_headers(self):
    actual = list(html_to_markdown(['<h3>H3</h3>\n', '  <h3>   H3   </h3>  \n']))
    expected = ['### H3', '### H3']
    self.assertEqual(actual, expected)

  def test_html_to_markdown_code_blocks(self):
    actual = list(html_to_markdown([
        '<pre>code 1</pre>\n',
        '<pre class="py">code 2</pre>\n',
        'line 1<pre class="py js" custom-attribute="value" >\n',
        'code 3\n',
        '</pre>line 2\n',
    ]))
    expected = [
        '```',
        'code 1',
        '```',
        '',
        '```py',
        'code 2',
        '```',
        '',
        'line 1',
        '',
        '```py js',
        '',
        'code 3',
        '',
        '```',
        'line 2',
    ]
    self.assertEqual(actual, expected)

  def test_html_to_markdown_headers_in_code_blocks(self):
    actual = list(html_to_markdown([
        '```\n',
        '<h1>H1</h1>\n',
        '```\n',
        '<pre><h1>H1</h1></pre>\n',
    ]))
    expected = [
        '```',
        '<h1>H1</h1>',
        '```',
        '',
        '```',
        '<h1>H1</h1>',
        '```',
    ]
    self.assertEqual(actual, expected)

  # jinja_variables
  def test_jinja_variables(self):
    actual = list(jinja_variables(
        lines=['{{x}}2', '{{   x   }}2', '{{undefined}}'],
        variables={'x': 4},
    ))
    expected = ['42', '42', '{{undefined}}']
    self.assertEqual(actual, expected)

  def test_jinja_variables_fatal_errors(self):
    with self.assertRaises(NameError):
      list(jinja_variables(
          lines=['{{undefined}}'],
          fatal_errors=True,
      ))

  # lines_to_paragraphs
  def test_lines_to_paragraphs(self):
    actual = list(lines_to_paragraphs([
        '# H1',
        'line 1',
        'line 2',
        '```',
        'code 1',
        'code 2',
        '```',
        'line 3',
    ]))
    expected = [
        '# H1',
        'line 1\nline 2',
        '```\ncode 1\ncode 2\n```',
        'line 3',
    ]
    self.assertEqual(actual, expected)

  def test_lines_to_paragraphs_spaced(self):
    actual = list(lines_to_paragraphs([
        '', '', '# H1',
        '', '', 'line 1',
        '', '', 'line 2',
        '', '', '```',
        '', '', 'code 1',
        '', '', 'code 2',
        '', '', '```',
        '', '', 'line 3',
        '', '',
    ]))
    expected = [
        '# H1',
        'line 1',
        'line 2',
        '```\n\n\ncode 1\n\n\ncode 2\n\n\n```',
        'line 3',
    ]
    self.assertEqual(actual, expected)

  # re_filter
  def test_re_filter_ignore(self):
    actual = list(re_filter(
        paragraphs=[
            '# H1',
            'line 1',
            '```py\ncode1\n```',
            '```js\ncode2\n```',
        ],
        filter_ignore=r'^```js',
    ))
    expected = ['# H1', 'line 1', '```py\ncode1\n```']
    self.assertEqual(actual, expected)

  def test_re_filter_ignore_multi(self):
    actual = list(re_filter(
        paragraphs=[
            '# H1',
            'line 1',
            '```py\ncode1\n```',
            '```js\ncode2\n```',
        ],
        filter_ignore=[r'^```js', r'^#'],
    ))
    expected = ['line 1', '```py\ncode1\n```']
    self.assertEqual(actual, expected)

  def test_re_filter_keep(self):
    actual = list(re_filter(
        paragraphs=[
            '# H1',
            'line 1',
            '```py\ncode1\n```',
            '```js\ncode2\n```',
        ],
        filter_ignore=r'^```\w+',
        filter_keep=r'^```py',
    ))
    expected = ['# H1', 'line 1', '```py\ncode1\n```']
    self.assertEqual(actual, expected)

  def test_re_filter_keep_multi(self):
    actual = list(re_filter(
        paragraphs=[
            '# H1',
            'line 1',
            '```py\ncode1\n```',
            '```js\ncode2\n```',
        ],
        filter_ignore=[r'^```\w+', r'^#'],
        filter_keep=[r'```py', r'H1']
    ))
    expected = ['# H1', 'line 1', '```py\ncode1\n```']
    self.assertEqual(actual, expected)

  # re_replace
  def test_re_replace(self):
    actual = list(re_replace(
        paragraphs=[
            '# H1',
            'Line 1\nline 2',
            '```\ncode 1\n```',
        ],
        replace={
            r'^```(.*)```$': r'code {\1}',
            r'^#\s*(.*)': r'<h1>\1</h1>',
        },
    ))
    expected=['<h1>H1</h1>', 'Line 1\nline 2', 'code {\ncode 1\n}']
    self.assertEqual(actual, expected)

  def test_re_replace_count(self):
    actual = list(re_replace(
        paragraphs=[
            '# H1',
            'Line 1\nline 2',
            '```\ncode 1\n```',
        ],
        replace={r'\w+ \d': '___'},
        replace_count=1,
    ))
    expected=['# H1', '___\nline 2', '```\n___\n```']
    self.assertEqual(actual, expected)

  # language
  def test_language_markdown(self):
    actual = list(language(
        paragraphs=[
            'line 1',
            '{:.language-js}\nJavascript text',
            '{:.language-py}\nPython text',
            '{:.language-go}\nGo text',
            'line 2',
        ],
        lang='py',
    ))
    expected = [
        'line 1',
        'Python text',
        'line 2',
    ]
    self.assertEqual(actual, expected)

  def test_language_code_py(self):
    actual = list(language(
        paragraphs=[
            'line 1',
            '```js\n# Hello\n```',
            '```py\n# Hello\n```',
            '```go\n// Hello\n```',
            'line 2',
        ],
        lang='py',
    ))
    expected = [
        'line 1',
        '```py\n# Hello\n```',
        'line 2',
    ]
    self.assertEqual(actual, expected)

  # paragraphs_to_sections
  def test_paragraphs_to_sections(self):
    actual = list(paragraphs_to_sections([
        'line 0',
        '# H1',
        'line 1\nline 2',
        '```\ncode 1\ncode 2\n```',
        'line 3',
        '## H2',
        'line 4',
        '```\ncode 3\n```',
    ]))
    expected = [
        [
            '# H1',
            'line 1\nline 2',
            '```\ncode 1\ncode 2\n```',
            'line 3',
        ],
        [
            '## H2',
            'line 4',
            '```\ncode 3\n```',
        ],
    ]
    self.assertEqual(actual, expected)

  def test_paragraphs_to_sections_start_on_header(self):
    actual = list(paragraphs_to_sections(
        paragraphs=[
            'line 0',
            '# H1',
            'line 1\nline 2',
        ],
        start_on_header=False,
    ))
    expected = [['line 0'], ['# H1', 'line 1\nline 2']]
    self.assertEqual(actual, expected)

  # imports
  def test_imports_at_start(self):
    actual = list(imports(
        sections=['section 1', 'section 2'],
        imports={
            0: ['title', 'start'],
            1: ['section 1.1'],
        },
    ))
    expected = ['title', 'start', 'section 1', 'section 1.1', 'section 2']
    self.assertEqual(actual, expected)

  def test_imports_at_end(self):
    actual = list(imports(
        sections=['section 1', 'section 2'],
        imports={
            -1: ['end', ':)'],
            -2: ['section 1.1'],
        },
    ))
    expected = ['section 1', 'section 1.1', 'section 2', 'end', ':)']
    self.assertEqual(actual, expected)

  def test_imports_with_steps(self):
    def lowercase(inputs, **kwargs):
      yield inputs.lower()

    actual = list(imports(
        sections=['Section 1', 'Section 2'],
        imports={0: ['TITLE']},
        steps=[lowercase],
    ))
    expected = ['title', 'Section 1', 'Section 2']
    self.assertEqual(actual, expected)

  # flatten
  def test_flatten(self):
    actual = list(flatten([['A'], ['B', 'C'], ['D']]))
    expected = ['A', 'B', 'C', 'D']
    self.assertEqual(actual, expected)

  # paragraphs_to_cells
  def test_paragraphs_to_cells(self):
    actual = list(paragraphs_to_cells([
        'line 0',
        '# H1',
        'line 1\nline 2',
        '```\ncode 1\n```',
        'line 3',
        '## H2',
        'line 4\nline 5',
        '```\ncode 2\n```',
        '```\ncode 3\n```',
    ]))
    expected = [
        new_markdown_cell('line 0'),
        new_markdown_cell('# H1\n\nline 1\nline 2', id='h1'),
        new_code_cell('code 1', id='h1-code'),
        new_markdown_cell('line 3', id='h1-2'),
        new_markdown_cell('## H2\n\nline 4\nline 5', id='h2'),
        new_code_cell('code 2', id='h2-code'),
        new_code_cell('code 3', id='h2-code-2'),
    ]
    self.assertEqual(actual, expected)

  # view_the_docs_cells
  def test_view_the_docs(self):
    actual = list(view_the_docs(
        cells=[new_markdown_cell('content', id='H1')],
        docs_url='www.docs-url.com',
    ))
    expected = [
        new_markdown_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  'View the Docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-top',
        ),
        new_markdown_cell('content', id='H1'),
        new_markdown_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  'View the Docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-bottom',
        ),
    ]
    self.assertEqual(actual, expected)

  def test_view_the_docs_logo(self):
    actual = list(view_the_docs(
        cells=[new_markdown_cell('content', id='H1')],
        docs_url='www.docs-url.com',
        docs_logo_url='www.docs-url.com/logo.png',
    ))
    expected = [
        new_markdown_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  '<img src="www.docs-url.com/logo.png" width="32" height="32" />'
                  'View the Docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-top',
        ),
        new_markdown_cell('content', id='H1'),
        new_markdown_cell(
            '<table align="left">'
              '<td>'
                '<a target="_blank" href="www.docs-url.com">'
                  '<img src="www.docs-url.com/logo.png" width="32" height="32" />'
                  'View the Docs'
                '</a>'
              '</td>'
            '</table>',
            id='view-the-docs-bottom',
        ),
    ]
    self.assertEqual(actual, expected)

  # open_in_colab
  def test_open_in_colab(self):
    actual = list(open_in_colab(
        cells=[new_markdown_cell('content', id='H1')],
        ipynb_github_url='https://github.com/user/repo/blob/master/notebook.ipynb',
    ))
    expected = [
        new_markdown_cell(
            '<a href="https://colab.research.google.com/github/user/repo/blob/master/notebook.ipynb" target="_parent">'
              '<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" />'
            '</a>',
            id='open-in-colab',
        ),
        new_markdown_cell('content', id='H1'),
    ]
    self.assertEqual(actual, expected)


if __name__ == '__main__':
  unittest.main()
