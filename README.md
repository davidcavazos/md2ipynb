# nbgen

Jupyter notebook generator from markdown files and code samples.

```bash
pip install -U -r requirements.txt
```

```bash
python nbgen.py --help
```

```bash
python nbgen.py \
  website/src/examples/transforms/element-wise/keys.md \
  --output-prefix examples/notebooks/transforms/element-wise/keys \
  --github-ipynb-url https://github.com/davidcavazos/beam/blob/notebooks/examples/notebooks/transforms/element-wise/keys-py.ipynb \
  --docs-url https://beam.apache.org/examples/transforms/element-wise/keys/ \
  --docs-logo-url https://beam.apache.org/images/logos/full-color/nameless/beam-logo-full-color-nameless-100.png \
  --variables-prefix site. \
  --imports \
    website/assets/license.md:0 \
    website/assets/setup-py.md:0:py \
    website/assets/setup-java.md:1:java \
    website/assets/setup-go.md:1:go \
    website/assets/cleanup.md:-1
```

  This will generate the following files:
    examples/notebooks/examples/transforms/element-wise/keys-java.ipynb
    examples/notebooks/examples/transforms/element-wise/keys-py.ipynb
    examples/notebooks/examples/transforms/element-wise/keys-go.ipynb
