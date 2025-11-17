<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/krita_ref_parser.svg?branch=main)](https://cirrus-ci.com/github/<USER>/krita_ref_parser)
[![ReadTheDocs](https://readthedocs.org/projects/krita_ref_parser/badge/?version=latest)](https://krita_ref_parser.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/krita_ref_parser/main.svg)](https://coveralls.io/r/<USER>/krita_ref_parser)
[![PyPI-Server](https://img.shields.io/pypi/v/krita_ref_parser.svg)](https://pypi.org/project/krita_ref_parser/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/krita_ref_parser.svg)](https://anaconda.org/conda-forge/krita_ref_parser)
[![Monthly Downloads](https://pepy.tech/badge/krita_ref_parser/month)](https://pepy.tech/project/krita_ref_parser)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/krita_ref_parser)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# krita_ref_parser

> Parses Krita Docs sections into HTML files.

This builds HTML and image files to be consumed by the Krita Reference Palette.

# HOW TO USE

# NOTE: DEPRECATED

## Generate input.
1. Create Python virtual environment and install requirements.
2. Create `input/` directory.
3. Navigate to `input/` and fetch official Krita documentation [source](https://invent.kde.org/documentation/docs-krita-org/) via `git clone https://invent.kde.org/documentation/docs-krita-org.git`.
4. Navigate to `input/docs-krita-org/` and invoke `make html`.

## Generate output.
1. Create `output/` directory.
2. Create `output/excerpts` directory and its contents via `excerpt_parser.py` script.
3. Create `output/image` directory and its contents via `image_parser.py` script.
4. Search for hidden output files.

> [!NOTE]
> It will suffice to run `make .OUTPUT_FILES` to execute all these steps automatically.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
