# md2ipynb

Markdown to Jupyter Notebook converter.

## Setup

### [optional] Virtual environment

Make sure you have `virtualenv` installed.

```sh
pip install -U virtualenv
```

Create and activate a new `virtualenv`.

```sh
python -m virtualenv env
source env/bin/activate
```

> **Note**: Once you are all done, you can deactivate it by running `deactivate`.

### Installation

The easiest way to install is through `pip`.

```sh
pip install -U md2ipynb
```

### Example data

Now, to get some example data, we'll clone the repository.

```sh
# Clone the repository just to have access to the examples.
git clone git@github.com:davidcavazos/md2ipynb.git
cd md2ipynb
```

> *Note:* If you make modifications to the source code and want to use that,
> you can install it in "editable" (development) mode.
>
> ```sh
> pip install -e .
> ```
>
> For more information, see the [Contribution guide](CONTRIBUTING.md).

Installing the `md2ipynb` module will also install the `md2ipynb` command line tool.
For custom preprocessing steps or integration with Python scripts,
it is also available by importing the `md2ipynb` module from any Python script.

## Minimal example

* source: [hello.md](examples/pages/hello.md)
* code: [hello-world.py](examples/code/hello-world.py)

Here is a minimal example on how to convert a Markdown file.
By default, the output is printed into `stdout`.

```sh
md2ipynb examples/pages/hello.md
```

You can also specify an output path with the `-o` or `--output` option.

```sh
md2ipynb examples/pages/hello.md -o examples/notebooks/hello.ipynb
```

Here is the generated notebook on Colab and GitHub.

<table>
  <td>
    <a target="_blank" class="button" href="https://colab.research.google.com/github/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello-minimal.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px"/>
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button" href="https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello-minimal.ipynb">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px"/>
      View on GitHub
    </a>
  </td>
</table>

## Example

* source: [hello.md](examples/pages/hello.md)
* code: [hello-world.py](examples/code/hello-world.py)
* import: [license.md](examples/templates/license.md)
* import: [setup-py.md](examples/templates/setup-py.md)
* import: [cleanup.md](examples/templates/cleanup.md)

Here is a more complete example on specifying an output path, import sections,
variables, as well as more metadata for a Colab visualization.

```sh
md2ipynb examples/pages/hello.md \
    -o examples/notebooks/hello.ipynb \
    --imports examples/templates/license.md:0 \
              examples/templates/setup-py.md:1 \
              examples/templates/cleanup.md:-2 \
    --var package=md2ipynb \
          end_message="You're all done 🎉🎉" \
    --notebook-title 'Hello md2ipynb!' \
    --docs-url https://github.com/davidcavazos/md2ipynb \
    --docs-logo-url https://www.tensorflow.org/images/GitHub-Mark-32px.png \
    --github-ipynb-url https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello.ipynb
```

> *Note:* For more information on the available options, run `md2ipynb --help`.

Here is the generated notebook on Colab and GitHub.
Note that since we specified the `--github-ipynb-url`,
there is now an "Open in Colab" button in the GitHub ipynb file.

<table>
  <td>
    <a target="_blank" class="button" href="https://colab.research.google.com/github/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px"/>
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button" href="https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello.ipynb">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px"/>
      View on GitHub
    </a>
  </td>
</table>

## Python example

* source: [hello.md](examples/pages/hello.md)
* code: [hello-world.py](examples/code/hello-world.py)
* import: [license.md](examples/templates/license.md)
* import: [setup-py.md](examples/templates/setup-py.md)
* import: [cleanup.md](examples/templates/cleanup.md)

The following example shows how to use `md2ipynb` as a Python module.
This example shows how to specify custom preprocessing steps, import sections,
use variables, as well as more metadata for a Colab visualization.

```py
import md2ipynb

def add_separators(paragraphs):
  for p in paragraphs:
    yield '---'
    yield p
  yield '---'

def replace(paragraphs, old, new):
  for p in paragraphs:
    yield p.replace(old, new)

# Create a new IPython notebook.
notebook = md2ipynb.new_notebook(
    input_file='examples/pages/hello.md',
    imports={
        0: ['examples/templates/license.md'],
        1: ['examples/templates/setup-py.md'],
        -1: ['examples/templates/cleanup.md'],
    },
    variables={
        'package': 'md2ipynb',
        'end_message': "You're all done 🎉🎉",
    },
    notebook_title='Hello md2ipynb!',
    docs_url='https://github.com/davidcavazos/md2ipynb',
    docs_logo_url='https://www.tensorflow.org/images/GitHub-Mark-32px.png',
    github_ipynb_url='https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello.ipynb',

    # Additional steps can be run in the order specified.
    # If the generator receives multiple arguments, they can be passed as a tuple.
    steps=[
        add_separators,
        (replace, 'Hello', 'Hi'),
    ],
)

# Write the notebook to a file.
import nbformat

with open('examples/notebooks/hello-custom.ipynb', 'w') as f:
  nbformat.write(notebook, f)
```

Here is the generated notebook on Colab and GitHub.

<table>
  <td>
    <a target="_blank" class="button" href="https://colab.research.google.com/github/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello-custom.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px"/>
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button" href="https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/hello-custom.ipynb">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px"/>
      View on GitHub
    </a>
  </td>
</table>

## Contributing

Contributions are welcome! For instructions on how to contribute,
please check the [Contribution guide](CONTRIBUTING.md).
