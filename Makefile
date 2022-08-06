# -*- coding: utf-8 -*-
# (c) 2014-2021 Andreas Motl <andreas.motl@getkotori.org>


# =============
# Configuration
# =============

$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval pytest       := $(venv)/bin/pytest)
$(eval bumpversion  := $(venv)/bin/bumpversion)
$(eval twine        := $(venv)/bin/twine)
$(eval sphinx       := $(venv)/bin/sphinx-build)
$(eval invoke       := $(venv)/bin/invoke)



# =====
# Setup
# =====

# Setup Python virtualenv.
setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venv)
	@$(pip) --quiet install wheel

# Install requirements for building the documentation.
virtualenv-docs: setup-virtualenv
	@$(pip) --quiet install --requirement=requirements-docs.txt

# Install requirements for development.
virtualenv-dev: setup-virtualenv
	@$(pip) install --upgrade --requirement=requirements-test.txt
	@$(pip) install --upgrade --editable=.[daq,daq_geospatial,export,scientific,firmware]

# Install requirements for releasing.
install-releasetools: setup-virtualenv
	@$(pip) install --quiet --requirement=requirements-release.txt --upgrade



# =======
# Release
# =======

# Release this piece of software.
# Uses the fine ``bumpversion`` utility.
#
# Synopsis::
#
#    make release bump={patch,minor,major}
#

release: bumpversion push build pypi-upload

bumpversion: install-releasetools check-bump-options
	$(bumpversion) $(bump)

push:
	git push && git push --tags

build:
	$(python) -m build

pypi-upload: install-releasetools
	twine upload --skip-existing --verbose dist/*.tar.gz

check-bump-options:
	@if test "$(bump)" = ""; then \
		echo "ERROR: 'bump' not set, try 'make release bump={patch,minor,major}'"; \
		exit 1; \
	fi



# =========
# Packaging
# =========

include packaging/tasks.mk



# ==============
# Software tests
# ==============

.PHONY:
test: virtualenv-dev
	$(pytest) kotori test

.PHONY:
test-coverage: virtualenv-dev
	$(pytest) --cov --cov-report=term-missing --cov-report=xml kotori test



# =============
# Documentation
# =============

# Build Sphinx documentation.
docs-html: virtualenv-docs
	touch doc/source/index.rst
	SPHINXBUILD="`pwd`/$(sphinx)" SPHINXOPTS="-j auto" make --directory=doc html

# Upload media assets. Images, videos, etc.
# Don't commit media assets (screenshots, etc.) to the repository.
# Instead, upload them to https://ptrace.getkotori.org/
ptrace_target := root@ptrace.getkotori.org:/srv/www/organizations/daq-tools/ptrace.getkotori.org/htdocs/
ptrace_http   := https://ptrace.getkotori.org/
ptrace: check-ptrace-options
	$(eval prefix := $(shell gdate --iso-8601))
	$(eval name   := $(shell basename $(source)))
	$(eval id     := $(prefix)_$(name))

	@# debugging
	@#echo "name: $(name)"
	@#echo "id:   $(id)"

	@scp '$(source)' '$(ptrace_target)$(id)'

	$(eval url    := $(ptrace_http)$(id))
	@echo "Access URL: $(url)"

check-ptrace-options:
	@if test "$(source)" = ""; then \
		echo "ERROR: 'source' not set"; \
		exit 1; \
	fi


# ==============
# Infrastructure
# ==============

start-foundation-services:
	docker-compose pull
	docker-compose up

mongodb-start:
	mongod --dbpath=./var/lib/mongodb/ --smallfiles
