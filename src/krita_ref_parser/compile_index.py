"""
"""

from pathlib import Path

from bs4 import BeautifulSoup

from krita_ref_parser.amputate_images import SampleImageType

SOURCE_DIR = "./output/raw-excerpts/"
TARGET_DIR = "./output/"

PILCROW = "¶"
# TODO: Index
# - (directory, filename, header, hero-image=null, figures=null)

def compile_directories(*, source_dir: str = SOURCE_DIR):
    """
    """
    directories = map(
        lambda path: path.name,
        filter(lambda path: path.is_dir(), Path(source_dir).iterdir()),
    )
    return set(directories)

def compile_filenames(source_subdir: str):
    """
    """
    files = map(
        lambda path: path.name,
        filter(lambda path: path.is_file(), Path(source_subdir).iterdir()),
    )
    return set(files)

def get_header(soup: BeautifulSoup, *, level):
    """
    """
    h_tag = "h%d" % level
    h_text = soup.find(h_tag).text
    return h_text[:h_text.index(PILCROW)]

def get_hero_image(soup: BeautifulSoup):
    """
    """
    try:
        img_src = Path(soup.find("img")['src']).name
    except TypeError:
        img_src = None
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
    return (figures if figures else None)

if __name__ == "__main__":
    import json
    import shutil
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
