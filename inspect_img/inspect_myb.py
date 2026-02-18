"""
"""

import json

from PIL import Image
from bs4 import BeautifulSoup

FILENAME = "brush_file.myb"

img = Image.open(FILENAME)
with open("myb.json", mode="w") as wfile:
    json.dump(img.info, wfile, indent=2)

with open("myb.xml", mode="w") as wfile:
    raw_xml = img.info["preset"]
    soup = BeautifulSoup(raw_xml, "html.parser")
    with open("myb.xml") as rfile:
        print(soup.prettify(), file=wfile)
