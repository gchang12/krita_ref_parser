
from PIL import Image

from _logging import logger

if __name__ == "__main__":
    filename = "images/.test.png"
    half_image = halve_image(filename, get_first_half=False)

