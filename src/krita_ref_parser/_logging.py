"""
Defines logging configuration.
"""

import logging

logger = logging.getLogger(name="krita_ref_parser")

logging.basicConfig(
    level=logging.DEBUG,
    filename="krita_ref_parser.log",
    format="%(levelname)s:%(module)s.%(funcName)s: %(message)s",
    filemode="w",
)
