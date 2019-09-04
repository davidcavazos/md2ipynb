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

import md2ipynb


def filter_classes(paragraphs, keep_classes=None):
  if keep_classes is None:
    keep_classes = {'language-py', 'shell-sh'}
  elif isinstance(keep_classes, str):
    keep_classes = {keep_classes}
  else:
    keep_classes = set(keep_classes)

  for paragraph in paragraphs:
    m = md2ipynb.util.class_re.search(paragraph)
    if m:
      paragraph_class = m.group(1)
      if paragraph_class not in keep_classes:
        continue
      paragraph = paragraph.replace(m.group(), '').strip('\n')
    if paragraph:
      yield paragraph