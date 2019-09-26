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

import logging
import re

# Format: {: #id .class attrib1='value' attrib2="value" }
attributes_re = re.compile(r'\s*{:(?P<attributes>[^}]*)}\n*')
attrib_re = re.compile(r'''^(?:
    \#(?P<id>[\w-]+)|                                  # #id
    \.(?P<class>[\w-]+)|                               # .class
    (?P<key>[\w-]+)=(?P<q>['"])(?P<value>[\w-]*)(?P=q) # key='value' key="value"
)$''', re.VERBOSE)


def parse_attributes(line):
  m = attributes_re.search(line)
  if not m:
    return None

  result = {}
  raw_attributes = m['attributes'].strip().split()
  for raw_attrib in raw_attributes:
    m = attrib_re.match(raw_attrib)
    if not m:
      logging.warning('invalid attribute syntax: {}'.format(repr(raw_attrib)))
      continue

    if m['id'] is not None:
      result['id'] = m['id']
    elif m['class'] is not None:
      if 'class' not in result:
        result['class'] = []
      result['class'].append(m['class'])
    elif m['key'] is not None and m['value'] is not None:
      result[m['key']] = m['value']

  return result
