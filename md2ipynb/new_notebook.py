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

import md2ipynb


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
    md_extensions=None,
):

    doc = md2ipynb.parse_markdown(input_file)
