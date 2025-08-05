"""
Logging configuration.
"""

import logging

logger = logging.getLogger(name="kritaref_parser")

logging.basicConfig(
    level=logging.DEBUG,
    filename=".kritaref_parser.log",
    format="%(levelname)s:%(module)s.%(funcName)s: %(message)s",
    filemode="w",
)


