VENV_NAME := .venv-krita_ref_parser

_ALL: output/excerpts/ output/index.json output/images/
	echo -ne "Success! Created and populated: 'output'/{excerpts,index.json,images}/"

# C: Parse raw HTML for text and images to insert into logical sections.

## 5: Format and clean generated HTML files.
output/excerpts/: output/raw-excerpts/ output/index.json
	mkdir output/excerpts/;
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_parser/regenerate_docs.py || rm -r output/excerpts/;
	echo "'output/excerpts/' has been cloned from 'output/raw-excerpts/' and processed."

## 4: Generate index of: (directory, file, header, header-image)
output/index.json: output/raw-excerpts/
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_parser/compile_index.py || rm output/index.json;
	echo "An index of (header, file, header, hero-image, figures) objects has been created."

## 3: Import images, then reference excerpt files to determine which to keep.
output/images/: output/raw-excerpts/
	mkdir output/images/;
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_parser/amputate_images.py || rm -r output/images/;
	echo "There are a total of (`ls output/images/ | wc -l`) output images.";

## 2: Search raw HTML for text-content to store in excerpt files.
output/raw-excerpts/: input/docs-krita-org/_build/html/ output/
	mkdir output/raw-excerpts/;
	. $(VENV_NAME)/bin/activate; python3 src/krita_ref_parser/split_docs.py || rm -r output/raw-excerpts/;
	echo "'output/raw-excerpts/' has been created and populated from 'input/docs-krita-org/'."

## 1: Create folder to store output.
output/:
	mkdir output/;
	echo "'output/' has been created."

# B: Generate raw HTML from source.

## 3: Extract HTML from source.
input/docs-krita-org/_build/html/: $(VENV_NAME)/ input/docs-krita-org/
	. $(VENV_NAME)/bin/activate; cd input/docs-krita-org/; make html || rm -r _build/html/;
	echo "HTML of Krita documentation has been generated and populated into 'input/docs-krita-org/_build/html/'.";

## 2: Fetch raw source from world-wide web.
input/docs-krita-org/: input/
	cd input/; git clone https://invent.kde.org/documentation/docs-krita-org.git || rm -rf docs-krita-org/;
	echo "'input/docs-krita-org/' has been created and populated from the repository at 'https://invent.kde.org/documentation/docs-krita-org.git'.";

## 1: Create folder to store input.
input/:
	mkdir input/;
	echo "'input/' has been created."

# A: Create virtual environment.

$(VENV_NAME)/:
	python3 -m venv $(VENV_NAME)/ && . $(VENV_NAME)/bin/activate && pip install -r requirements.txt && pip install -e . || rm -r $(VENV_NAME)/;
	echo "$(VENV_NAME)/ has been created.";


# *: CLEANUP

.PHONY: clean
clean:
	rm -rf output/ $(VENV_NAME)/ input/
	echo "'output/', 'input/', and '$(VENV_NAME)' have been removed."
