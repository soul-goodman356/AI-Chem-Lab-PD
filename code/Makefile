PY ?= python

.PHONY: all tables figures clean
all: tables figures

tables:
	$(PY) make_tables.py

figures:
	$(PY) make_figures.py

clean:
	- rm -f results/*.csv results/*.png
