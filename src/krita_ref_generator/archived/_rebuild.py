
import json
import logging
from pathlib import Path
from bs4 import BeautifulSoup

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

