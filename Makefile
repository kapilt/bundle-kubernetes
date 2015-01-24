#!/usr/bin/make

build: virtualenv lint test

virtualenv: .venv/bin/python
.venv/bin/python:
	sudo apt-get install python-virtualenv
	virtualenv .venv
	.venv/bin/pip install pytest flake8 mock pyyaml charmhelpers charm-tools ecdsa bundletester

lint:
	@.venv/bin/flake8 hooks unit_tests
	@.venv/bin/juju-bundle proof


func_test:
	@echo functional tests...
	@juju test

clean:
	rm -rf .venv
	find -name *.pyc -delete
