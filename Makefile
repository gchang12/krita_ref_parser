VENV_NAME := .venv-krita_ref_parser

# A: Create virtual environment.

$(VENV_NAME)/:
	python3 -m venv $(VENV_NAME)/;
	. $(VENV_NAME)/bin/activate; pip install -r requirements.txt;
	# TODO: Insert report

# B: Generate raw HTML from source.

.INPUT_FILES: \
	input/ \
	input/docs-krita-org/ \
	input/docs-krita-org/_build/html/

## 1: Create folder to store input.
input/:
	mkdir input/;
	# TODO: Insert report

## 2: Fetch raw source from world-wide web.
input/docs-krita-org/: input/
	cd input/; git clone https://invent.kde.org/documentation/docs-krita-org.git;
	# TODO: Insert report

## 3: Extract HTML from source.
input/docs-krita-org/_build/html/: $(VENV_NAME)/ input/docs-krita-org/
	. $(VENV_NAME)/bin/activate; cd input/docs-krita-org/; make html;

# C: Parse raw HTML for text and images to insert into logical sections.

.OUTPUT_FILES: \
	output/ \
	output/raw-excerpts/ \
	output/images/ \
	output/excerpts/ \
	output/index.json \
	.SEARCH_FOR_HIDDEN_OUTPUT

## 1: Create folder to store output.
output/:
	mkdir output/;
	# TODO: Insert report

## 2: Search raw HTML for text-content to store in excerpt files.
output/raw-excerpts/: output/ .INPUT_FILES
	mkdir output/raw-excerpts/;
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_generator/split_docs.py;
	# TODO: Insert report

## 3: Import images, then reference excerpt files to determine which to keep.
output/images/: output/raw-excerpts/
	mkdir output/images/;
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_generator/amputate_images.py;
	echo "There are a total of (`ls output/images/ | wc -l`) output images.";

## 4: Generate index of: (directory, file, header, header-image)
output/index.json: output/raw-excerpts/
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_generator/compile_index.py;
	# TODO: Insert report

## 5: Format and clean generated HTML files.
output/excerpts/: output/raw-excerpts/ output/index.json
	mkdir output/excerpts/;
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_generator/modify_dom.py;
	# TODO: Insert report

## 6: Search for hidden output.
.SEARCH_FOR_HIDDEN_OUTPUT:
	echo "The following files are hidden: `find output/ -name \.\*`";

# *: CLEANUP

.PHONY: clean
clean:
	rm -rf output/ $(VENV_NAME)/ #input/
