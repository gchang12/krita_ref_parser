"""
Compiles index of documentation entries to include in web interface.
"""

import json

SOURCE_DIR = "../../output/raw-excerpts/"
TARGET_DIR = "../../output/"

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

