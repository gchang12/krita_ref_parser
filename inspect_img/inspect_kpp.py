import json

from PIL import Image
from bs4 import BeautifulSoup

# https://docs.krita.org/en/reference_manual/resource_management/paintoppresets.html#structure
# https://docs.krita.org/en/user_manual/loading_saving_brushes.html#section-a-general-information

FILENAME = "brush_file.kpp"

img = Image.open(FILENAME)
with open("brush_file.json", mode="w") as wfile:
    json.dump(img.info, wfile, indent=2)

with open("brush_file.xml", mode="w") as wfile:
    raw_xml = img.info["preset"]
    soup = BeautifulSoup(raw_xml, "html.parser")
    with open("brush_file.xml") as rfile:
        print(soup.prettify(), file=wfile)

