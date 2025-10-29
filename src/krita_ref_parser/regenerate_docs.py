"""
Modifies compiled HTML documents and yields various output.
"""

SOURCE_DIR = "./output/raw-excerpts/"
TARGET_DIR = "./output/excerpts/"

#CLASS_FOR_LINKS_TO_OFFICIAL_DOCS = "link-to-official-docs"
PILCROW = "¶"

# TODO:
#- Extract H2 tags.
#- Change image sources
#- Extract images as necessary.
#- Prepend CSS link lines.
#- Mark stuff as external or not.
#- Have links open new tabs.
#- Add CSS classes
#- Delete bad tags.
#- Set CSS 'rel' attribute

def _extract_h_tag(section, *, h_level: int):
    """
    Pops <h[1-6]> tag from HTML soup `section` and returns it.
    """
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
    # extract header tag
    # store filename-header pairs as JSON to be returned
    #logger.debug("Searching for tag: h%d", h_level)
    h = section.find('h%d' % h_level).extract().text
    #logger.debug("Searching for pilcrow in: '%s'", h)
    pilcrow_loc = h.index(PILCROW)
    #logger.debug("Returning: %r", h)
    return h[:pilcrow_loc]

def _reset_anchor_tag_sources(section):
    """
    Sets href for <a> to links s.t. they reference official Krita docs.
    """
    # have all anchor tags reference the actual Krita-Docs website
    # from: '../../'
    # to: 'https://docs.krita.org/en/'
    # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
    # (and add an additional class to this while you're at it)
    external_root = 'https://docs.krita.org/en/'
    #logger.debug("Setting <a> hrefs to reference '%s' instead of '../../'.", external_root)
    for a in filter(lambda a_: "internal" in a_['class'], section.find_all('a')):
        #href_path = a['href'].split('/')
        #a['href'] = external_root + '/'.join(href_path[2:])
        #a['class'].remove("internal")
        #a['class'].append(CLASS_FOR_LINKS_TO_OFFICIAL_DOCS)
        pass

def _extract_dotsimg(section):
    """
    Pops first dots-img tag in a section.
    """
    dotsimg = None
    #logger.debug("Searching for <img> tag where src.endswith('_with_dots.png')")
    for img in section.find_all("img"):
        if img['src'].endswith("_with_dots.png"):
            dotsimg = img.extract()
            #logger.debug("Dots-image found: %s. Returning.", dotsimg)
            break
    return dotsimg

def _replace_img_sources(section, *, levels, img_root="../../images/"):
    """
    Replaces src attributes in <img> tags to match new filetree.
    """
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
    # change all image sources:
    # - from: '../../_images/'
    # - to: './images/'
    #logger.debug("Replacing `img-src` to ./images/`img-src[%d:]`", levels)
    for img in section.find_all("img"):
        img_src = img['src'].split('/')
        #logger.debug("Found `img-src`: %s", img['src'])
        # TODO: Delete leading './'
        new_img_src = img_root + '/'.join(img_src[levels:])
        img['src'] = new_img_src
        #logger.debug("Set `img-src`: %s", new_img_src)

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
                try:
                    a['class'].remove('internal')
                except ValueError:
                    pass
                if 'link-to-official-docs' not in a['class']:
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
                try:
                    a['class'].remove('internal')
                except ValueError:
                    pass
                a['class'].append('link-to-official-docs')
                a['href'] = new_href
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

def have_excerpt_anchors_open_new_tab(excerpt_dir):
    """
    Hacks into anchor tags and changes the 'target' of each one to '_blank'.
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
    logging.debug("Changing a[target='_blank'] for all a.")
    for section in sections:
        path_to_section = Path(excerpt_dir, section)
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for a in soup.find_all("a"):
                a['target'] = "_blank"
            htmlfile.write_text(str(soup), encoding='utf-8')

def prepend_lines_to_section_excerpt(excerpt_dir, section, lines):
    """
    Prepends CSS links to HTML excerpt files.
    """
    for htmlfile in filter(
        lambda filepath: filepath.is_file(),
        Path(excerpt_dir, section).iterdir(),
    ):
        filetext = htmlfile.read_text(encoding='utf-8')
        soup = BeautifulSoup(filetext, 'html.parser')
        if soup.css.select('link[rel="stylesheet"][href][type="text/css"]') is None:
            continue
        new_filetext = lines + filetext.splitlines()
        htmlfile.write_text(
            "\n".join(new_filetext),
            encoding="utf-8",
        )

def prepend_lines_to_all_section_excerpts(excerpt_dir, index, tgt_dir):
    """
    Prepends CSS links to all HTML excerpt files.
    """
    sections_without_icons = (
        #"brush_engines/",
        #"tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        #"blending_modes/",
    )
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/without-icon.css" type="text/css" />',
    ]
    logging.debug("Prepending <link ...> lines to sans-icon sections.")
    for section in sections_without_icons:
        prepend_lines_to_section_excerpt(excerpt_dir, section, lines)
    sections_with_icons = (
        "tools/",
        "brush_engines/",
        #"brush_settings/",
        #"dockers/",
        #"filters/",
        #"layers_and_masks/",
        #"main_menu/",
        #"preferences/",
        #"resource_management/",
        #"blending_modes/",
    )
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/with-icon.css" type="text/css" />',
    ]
    logging.debug("Prepending <link ...> lines to sections with icons.")
    for section in sections_with_icons:
        prepend_lines_to_section_excerpt(excerpt_dir, section, lines)
    bm_index1 = filter(lambda record: record['dir'] == "blending_modes/", index)
    logging.debug("Prepending <link ...> lines to files in 'blending_modes/*'.")
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/without-icon.css" type="text/css" />',
    ]
    for record in filter(lambda record: record['icon'] is None, bm_index1):
        htmlfile = Path(tgt_dir, "blending_modes", record['file'])
        filetext = htmlfile.read_text(encoding='utf-8').splitlines()
        new_filetext = lines + filetext
        htmlfile.write_text(
            "\n".join(new_filetext),
            encoding="utf-8",
        )
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/blending_modes.css" type="text/css" />',
    ]
    #print(list(index))
    bm_index2 = filter(lambda record: record['icon'] is not None and record['dir'] == "blending_modes/", index)
    for record in bm_index2:
        #print(record)
        htmlfile = Path(tgt_dir, "blending_modes", record['file'])
        filetext = htmlfile.read_text(encoding='utf-8').splitlines()
        new_filetext = lines + filetext
        htmlfile.write_text(
            "\n".join(new_filetext),
            encoding="utf-8",
        )

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
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for a in soup.find_all("a"):
                if "internal" not in a['class']:
                    continue
                a['href'] = root + "/" + a['href'].lstrip('./')
            htmlfile.write_text(str(soup), encoding='utf-8')
