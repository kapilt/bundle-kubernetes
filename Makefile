#!/usr/bin/make

build: virtualenv lint test

virtualenv:
	virtualenv .venv
	.venv/bin/pip install pytest flake8 mock pyyaml charmhelpers charm-tools ecdsa bundletester

lint: virtualenv
	@.venv/bin/flake8 tests
	@.venv/bin/juju-bundle proof

test: virtualenv
	@echo Starting tests...


func_test: virtualenv
	@echo functional tests...
	@.venv/bin/bundletester -v -F -l DEBUG

clean:
	rm -rf .venv
	find -name *.pyc -delete
