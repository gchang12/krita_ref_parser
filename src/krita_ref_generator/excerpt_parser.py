"""
Modifies compiled HTML documents, yields various output.
"""

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
