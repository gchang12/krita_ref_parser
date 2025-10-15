<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/krita_ref_generator.svg?branch=main)](https://cirrus-ci.com/github/<USER>/krita_ref_generator)
[![ReadTheDocs](https://readthedocs.org/projects/krita_ref_generator/badge/?version=latest)](https://krita_ref_generator.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/krita_ref_generator/main.svg)](https://coveralls.io/r/<USER>/krita_ref_generator)
[![PyPI-Server](https://img.shields.io/pypi/v/krita_ref_generator.svg)](https://pypi.org/project/krita_ref_generator/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/krita_ref_generator.svg)](https://anaconda.org/conda-forge/krita_ref_generator)
[![Monthly Downloads](https://pepy.tech/badge/krita_ref_generator/month)](https://pepy.tech/project/krita_ref_generator)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/krita_ref_generator)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# krita_ref_generator

> Parses Krita Docs sections into HTML files.

For use in Krita Reference Palette, an alternative online interface for perusing the Krita documentation.

# HOW TO USE

## Generate input.
1. Create Python virtual environment and install requirements.
2. Create `input/` directory.
3. Navigate to `input/` and fetch official Krita documentation [source](https://invent.kde.org/documentation/docs-krita-org/) via `git clone https://invent.kde.org/documentation/docs-krita-org.git`.
4. Navigate to `input/docs-krita-org/` and invoke `make html`.

## Generate output.
1. Create `output/` directory.
2. Create `output/excerpts` directory and its contents via `excerpt_generator.py` script.
3. Create `output/image` directory and its contents via `image_generator.py` script.
4. Search for hidden output files.

## 

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
