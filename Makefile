.PHONY: dev install test lint clean
VIRTUALENV ?= .venv


$(VIRTUALENV):
	python3 -m venv .venv

dev: $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip3 install -U pip
	$(VIRTUALENV)/bin/pip3 install -e '.[dev]'

install: $(VIRTUALENV)
	$(VIRTUALENV)/bin/python3 setup.py install

lint: dev
	$(VIRTUALENV)/bin/flake8

test: dev
	$(VIRTUALENV)/bin/pytest

clean: $(VIRTUALENV)
	$(VIRTUALENV)/bin/python3 setup.py clean
	rm -rf .venv
