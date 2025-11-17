"""
Extracts raw excerpts from HTML copy of Krita documentation and splits them into files in the desired filetree.
"""

import re
from pathlib import Path

from bs4 import BeautifulSoup

from krita_ref_parser._logging import logger

PILCROW = "¶"

SOURCE_DIR = "./input/docs-krita-org/_build/html/reference_manual/"
TARGET_DIR = "./output/raw-excerpts/"

def split_from_page(soup: BeautifulSoup):
    """
    """
    sections = [soup.css.select_one("section[id]")]
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def split_from_blendingmodes_page(soup: BeautifulSoup):
    """
    """
    sections = list(soup.css.select("section[id] > section[id]"))
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def split_from_hsx_blendingmodes_page(soup: BeautifulSoup):
    """
    """
    sections = list(soup.css.select("#hsx-blending-modes > section[id]"))
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def write_stripped_soup(soup: BeautifulSoup, filename: str):
    """
    """
    logger.debug("Writing lines to '%s'. Calculating number of lines.", filename)
    soup_as_lines = [line.strip() for line in str(soup).splitlines() if line.strip()]
    soup_as_str = "\n".join(soup_as_lines)
    num_lines = len(soup_as_lines)
    logger.debug("(%d) lines were found in soup. Writing.", num_lines)
    Path(filename).write_text(soup_as_str, encoding="utf-8") # returns number of bytes written; unneeded.
    logger.debug("Write operation successful.")
    return num_lines

if __name__ == "__main__":

    def create_main_directories_and_indices():
        """
        Creates main directories and their corresponding index files.
        """
        # create folders, then create index files
        num_directories = 0
        for dirpath in filter(lambda path_: path_.is_dir(), Path(SOURCE_DIR).iterdir()):
            target_subdir = Path(TARGET_DIR, dirpath.name)
            index_path = dirpath.with_suffix(".html")
            # check if directory should be made.
            if not index_path.exists():
                logger.warning("'%s' does not exist. Skipping.", index_path)
                continue
            # create folder
            target_subdir.mkdir(exist_ok=True, parents=True)
            logger.debug("'%s' now exists.", target_subdir)
            # create index file
            # - get file content
            soup = BeautifulSoup(index_path.read_text(), 'html.parser')
            section = split_from_page(soup).pop()
            # - declare filename
            target_indexfile = Path(TARGET_DIR, index_path.name)
            # - write
            num_lines = write_stripped_soup(section, target_indexfile)
            logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_indexfile)
            num_directories += 1
        logger.info("Created (%d) directories.", num_directories)

    def populate_main_directories():
        """
        """
        for dirpath in filter(lambda path_: path_.is_dir(), Path(SOURCE_DIR).iterdir()):
            logger.info("Populating '%s'.", dirpath)
            num_files = 0
            for filepath in filter(lambda path_: path_.is_file(), dirpath.iterdir()):
                if not filepath.name.endswith(".html"):
                    logger.warning("'%s' is not an HTML file. Skipping.", filepath)
                    continue
                soup = BeautifulSoup(filepath.read_text(), 'html.parser')
                section = split_from_page(soup).pop()
                target_file = Path(TARGET_DIR, dirpath.name, filepath.name)
                num_lines = write_stripped_soup(section, target_file)
                logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
                num_files += 1
            logger.info("(%d) HTML files have been created.", num_files)

    def populate_main_subdirectories():
        """
        """
        for dir_path in filter(lambda path_: path_.is_dir(), Path(SOURCE_DIR).iterdir()):
            # brushes/
            for subdir_path in filter(lambda path_: path_.is_dir(), dir_path.iterdir()):
                # brush_settings/
                target_subsubdir = Path(TARGET_DIR, dir_path.name, subdir_path.name)
                target_subsubdir.mkdir(exist_ok=True, parents=True)
                logger.info("Populating '%s'.", target_subsubdir)
                num_files = 0
                for filepath in filter(lambda path_: path_.is_file(), subdir_path.iterdir()):
                    if not filepath.name.endswith(".html"):
                        logger.warning("'%s' is not an HTML file. Skipping.", filepath)
                        continue
                    soup = BeautifulSoup(filepath.read_text(), 'html.parser')
                    section = split_from_page(soup).pop()
                    target_file = target_subsubdir.joinpath(filepath.name)
                    num_lines = write_stripped_soup(section, target_file)
                    logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
                    num_files += 1
                logger.info("(%d) HTML files have been created.", num_files)

    def _get_blendingmode_dict():
        """
        """
        blendingmode_dict = {}
        for filepath in filter(lambda path_: path_.is_file() and path_.name != "hsx.html", Path(TARGET_DIR, "blending_modes").iterdir()):
            soup = BeautifulSoup(filepath.read_text(), 'html.parser')
            sections = split_from_blendingmodes_page(soup)
            for section in sections:
                h2_text = section.find("h2").text
                h2_text = h2_text[:h2_text.index(PILCROW)]
                blending_mode = re.sub(r" \((.+?)\)", r"_\1", h2_text.replace(" & ", "_and_").replace(" - ", "_")).replace(" ", "-").lower()
                blendingmode_dict[h2_text] = blending_mode
        import json
        #import tempfile
        #import subprocess
        #with tempfile.NamedTemporaryFile(mode="w", encoding='utf-8') as wfile:
        bm_dict_as_json = json.dumps(blendingmode_dict, indent=4)
        print(bm_dict_as_json)
        #tempfile_name = wfile.name
        #subprocess.run(["vi", tempfile_name])

    def populate_blendingmodes_subdirectories():
        """
        """
        blendingmode_dict = {
            "Luminosity/Shine (SAI)": "luminosity-shine_sai",
            "Copy Red, Green, Blue": "copy_red-green-blue",
            "P-Norm A": "p-norm_a",
            "P-Norm B": "p-norm_b",
            "Addition": "addition",
            "Divide": "divide",
            "Inverse Subtract": "inverse-subtract",
            "Multiply": "multiply",
            "Subtract": "subtract",
            "Divisive Modulo": "divisive-modulo",
            "Divisive Modulo - Continuous": "divisive-modulo_continuous",
            "Modulo": "modulo",
            "Modulo - Continuous": "modulo_continuous",
            "Modulo Shift": "modulo-shift",
            "Modulo Shift - Continuous": "modulo-shift_continuous",
            "Burn": "burn",
            "Easy Burn": "easy-burn",
            "Fog Darken (IFS Illusions)": "fog-darken_ifs-illusions",
            "Darken": "darken",
            "Darker Color": "darker-color",
            "Gamma Dark": "gamma-dark",
            "Linear Burn": "linear-burn",
            "Shade (IFS Illusions)": "shade_ifs-illusions",
            "Freeze": "freeze",
            "Freeze-Reflect": "freeze-reflect",
            "Glow": "glow",
            "Glow-Heat": "glow-heat",
            "Heat": "heat",
            "Heat-Glow": "heat-glow",
            "Heat-Glow and Freeze-Reflect Hybrid": "heat-glow-and-freeze-reflect-hybrid",
            "Reflect": "reflect",
            "Reflect-Freeze": "reflect-freeze",
            "Color Dodge": "color-dodge",
            "Gamma Illumination": "gamma-illumination",
            "Gamma Light": "gamma-light",
            "Hard Light": "hard-light",
            "Lighten": "lighten",
            "Lighter Color": "lighter-color",
            "Linear Dodge": "linear-dodge",
            "Easy Dodge": "easy-dodge",
            "Flat Light": "flat-light",
            "Fog Lighten (IFS Illusions)": "fog-lighten_ifs-illusions",
            "Linear Light": "linear-light",
            "Pin Light": "pin-light",
            "Screen": "screen",
            "Soft Light (Photoshop) & Soft Light SVG": "soft-light_photoshop_and_soft-light-svg",
            "Soft Light (IFS Illusions) & Soft Light (Pegtop-Delphi)": "soft-light_ifs-illusions_and_soft-light_pegtop-delphi",
            "Super Light": "super-light",
            "Tint (IFS Illusions)": "tint_ifs-illusions",
            "Vivid Light": "vivid-light",
            "Allanon": "allanon",
            "Interpolation": "interpolation",
            "Interpolation - 2X": "interpolation_2x",
            "Alpha Darken": "alpha-darken",
            "Behind": "behind",
            "Erase": "erase",
            "Geometric Mean": "geometric-mean",
            "Grain Extract": "grain-extract",
            "Grain Merge": "grain-merge",
            "Greater": "greater",
            "Hard Mix": "hard-mix",
            "Hard Mix (Photoshop)": "hard-mix_photoshop",
            "Hard Mix Softer (Photoshop)": "hard-mix-softer_photoshop",
            "Hard Overlay": "hard-overlay",
            "Normal": "normal",
            "Overlay": "overlay",
            "Parallel": "parallel",
            "Penumbra A": "penumbra-a",
            "Penumbra B": "penumbra-b",
            "Penumbra C": "penumbra-c",
            "Penumbra D": "penumbra-d",
            "Bumpmap": "bumpmap",
            "Combine Normal Map": "combine-normal-map",
            "Copy": "copy",
            "Dissolve": "dissolve",
            "AND": "and",
            "CONVERSE": "converse",
            "IMPLICATION": "implication",
            "NAND": "nand",
            "NOR": "nor",
            "NOT CONVERSE": "not-converse",
            "NOT IMPLICATION": "not-implication",
            "OR": "or",
            "XOR": "xor",
            "XNOR": "xnor",
            "Additive Subtractive": "additive-subtractive",
            "Arcus Tangent": "arcus-tangent",
            "Difference": "difference",
            "Equivalence": "equivalence",
            "Exclusion": "exclusion",
            "Negation": "negation"
        }
        for filepath in filter(lambda path_: path_.is_file() and path_.name != "hsx.html", Path(TARGET_DIR, "blending_modes").iterdir()):
            # brushes/
            blendingmodes_subdir = Path(TARGET_DIR, "blending_modes", filepath.with_suffix("").name) # TARGET_DIR/'blending_modes'/blending_mode_type/
            blendingmodes_subdir.mkdir(exist_ok=True, parents=True)
            logger.info("Populating '%s'.", blendingmodes_subdir)
            soup = BeautifulSoup(filepath.read_text(), 'html.parser')
            sections = split_from_blendingmodes_page(soup)
            num_files = 0
            for section in sections:
                #h2_text = section.find("h2").text
                #h2_text = section.find("h2").text.replace(PILCROW, "")
                #h2_text = h2_text[:h2_text.index(PILCROW)]
                #blending_mode = blendingmode_dict[h2_text]
                blending_mode = section['id']
                target_file = blendingmodes_subdir.joinpath(blending_mode + ".html")
                soup = BeautifulSoup(str(section), 'html.parser')
                num_lines = write_stripped_soup(section, target_file)
                logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
                num_files += 1
            logger.info("(%d) HTML files have been created.", num_files)
        assert len(set(blendingmode_dict.values())) == len(set(blendingmode_dict.keys()))
        logger.info("Filenames are unique.")

    def populate_hsx_blendingmodes_subdirectories():
        """
        """
        hsx_blendingmode_dict = {
            "Color, HSV, HSI, HSL, HSY": "color_hsv-hsi-hsl-hsy",
            "Hue HSV, HSI, HSL, HSY": "hue_hsv-hsi-hsl-hsy",
            "Increase Value, Lightness, Intensity or Luminosity.": "increase-value_lightness-intensity-luminosity",
            "Increase Saturation HSI, HSV, HSL, HSY": "increase-saturation_hsi-hsv-hsl-hsy",
            "Intensity": "intensity",
            "Value": "value",
            "Lightness": "lightness",
            "Luminosity": "luminosity",
            "Saturation HSI, HSV, HSL, HSY": "saturation_hsi-hsv-hsl-hsy",
            "Decrease Value, Lightness, Intensity or Luminosity": "decrease-value_lightness-intensity-luminosity",
            "Decrease Saturation HSI, HSV, HSL, HSY": "decrease-saturation_hsi-hsv-hsl-hsy",
        }
        filepath = Path(TARGET_DIR, "blending_modes", "hsx.html")
        hsx_blendingmode_subdir = filepath.with_suffix("")
        hsx_blendingmode_subdir.mkdir(exist_ok=True, parents=True)
        logger.info("Populating '%s'.", hsx_blendingmode_subdir)
        soup = BeautifulSoup(filepath.read_text(), 'html.parser')
        sections = split_from_hsx_blendingmodes_page(soup)
        num_files = 0
        for section in sections:
            #h3_text = section.find("h3").text
            #h3_text = section.find("h3").text.replace(PILCROW, "")
            #h3_text = h3_text[:h3_text.index(PILCROW)]
            #blending_mode = hsx_blendingmode_dict[h3_text]
            blending_mode = section['id']
            target_file = hsx_blendingmode_subdir.joinpath(blending_mode + ".html")
            soup = BeautifulSoup(str(section), 'html.parser')
            num_lines = write_stripped_soup(section, target_file)
            logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
            num_files += 1
        logger.info("(%d) HTML files have been created.", num_files)

    def split_docs():
        """
        """
        create_main_directories_and_indices()
        print("Created main directories and indices in: '%s'" % TARGET_DIR)
        populate_main_directories()
        print("Populated main directories.")
        populate_main_subdirectories()
        print("Populated main subdirectories.")
        populate_blendingmodes_subdirectories()
        print("Populated blending-mode subdirectories.")
        populate_hsx_blendingmodes_subdirectories()
        print("Populated blending-mode-hsx subdirectory.")

    def inspect_output():
        """
        """
        args = ["vi"]
        root_dir = "output/raw-excerpts"
        filelist = (
            "dockers.html",
            "filters/map.html",
            "brushes/brush_settings/options.html",
            "blending_modes/arithmetic/addition.html",
            "blending_modes/hsx/increase-value_lightness-intensity-luminosity.html",
        )
        for file in filelist:
            args.append("/".join([root_dir, file]))
        import subprocess
        subprocess.run(args)

    split_docs()
    #inspect_output()
    #_get_blendingmode_dict()

