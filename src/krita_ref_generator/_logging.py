"""
Logging configuration.
"""

import logging

logger = logging.getLogger(name="krita_ref_generator")

logging.basicConfig(
    level=logging.DEBUG,
    #filename=".kritaref_palette.log",
    format="%(levelname)s:%(module)s.%(funcName)s: %(message)s",
    filemode="w",
)

