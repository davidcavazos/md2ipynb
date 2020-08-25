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

# take(x: m<a>, quantifier: Quantifier): [a]
# take(p: Parser<a>, quantifier: Quantifier): Parser<[a]>

# let identifier: Parser<Text> ->
#   for x in letter or char '_'
#   for xs in (alphanum or char '_') .take (AtLeast 0)
#   as Token(x ++ xs .join)

# let a: Integer.. =
#   for x in 1.. .take (AtMost 3)
#   for y in 2.. if y .is_even
#   do (x, y)
