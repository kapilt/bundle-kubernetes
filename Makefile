#!/usr/bin/make

build: virtualenv lint test

virtualenv: .venv/bin/python
.venv/bin/python:
	sudo apt-get install python-virtualenv
	virtualenv .venv
	.venv/bin/pip install pytest flake8 mock pyyaml charmhelpers charm-tools ecdsa bundletester

lint: virtualenv
	@.venv/bin/flake8 tests
	@.venv/bin/juju-bundle proof


func_test: virtualenv
	@echo functional tests...
	@.venv/bin/bundletester -v -F -l DEBUG 

clean:
	rm -rf .venv
	find -name *.pyc -delete
