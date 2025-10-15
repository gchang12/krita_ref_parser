VENV_NAME := .venv-krita_ref_generator

# A: Generate raw HTML from source.

.INPUT_FILES: \
	$(VENV_NAME)/ \
	input/ \
	input/docs-krita-org/ \
	input/docs-krita-org/_build/html/

## 1: Create virtual environment.
$(VENV_NAME)/:
	python3 -m venv $(VENV_NAME)/;
	. $(VENV_NAME)/bin/activate; pip install -r requirements.txt;

## 2: Create folder to store input.
input/:
	mkdir input/;

## 3: Fetch raw source from world-wide web.
input/docs-krita-org/: input/
	cd input/; git init; git clone https://invent.kde.org/documentation/docs-krita-org.git;

## 3: Extract HTML from source.
input/docs-krita-org/_build/html/: $(VENV_NAME)/ input/docs-krita-org/
	. $(VENV_NAME)/bin/activate; cd input/docs-krita-org/; make html;

# B: Parse raw HTML for text and images to insert into logical sections.

.OUTPUT_FILES: \
	output/ \
	output/excerpts/ \
	output/images/

## 1: Create folder to store output.
output/:
	mkdir output/;

## 2: Search raw HTML for text-content to store in excerpt files.
output/excerpts/: output/
	mkdir output/excerpts/;
	python3 src/krita_ref_generator/excerpt_generator.py;
	#python3 src/krita_ref_generator/__main__.py;
	#python3 src/krita_ref_generator/_build.py;
	#python3 src/krita_ref_generator/_rebuild.py;

## 3: Import images, then reference excerpt files to determine which to keep.
output/images/: output/excerpts/
	mkdir output/images/;
	python3 src/krita_ref_generator/image_generator.py;
	echo "There are a total of (`ls output/images/ | wc -l`) output images.";

# C: Search for hidden files.
.SEARCH_FOR_HIDDEN_OUTPUT:
	echo "The following files are hidden: `find output/ -name \.\*`";

# *: CLEANUP

.PHONY: clean
clean:
	rm -rf output/ input/ $(VENV_NAME)/
