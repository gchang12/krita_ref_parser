"""
Defines functions to return list of objects of the form:
[
  {
    path: [str],
    header: str,
    icon: str|null,
    figures: [{img, figcaption}]|null,
  },
  ...
]
"""

from pathlib import Path

from bs4 import BeautifulSoup

from krita_ref_parser.amputate_images import SampleImageType
from krita_ref_parser._logging import logger

SOURCE_DIR = "./output/raw-excerpts/"
TARGET_DIR = "./output/"

PILCROW = "¶"
# - (directory, filename, header, hero-image=null, figures=null)

def detect_index_files_for_directories(source_dir: str):
    """
    """
    missing_files = []
    for dirpath in filter(
        lambda path: not path.with_suffix(".html").exists(),
        filter(lambda path: path.is_dir(), Path(source_dir).iterdir()),
    ):
        missing_files.append(dirpath)
    if missing_files:
        raise FileNotFoundError("These directories in '%s' lack complementing index files: %r" % (source_dir, missing_files))
    logger.info("All directories in '%s' have complementing index files.", source_dir)

def compile_directories(source_dir: str):
    """
    """
    directories = map(
        lambda path: path.name,
        filter(lambda path: path.is_dir(), Path(source_dir).iterdir()),
    )
    directory_set = set(directories)
    logger.debug("Identified (%d) directories in '%s/'. Returning set of directories as string.", len(directory_set), source_dir)
    return directory_set

def compile_filenames(source_subdir: str):
    """
    """
    files = map(
        lambda path: path.name,
        filter(lambda path: path.is_file(), Path(source_subdir).iterdir()),
    )
    file_set = set(files)
    logger.debug("Identified (%d) files in '.../%s'. Returning set of files as string.", len(file_set), source_subdir)
    return file_set

def get_header(soup: BeautifulSoup, *, level):
    """
    """
    h_tag = "h%d" % level
    h_text = soup.find(h_tag).text
    h_text = h_text[:h_text.index(PILCROW)]
    logger.debug("Returning header: '%s'", h_text)
    return h_text

def get_hero_image(soup: BeautifulSoup):
    """
    """
    try:
        img_src = Path(soup.find("img")['src']).name
        logger.debug("Image found. Returning source: '%s'", img_src)
    except TypeError:
        img_src = None
        logger.debug("No image found. Returning None.")
    return img_src

def get_figures(soup: BeautifulSoup):
    """
    """
    figures = []
    for figure in soup.find_all("figure"):
        img = figure.find('img')['src']
        try:
            figcaption = figure.find('figcaption').text.strip()
            figcaption = figcaption[:figcaption.index(PILCROW)]
        except AttributeError:
            figcaption = None
        fig_as_dict = {
            "img": Path(img).name,
            "figcaption": figcaption,
        }
        figures.append(fig_as_dict)
    if figures:
        logger.debug("(%d) figures found. Returning as dict-list.", len(figures))
        return figures
    logger.debug("No figures found. Returning None.")
    return None

if __name__ == "__main__":
    # Walk file-tree and replicate it in JSON
def detect_index_files_for_directories(source_dir: str):

    import json
    import shutil
    '''
    [
      {
        path: [str],
        header: str,
        icon: str|null,
        figures: [{img, figcaption}]|null,
      },
      ...
    ]
    '''

    INDEX = []

    for dirpath in Path(SOURCE_DIR).iterdir():
        #path = [subdir.name]
        for 

    def get_index(filename):
        """
        Returns a dict-object from file.
        """
        with open(filename, encoding="utf-8") as rfile:
            index = json.load(rfile)
        return index

    def write_index(buffer, index_name):
        """
        Writes directory, filename, header, icon to JSON
        """
        #index_name = "kritaref-index.json"
        def get_fileheadericon(kernel_item):
            """
            Turns 4-tuple into dict
            """
            # expect: 5-tuple of the form: directory, (filename, header, icon, soup)
            directory, source, target, header, icon, _ = kernel_item
            fileheadericon = {
                "dir": directory.rstrip('/') + "/",
                "file": target,
                "header": header,
                "icon": icon,
            }
            return fileheadericon
        out_kernel = list(map(get_fileheadericon, buffer))
        with open(index_name, mode="w", encoding="utf-8") as wfile:
            json.dump(out_kernel, wfile)
