---
layout: section
title: "Home"
permalink: /index/
---
<!--
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

<!-- Comments --> and anything before the first header is not rendered into the
output notebook by default.

# Hello World!

This is a simple markdown page with GitHub code snippets.
All this will be translated into a Jupyter notebook using the desired language.

## Example

Here is a code sample:

<!-- This is equivalent to either the {: .py} or {: .language-py} classes -->
```py
{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py tag:hello_world %}
```

{: .output}
<!-- The `output` class will be ignored in the notebook -->
Output:

{: .output}
```
Hello from Python!
```

{: .language-py}
<table>
  <td>
    <a target="_blank" class="button"
        href="https://colab.research.google.com/github//davidcavazos/md2ipynb/blob/master/examples/notebooks/hello-world-py.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px" />
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button"
        href="https://github.com//davidcavazos/md2ipynb/blob/master/examples/code/hello-world.py">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px" />
      View on GitHub
    </a>
  </td>
</table>
<br>

```java
{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/HelloWorld.java tag:hello_world %}
```

{: .output}
Output:

{: .output}
```
Hello from Java!
```

{: .language-java}
<table>
  <td>
    <a target="_blank" class="button"
        href="https://colab.research.google.com/github//davidcavazos/md2ipynb/blob/master/examples/notebooks/hello-world-java.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px" />
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button"
        href="https://github.com//davidcavazos/md2ipynb/blob/master/examples/code/HelloWorld.java">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px" />
      View on GitHub
    </a>
  </td>
</table>
<br>

```go
{% github_sample /davidcavazos/md2ipynb/blob/master/examples/code/hello-world.go tag:hello_world %}
```

{: .output}
Output:

{: .output}
```
Hello from Java!
```

{: .language-go}
<table>
  <td>
    <a target="_blank" class="button"
        href="https://colab.research.google.com/github/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello-world-go.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px" />
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button"
        href="https://github.com/davidcavazos/md2ipynb/blob/master/examples/code/hello-world.go">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px" />
      View on GitHub
    </a>
  </td>
</table>
<br>

You are all done!

<h2>HTML Section</h2>

<p>HTML is also supported since Markdown is a superset of HTML</p>

## Form view

In "form view", a code cell's contents will be hidden by default in
[Colab](https://colab.research.google.com).
You can open and close the contents by double clicking it.

```
#@title A code cell containing `#@title`
# Contents will be hidden in Colab
```

Or, a code cell containing `#@param`.

```
message = "Hello!" #@param {type:"string"}
```

## What's next

Check the [README.md](https://github.com/davidcavazos/md2ipynb/blob/master/README.md) for more instructions.
