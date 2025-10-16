"""
Compiles sections of documentation and saves them as raw HTML.
"""

SOURCE_DIR = "../../input/docs-krita-org/_build/html/reference_manual/"
TARGET_DIR = "../../output/excerpts/"

BLENDINGMODE_LIST = (
    "Color",
    "Hue",
    "Increase",
    "Increase Saturation",
    "Intensity",
    "Value",
    "Lightness",
    "Luminosity",
    "Saturation",
    "Decrease",
    "Decrease Saturation",
)



def _generate_excerpt_with_icon(soup: BeautifulSoup, *, levels, h_level, exclude=()):
    """
    Given a BS object, returns a tuple (header: str, icon: str, section_html: bs4.Tag)
    This function is for pages whose content has icons.
    """
    section = soup.select_one("section[id]")
    _reset_anchor_tag_sources(section)
    h1 = _extract_h_tag(section, h_level=h_level)
    _replace_img_sources(section, levels=levels)
    if section['id'] in exclude:
        icon = None
    else:
        try:
            icon = section.find('img').extract()['src']
        except AttributeError:
            #logger.info("Unable to find 'img' in '%s' section.", h1)
            icon = None
    return (h1, icon, section)

def generate_blendingmodes_excerpt(soup: BeautifulSoup):
    """
    Compiles list of (header, dotsimg-src, html-soup) objects from `soup`.
    This works for all subsections except for HSX.
    """
    sections = []
    #logger.debug("Compiling list of (header, icon, section_html) objects.")
    for section in soup.css.select("section[id]")[1:]:
        _reset_anchor_tag_sources(section)
        _replace_img_sources(section, levels=3)
        try:
            h_tag = _extract_h_tag(section, h_level=2)
        except AttributeError:
            #logger.info("No <h2> tag was found. Getting <h3>.")
            h_tag = _extract_h_tag(section, h_level=3)
        dotsimg = _extract_dotsimg(section)
        if dotsimg is not None:
            dotsimg_src = dotsimg['src']
        else:
            dotsimg_src = None
        #logger.debug("Header: %s, Dots-Image: %s, Section.Length: %d", h_tag, dotsimg_src, len(section))
        sections.append((h_tag, dotsimg_src, section))
    #logger.debug("(%d) sections found in soup.", len(sections))
    return sections

def generate_hsx_blendingmode_excerpt(soup: BeautifulSoup):
    """
    Compiles list of (header, dotsimg-src, html-soup) objects from `soup`.
    This works only for the HSX subsections.
    """
    # I L V Y
    # the usual ministrations
    section = soup.find("section", id="hsx")
    _reset_anchor_tag_sources(section)
    _replace_img_sources(section, levels=3)
    # compile HS[ILVY] p-text
    def compile_hsx_paragraph(hsx):
        """
        Gets paragraph text for a given HSX type.
        """
        return (hsx, section
            .find("section", id=hsx)
            .find('p')
            .text,
        )
    hsx_paragraphs = OrderedDict(
        map(
            compile_hsx_paragraph,
            ("hsi", "hsl", "hsv", "hsy"),
        )
    )
    # assemble complementary text and image URLs also
    # get blending mode dot-images and soup
    blendingmode_sections = section.css.select("#hsx-blending-modes > section[id]")
    assert len(BLENDINGMODE_LIST) == len(blendingmode_sections)
    def get_blendingmode_images_and_soup(namesection):
        """
        Gets images and soup from name-section tuple.
        """
        name, subsection = namesection
        dots_images = []
        #logger.debug("Getting images and soup for: %s", name)
        num_images = 0
        for img in filter(
            lambda img_: img_['src'].endswith("_with_dots.png"),
            subsection.find_all('img'),
        ):
            dots_image = img.extract()['src']
            dots_images.append(dots_image)
            num_images += 1
        #logger.debug("(%d) images found.", num_images)
        return (name, (dots_images, subsection))
    images_and_soup = dict(
        map(
            get_blendingmode_images_and_soup,
            zip(BLENDINGMODE_LIST, blendingmode_sections),
        )
    )
    # end: get blending mode dot-images
    subsections = []
    # process the exceptions first
    for hsx, blending_mode in (
        ("hsi", "Intensity"),
        ("hsl", "Lightness"),
        ("hsv", "Value"),
        ("hsy", "Luminosity"),
    ):
        dots_images, subsection = images_and_soup.pop(blending_mode)
        # keys: images, soup
        hsx_paragraph = BeautifulSoup().new_tag(
            "p",
            attrs={"class": "hsx-paragraph"},
            string=hsx_paragraphs[hsx],
        )
        subsection.append(hsx_paragraph)
        subsection.attrs['class'] = []
        subsection['class'].append(blending_mode.lower())
        subsection['class'].append(hsx)
        #logger.debug("Compiling (header, dotsimg_src, section) for (%s, %s).", hsx, blending_mode)
        dotsimg_src = dots_images.pop(0)
        num_figures = 0
        for figure in subsection.find_all("figure"):
            figure.extract()
            num_figures += 1
        #logger.debug("(%d) figures deleted.", num_figures)
        h_tag = blending_mode
        subsections.append((h_tag, dotsimg_src, subsection))
    for blending_mode, (dots_images, subsection_) in images_and_soup.items():
        for (hsx, hsx_paragraph), dotsimg_src in zip(hsx_paragraphs.items(), dots_images):
            hsx_paragraph = BeautifulSoup().new_tag(
                name="p",
                attrs={"class": "hsx-paragraph"},
                string=hsx_paragraph,
            )
            subsection = copy.copy(subsection_)
            subsection.attrs['class'] = []
            subsection['class'].append(
                blending_mode.lower().replace(' ', '-'),
            )
            subsection['class'].append(hsx)
            subsection.append(hsx_paragraph)
            if hsx != "hsy":
                h_tag = "%s - %s" % (blending_mode, hsx.upper())
            else:
                h_tag = {
                    "Color": "Color",
                    "Hue": "Hue",
                    "Increase": "Increase Luminosity",
                    "Increase Saturation": "Increase Saturation",
                    "Saturation": "Saturation",
                    "Decrease": "Decrease Luminosity",
                    "Decrease Saturation": "Decrease Saturation",
                }[blending_mode]
            num_figures = 0
            for figure in subsection.find_all("figure"):
                figure.extract()
                num_figures += 1
            #logger.debug("(%d) figures deleted.", num_figures)
            subsections.append((h_tag, dotsimg_src, subsection))
    return subsections

def _generate_excerpt_without_icon(soup: BeautifulSoup, *, h_level, levels):
    """
    Returns a (header, icon, section) object for a section without a header icon.
    Must provide `h_level` to specify the type of subsection header to extract.
    Must provide `levels` to specify how deep into the filetree the file for the section is.
    """
    section = soup.css.select("section[id]")[0]
    _reset_anchor_tag_sources(section)
    h_tag = _extract_h_tag(section, h_level=h_level)
    _replace_img_sources(section, levels=levels)
    icon = None
    return (h_tag, icon, section)

def write_html_output(root, buffer, targetdir):
    """
    Formats and then writes HTML output.
    """
    # write HTML output
    for directory, source, target, header, _, soup in buffer:
        # generate dict of sort: {source: ref_section/[filename], header: h, icon: icon}
        path_to_source = Path(root, directory, source)
        path_to_target = Path(targetdir, directory, target)
        if path_to_target.is_file():
            pass
        # clean html
        html_to_write = "\n".join([line.strip() for line in str(soup).splitlines() if line.strip()])
        path_to_target.write_text(html_to_write, encoding="utf-8")

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

def _format_target_filename(filename_root, header):
    """
    """
    #filename_root = path_to_source.name
    filename =  filename_root.replace('.html', '') \
        + "_" \
        + header.replace(' - ', '-').replace(' ', '-') \
        + ".html"
    filename = filename.replace(' ', '_').lower()
    filename = re.sub("[^a-z0-9_.-]", "", filename)
    return filename

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
