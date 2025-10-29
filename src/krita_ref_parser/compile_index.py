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

    def validate_directory_set(dirname):
        """
        """
        logger.info("Validating: An index file exists for each directory in '%s'.", dirname)
        detect_index_files_for_directories(dirname)
        logger.info("Success!")

    # SOURCE_DIR
    #compile_and_validate_directory_set(SOURCE_DIR)
    # {'resource_management', 'blending_modes', 'dockers', 'filters', 'layers_and_masks', 'brushes', 'preferences', 'tools', 'main_menu'}
    # index files exist: YES

    # compile index for sections without icons
    SECTIONS_WITHOUT_ICONS = (
        #"brush_engines/",
        #"tools/",
        #"brushes",
        "brushes/brush_settings",
        "dockers",
        "filters",
        "layers_and_masks",
        "layers_and_masks/fill_layer_generators",
        "main_menu",
        "preferences",
        "resource_management",
        #"blending_modes/",
    )

    sections_to_search = SECTIONS_WITHOUT_ICONS
    level = 1

    index = []
    def walk_entry_is_in_section(dirpathdirnamesfilenames):
        """
        """
        dirpath, dirnames, filenames = dirpathdirnamesfilenames
        content_path = "/".join(dirpath.parts[2:])
        return content_path in sections_to_search
    for dirpath, dirnames, filenames in filter(
        lambda dirpathdirnamesfilenames: not dirpathdirnamesfilenames[1],
        filter(walk_entry_is_in_section, Path(SOURCE_DIR).walk()),
    ):
        validate_directory_set(dirpath)
        path_root = list(dirpath.parts[2:])
        for filename in filenames:
            #path = path_buf.copy()
            #path.append(filename)
            # path: DONE
            filepath = Path(dirpath, filename)
            filetext = filepath.read_text(encoding="utf-8")
            soup = BeautifulSoup(filetext, "html.parser")
            header = get_header(soup, level=level)
            # header: DONE
            icon = get_hero_image(soup)
            # icon: DONE
            figures = get_figures(soup)
            # figures: DONE
            article = {
                "path": path_root + [filename],
                "header": header,
                "icon": icon,
                "figures": figures,
            }
            index.append(article)
        logger.info("Extracted data for (%d) sections from '%s'.", len(filenames), dirpath)
    logger.info("Returning index of length: %d", len(index))
    #return index

    # compile index for sections with icons
    with_icons = (
        "tools",
        "brushes/brush_engines",
        #"brushes",
        #"brushes/brush_settings",
        #"dockers/",
        #"filters/",
        #"layers_and_masks/",
        #"main_menu/",
        #"preferences/",
        #"resource_management/",
        #"blending_modes/",
    )
    # compile index for 'blending_modes/' section
