"""
Logging configuration.
"""

import logging

logger = logging.getLogger(name="kritaref_palette")

logging.basicConfig(
    level=logging.DEBUG,
    filename=".kritaref_palette.log",
    format="%(levelname)s:%(module)s.%(funcName)s: %(message)s",
    filemode="w",
)

