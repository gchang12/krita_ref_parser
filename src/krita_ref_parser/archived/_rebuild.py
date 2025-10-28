"""
"""

import json
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

def get_index(filename):
    """
    Returns a dict-object from file.
    """
    with open(filename, encoding="utf-8") as rfile:
        index = json.load(rfile)
    return index

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
    )
    tgt_dir = "./frontend/kritaref_palette/public/excerpts/"
    index = get_index("./static/index.json")
    excerpt_dir = "./frontend/kritaref_palette/public/excerpts/"
    #have_anchor_tags_reference_source(excerpt_dir)
    have_anchor_tags_reference_source2(excerpt_dir)
    delete_orphaned_figcaption(excerpt_dir)
    set_rel_attribute(excerpt_dir)
    have_excerpt_anchors_open_new_tab(excerpt_dir)
    prepend_lines_to_all_section_excerpts(excerpt_dir, index, tgt_dir)

# TODO: For populating 'app/' directory in web interface source

def clean_app_directory(dirname):
    """
    Deletes directories in 'app/*'.
    """
    logging.debug("Deleting directories in: %s", dirname)
    for dirpath in filter(
        lambda path: path.is_dir() and "_templates" not in path.parts,
        Path(dirname).iterdir(),
    ):
        shutil.rmtree(dirpath)

def import_parsed_files(src, tgt):
    """
    Copies parsed files from src to tgt.
    """
    parsed_files = (
        "excerpts/",
        "images/",
        #"index.json",
    )
    for parsed_file in parsed_files:
        path_to_parsed_file = Path(src, parsed_file)
        tgt_file = '/'.join([tgt, parsed_file])
        logging.debug("Trying to remove: %s" % tgt_file)
        try:
            shutil.rmtree(tgt_file)
        except FileNotFoundError:
            logging.info("'%s' not found. Skipping.", tgt_file)
            pass
        shutil.copytree(path_to_parsed_file, tgt_file)
    index_filename = "index.json"
    path_to_parsed_file = Path(src, index_filename)
    tgt_file = '/'.join([tgt, index_filename])
    try:
        logging.debug("Trying to remove: %s" % tgt_file)
        Path(tgt_file).unlink()
    except FileNotFoundError:
        logging.info("'%s' not found. Skipping.", tgt_file)
        pass
    shutil.copy(path_to_parsed_file, tgt_file)

def generate_menu(list_items):
    """
    Generates an HTML string containing a menu.
    """
    return "const menuItems = " + json.dumps(list_items, indent=4) + ";\nexport default menuItems;"

def generate_list_items_for_section_with_icon(section, index):
    """
    Generates list items for a section whose subsections can be
    identified by their icons.
    """
    list_items = list(filter(lambda record_: record_['dir'] == section, index))
    if section == "blending_modes/":
        list_items = list(filter(lambda record_: record_['icon'] is not None, list_items))
    for item in list_items:
        if item['icon'] is None:
            continue
        item['icon'] = item['icon'].lstrip('./').replace('images/', '')
    return list_items

def generate_list_items_for_section_without_icon(section, index):
    """
    Generates list items for a section whose subsections cannot be
    identified by their icons.
    """
    list_items = list(filter(lambda record_: record_['dir'] == section, index))
    return list_items

def generate_menu_for_sections(index, generate_list_items, sections, app_dir):
    """
    Generates HTML files for sections.
    """
    for section in sections:
        # Create directory
        Path(app_dir, section).mkdir(exist_ok=True)
        list_items = generate_list_items(section, index)
        menu = generate_menu(list_items)
        #menu_file = Path(app_dir, section, "menuItems.tsx")
        #logging.debug("Writing to: %s", menu_file)
        #menu_file.write_text(menu, encoding="utf-8")

def generate_menu_for_sections_without_icons(index, app_dir):
    """
    Generates HTML files for sections without icons.
    """
    sections = (
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
    generate_list_items = generate_list_items_for_section_without_icon
    return generate_menu_for_sections(index, generate_list_items, sections, app_dir)

def generate_menu_for_sections_with_icons(excerpt_dir, index, app_dir):
    """
    Generates HTML files for sections with icons.
    """
    sections = (
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
    generate_list_items = generate_list_items_for_section_with_icon
    return generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections, app_dir)

def generate_menu_for_blending_modes_without_dots(excerpt_dir, index, app_dir):
    """
    Generates HTML files for 'blending_modes' section.
    """
    sections = ("blending_modes/",)
    generate_list_items = generate_list_items_for_section_without_icon
    index = filter(lambda record: record['icon'] is None, index)
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/without-icons.css" type="text/css" />')
    generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections, app_dir)
    output_files = (
        #"page.tsx",
        "menuItems.tsx",
    )
    new_dst = Path(app_dir, sections[0], "without-dots")
    new_dst.mkdir(exist_ok=True)
    for file in output_files:
        Path(app_dir, sections[0], file).rename(new_dst.joinpath(file))
    logging.debug("Moved files to: %s", new_dst)

def generate_menu_for_blending_modes_with_dots(excerpt_dir, index, app_dir):
    """
    Generates HTML files for 'blending_modes' dots-subsections.
    """
    index = filter(lambda record: record['icon'] is not None, index)
    section = "blending_modes/"
    list_items = []
    keys = set(["HSX Blending Modes"])
    for record in filter(
        lambda record_: record_['dir'] == section,
        index,
    ):
        #print(record)
        header = record['header']
        try:
            record['icon'] = record['icon'].lstrip('./').replace('images/', '')
        except AttributeError:
            #print(f"'{header}' blending mode has no icon.")
            #icon = "_blending_modes-not-found%d.svg" % key_counter
            #key_counter += 1
            #print(header)
            continue
        if header in keys:
            #print(f"{header} is already in keys.")
            continue
        keys.add(record['header'])
        # TODO: Incorporate this into bm template-function
        list_item = '''<li key="%(header)s" id="%(header)s">
  <div className="title-and-image">
    <h2>%(header)s<input type="checkbox" onClick={moveToQueue} data-header="%(header)s" data-image="%(icon)s" /></h2>
    <img src="/images/%(icon)s" alt="The '%(header)s' blending-mode as applied to dots" width={iconWidth} height={iconHeight} />
  </div>''' % record
        excerpt_text = Path(f"{excerpt_dir}/{section}/{record['file']}") \
            .read_text(encoding="utf-8") \
            .replace('{', '&#123;').replace('}', '&#125;') \
            .replace('class', 'className')
        pattern = 'style="(.*)"'
        repl = ''
        excerpt_text = re.sub(pattern, repl, excerpt_text)
        pattern = 'src="../../images/'
        repl = 'src="/images/'
        excerpt_text = re.sub(pattern, repl, excerpt_text)
        list_items.append(record)
    '''
    target_dir = Path(app_dir, section, "with-dots")
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir.joinpath("menuItems.tsx")
    buffer = "const menuItems = " + json.dumps(list_items, indent=4) + ";\nexport default menuItems;"
    target_file.write_text(buffer, encoding="utf-8")
    #target_file.write_text("\n".join(buffer), encoding="utf-8")
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/without-icons.css" type="text/css" />')
    #prepend_lines_to_section_excerpts(excerpt_dir, section, lines)
    logging.debug("Moved files to: %s", target_dir)
    '''
    json.dump(out_kernel, wfile, indent=4)

def compile_item(root, ref_section, processing_func):
    """
    Compiles list of 4-tuples.
    """
    path_to_source = Path(root, ref_section)
    if path_to_source.is_dir():
        def convert_path_to_headericonhtml(ref_file):
            """
            """
            with open(ref_file, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            header_icon_html = processing_func(soup)
            header, icon, soup = header_icon_html
            #header = header_icon_html[0]
            filename = ref_file.name
            return filename, filename, *header_icon_html
        h_icon_html_list = list(
            map(
                convert_path_to_headericonhtml,
                filter(
                    lambda ref_file: ref_file.is_file(),
                    path_to_source.iterdir(),
                ),
            )
        )
    elif path_to_source.is_file():
        def convert_path_to_headericonhtml(headericonhtml):
            """
            For each HSX section, creates a pseudonym to use as a filename, then returns the object in the ideal format.
            """
            header, icon, soup = headericonhtml
            filename = filename.lower()
            #assert len(filename, header,icon,html) == 4
            return (filename, filename, header, icon, soup)
        with open(path_to_ref, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, "html.parser")
        h_icon_html_list = list(
            map(
                convert_path_to_headericonhtml,
                processing_func(soup),
            ),
        )
    else:
        h_icon_html_list = None
    return h_icon_html_list


def compile_item_from_list(root, ref_section, processing_func):
    """
    Compiles list of 4-tuples.
    """
    path_to_source = Path(root, ref_section)
    h_icon_html_list = []
    def extend_3tuple_list(path, headericonhtml_list):
        """
        Extends local list variable with 4-tuples using pathlib.Path and list[(..., ..., ...)] as arguments.
        """
        filename_root = path.parts[-1]
        for header, icon, html_soup in headericonhtml_list:
            filename = _format_target_filename(filename_root, header)
            h_icon_html_list.append(
                (filename_root, filename, header, icon, html_soup),
            )
    def convert_path_to_headericonhtml(headericonhtml):
        """
        For each HSX section, creates a pseudonym to use as a filename, then returns the object in the ideal format.
        """
        header, icon, soup = headericonhtml
        filename_root = path_to_source.name
        filename = _format_target_filename(filename_root, header)
        return (filename_root, filename, header, icon, soup)
    if path_to_source.is_dir():
        for itemfile in path_to_source.iterdir():
            with open(itemfile, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            extend_3tuple_list(itemfile, processing_func(soup))
    elif path_to_source.is_file():
        with open(path_to_source, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, "html.parser")
        h_icon_html_list.extend(list(map(convert_path_to_headericonhtml, processing_func(soup))))
    else:
        h_icon_html_list = None
    return h_icon_html_list

def compile_items(root, reference_sections):
    """
    Compiles all page items.
    """
    buffer = []
    for ref_section, processing_func in reference_sections.items():
        if "blending_modes/" not in ref_section:
            fileheadericonhtml_list = compile_item(root, ref_section, processing_func)
        else:
            fileheadericonhtml_list = compile_item_from_list(root, ref_section, processing_func)
        if ref_section.count('/') == 1 and "hsx.html" not in ref_section:
            directory = ref_section
        else:
            directory = ref_section.split('/')[-2]
        for value in fileheadericonhtml_list:
            (source, target, header, icon, soup) = value
            #filename = filename.replace('.html', '') + "_" + header.replace(' ', "_") + '.html'
            #filename = filename.lower()
            buffer.append(
                (directory, source, target, header, icon, soup)
            )
    return buffer

