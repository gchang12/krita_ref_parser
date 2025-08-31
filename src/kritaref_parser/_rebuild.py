"""
"""

import logging
from pathlib import Path
from bs4 import BeautifulSoup

def have_anchor_tags_reference_source(excerpt_dir):
    """
    """
    sections = (
        "brush_engines/",
        "tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        "blending_modes/",
    )
    root = "https://docs.krita.org/en"
    logging.debug("Changing a[src] to source where 'internal' in a[class].")
    for section in sections:
        path_to_section = Path(excerpt_dir, section)
        file_count = 0 
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for a in soup.find_all("a"):
                if "internal" not in a['class']:
                    #a['class'].append('external')
                    continue
                a['href'] = root + "/" + a['href'].lstrip('./')
                a['class'].remove('internal')
                a['class'].append('link-to-official-docs')
            htmlfile.write_text(str(soup), encoding='utf-8')
            file_count += 1
        logging.debug("%d files have been modified for '%s'.", file_count, section)

def have_anchor_tags_reference_source2(excerpt_dir):
    """
    """
    sections = (
        "brush_engines/",
        "tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        "blending_modes/",
    )
    root = "https://docs.krita.org/en/"
    logging.debug("Changing a[src] to source where 'internal' in a[class].")
    sectors = ("user_manual", "general_concepts", "tutorials", "KritaFAQ", "contributors_manual", "resources_page")
    for section in sections:
        path_to_section = Path(excerpt_dir, section)
        file_count = 0
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for a in soup.find_all("a"):
                #sector = a['href'].split('/')[4]
                #print(sector)
                #print(sector)
                #print(a['href'])
                #a['href'] = a['href'].replace(root, root + repl)
                if a['href'].startswith("#"):
                    continue
                if "blending_modes" in a['href']:
                    repl = root + "reference_manual/"
                    if "brush_" in section:
                        pattern = "../../"
                    else:
                        pattern = "../"
                    new_href = a['href'].replace(pattern, repl)
                elif "brush_" not in section:
                    if a['href'].startswith("../../"):
                        repl = root
                        new_href = a['href'].replace("../../", repl)
                    else:
                        continue
                elif "brush_" in section:
                    if a['href'].startswith("../../../"):
                        repl = root
                        new_href = a['href'].replace("../../../", repl)
                    else:
                        continue
                else:
                    continue
                if "reference_manual/brush_" in new_href:
                    new_href = new_href.replace("reference_manual/", "reference_manual/brushes/")
                if ".." in new_href:
                    new_href = new_href.replace('..', '')
                #print(new_href)
                a['class'].remove('internal')
                a['class'].append('link-to-official-docs')
                a['href'] = new_href
                a['rel'] = "external"
            htmlfile.write_text(str(soup), encoding='utf-8')
            file_count += 1
        logging.debug("%d files have been modified for '%s'.", file_count, section)

def delete_orphaned_figcaption(excerpt_dir):
    """
    """
    sections = (
        "brush_engines/",
        "tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        "blending_modes/",
    )
    for section in sections:
        path_to_section = Path(excerpt_dir, section)
        file_count = 0
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for figcaption in soup.find_all("figcaption"):
                if figcaption.parent.find("img") is None:
                    figcaption.parent.extract()
            htmlfile.write_text(str(soup), encoding="utf-8")

# specially mark blending mode subsections

def set_rel_attribute(excerpt_dir):
    """
    """
    sections = (
        "brush_engines/",
        "tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        "blending_modes/",
    )
    for section in sections:
        path_to_section = Path(excerpt_dir, section)
        file_count = 0
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for a in soup.find_all("a"):
                if "external" in a['class']:
                    a['class'].remove("external")
                if a['href'].startswith('http'):
                    a['rel'] = "external"
            htmlfile.write_text(str(soup), encoding="utf-8")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
    )
    excerpt_dir = "./frontend/kritaref_palette/public/excerpts/"
    #have_anchor_tags_reference_source(excerpt_dir)
    #have_anchor_tags_reference_source2(excerpt_dir)
    #delete_orphaned_figcaption(excerpt_dir)
    set_rel_attribute(excerpt_dir)

