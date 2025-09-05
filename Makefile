./frontend/kritaref_palette/public/excerpts/:
	python3 src/kritaref_parser/__main__.py && python3 src/kritaref_parser/_build.py && python3 src/kritaref_parser/_rebuild.py
