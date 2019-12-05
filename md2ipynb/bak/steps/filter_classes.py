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

from md2ipynb import util

SHELLS = {'sh', 'bash'}


def filter_classes(paragraphs, keep_classes=None, force_filter=None):
  if keep_classes is None:
    keep_classes = {'language-py'}
    keep_classes.update({'shell-' + shell for shell in SHELLS})
  elif isinstance(keep_classes, str):
    keep_classes = {keep_classes}
  else:
    keep_classes = set(keep_classes)

  if force_filter is None:
    force_filter = {}
  elif isinstance(force_filter, str):
    force_filter = {force_filter}
  else:
    force_filter = set(force_filter)

  for paragraph in paragraphs:
    # Check for a paragraph class '{: .class}'.
    attributes = util.parse_attributes(paragraph) or {}
    if 'class' in attributes:
      if force_filter and len(set(attributes['class']) & force_filter) > 0:
        continue
      if len(set(attributes['class']) & keep_classes) == 0:
        continue
      paragraph = util.attributes_re.sub('', paragraph).strip('\n')

    # Check for a code block '```class' both as 'class' and 'language-class'.
    if paragraph.startswith('```') and paragraph.endswith('```'):
      lines = paragraph.splitlines()
      lang = lines[0].lstrip('`').strip()
      possible_classes = {lang, 'language-' + lang, 'shell-' + lang}
      if lang and not keep_classes.intersection(possible_classes):
        continue
      if lang in SHELLS:
        for i in range(1, len(lines)-1):
          lines[i] = '!' + lines[i]
        paragraph = '\n'.join(lines)

    # If we're still here and the paragraph is not empty, yield it.
    if paragraph:
      yield paragraph
