.DEFAULT_GOAL := help
.PHONY: all tests clean

TEST_PATH=./
VENV=./venv/bin/

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo " clean  : Removes stale objects: *.pyc and __pycache__"
	@echo " tests  : run all tests"
	@echo " help   : this section"

all:
	@echo "Not implemented."

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -rf
	rm -rf docs/_build/
	find . -name 'htmlcov' -type d | xargs rm -rf

dev:
	virtualenv -p /usr/bin/python3 venv
	./venv/bin/pip install -r requirements.txt -r requirements-dev.txt


tests:
	$(VENV)coverage run --source=gotime -m pytest

default: help

