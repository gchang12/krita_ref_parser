"""
ORDER IN WHICH SCRIPTS MUST BE EXECUTED
1. split_docs.py
2. amputate_images.py
3. compile_index.py
4. regenerate_docs.py
"""

import sys

from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
