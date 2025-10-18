"""
Defines logging configuration.
"""

import logging

logger = logging.getLogger(name="krita_ref_generator")

logging.basicConfig(
    level=logging.INFO,
    filename="krita_ref_generator.log",
    format="%(levelname)s:%(module)s.%(funcName)s: %(message)s",
    filemode="w",
)
