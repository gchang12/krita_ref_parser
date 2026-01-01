
DONE
====
split_docs.py
amputate_images.py
compile_index.py
modify_dom.py
grep -P "blending_modes/(lighten|darken)/arith" output/excerpts/*/*/*
Revise framework.
segregate build and website
fix build-script
Change layout of KRF
Grouping of different blending modes.
Clean up files:
Replace links where appropriate.
Segregate build and deployment
Regenerate index with the new `pathAsStr` field.
Clear out archived files.
Add some `resize_image_file` function to `amputate_images.py`.
Rotate `Gradients_Comparison` image file 90 degrees clockwise.
Make sure that all index-modifications are in one module.
Add function to inspect for script tags and remove them also.
Add docstrings before I forget what all this does.
Shake the proverbial trees of this program.
Modify:
- CONTRIBUTING.md
- AUTHORS.md
- CHANGELOG.md

ABANDONED
=========
Extract header.
Extract header image.
Parse source and section into different HTML files. (What?)
Make sure to convert those things to Link objects. (bs4 limitations)
Replace 'link-replacement' function with pure equivalent.
