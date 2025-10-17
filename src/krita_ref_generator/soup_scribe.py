"""
"""

from bs4 import BeautifulSoup

def format_target_filename(filename: str, h2_text: str):
    """
    """
    new_filename = filename.replace('.html', '') \
        + "_" \
        + h2_text.replace(' - ', '-').replace(' ', '-') \
        + ".html"
    new_filename = new_filename.replace(' ', '_').lower()
    new_filename = re.sub("[^a-z0-9_.-]", "", new_filename)
    return new_filename

def write_stripped_soup(soup: BeautifulSoup, filename: str):
    """
    """
    soup_as_str = "\n".join([line.strip() for line in str(soup).splitlines() if line.strip()])
    write_result = Path(filename).write_text(soup_as_str, encoding="utf-8")
    return write_result

