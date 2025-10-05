_:
	make .clean;
	mkdir static;
	python3 src/kritaref_parser/__main__.py;
	python3 src/kritaref_parser/_build.py;
	python3 src/kritaref_parser/_rebuild.py;

.clean:
	rm -fr static/;
	rm -fr frontend/kritaref_palette/public/images;
	rm -fr frontend/kritaref_palette/public/excerpts;
