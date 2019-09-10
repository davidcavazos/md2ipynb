# md2ipynb

Markdown to Jupyter Notebook converter.

## Minimal example

* source: [example.md](examples/pages/example.md)
* code: [hello-world.py](examples/code/hello-world.py)

Here is a minimal example on how to convert a Markdown file.
By default, the output is printed into `stdout`.

```sh
md2ipynb examples/pages/example.md
```

You can also specify an output path with the `-o` or `--output` option.

```sh
md2ipynb examples/pages/example.md -o examples/notebooks/example.ipynb
```

Here is the generated notebook on GitHub and Colab.

<table>
  <td>
    <a target="_blank" class="button" href="https://colab.research.google.com/github/davidcavazos/md2ipynb/blob/master/examples/notebooks/example-minimal.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px"/>
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button" href="https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/example-minimal.ipynb">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px"/>
      View on GitHub
    </a>
  </td>
</table>
<br/>

## Example

* source: [example.md](examples/pages/example.md)
* code: [hello-world.py](examples/code/hello-world.py)
* import: [license.md](examples/templates/license.md)
* import: [setup-py.md](examples/templates/setup-py.md)
* import: [cleanup.md](examples/templates/cleanup.md)

Here is a more complete example on specifying an output path, import sections,
variables, as well as more metadata for a Colab visualization.

```sh
md2ipynb examples/pages/example.md \
    -o examples/notebooks/example.ipynb \
    --imports examples/templates/license.md:0 \
              examples/templates/setup-py.md:1 \
              examples/templates/cleanup.md:-2 \
    --var package=md2ipynb \
          end_message="You're all done 🎉🎉" \
    --notebook-title 'Hello md2ipynb!' \
    --docs-url https://github.com/davidcavazos/md2ipynb \
    --docs-logo-url https://www.tensorflow.org/images/GitHub-Mark-32px.png \
    --github-ipynb-url https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/example.ipynb
```

> *Note:* For more information on the available options, run `md2ipynb --help`.

Here is the generated notebook on GitHub and Colab.
Note that since we specified the `--github-ipynb-url`,
there is now an "Open in Colab" button in the GitHub ipynb file.

<table>
  <td>
    <a target="_blank" class="button" href="https://colab.research.google.com/github/davidcavazos/md2ipynb/blob/master/examples/notebooks/example.ipynb">
      <img src="https://www.tensorflow.org/images/colab_logo_32px.png" width="20px" height="20px"/>
      Run in Colab
    </a>
  </td>
  <td style="padding-left:1em">
    <a target="_blank" class="button" href="https://github.com/davidcavazos/md2ipynb/blob/master/examples/notebooks/example.ipynb">
      <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" width="20px" height="20px"/>
      View on GitHub
    </a>
  </td>
</table>
<br/>

## Contributing

Contributions are welcome! For instructions on how to contribute,
please check the [Contribution guide](CONTRIBUTING.md).