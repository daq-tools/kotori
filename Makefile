# -*- coding: utf-8 -*-
# (c) 2014-2023 Andreas Motl <andreas.motl@getkotori.org>


# =============
# Configuration
# =============

$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval pytest       := $(venv)/bin/pytest)
$(eval coverage     := $(venv)/bin/coverage)
$(eval twine        := $(venv)/bin/twine)
$(eval sphinx-build := $(venv)/bin/sphinx-build)
$(eval sphinx-autobuild := $(venv)/bin/sphinx-autobuild)
$(eval invoke       := $(venv)/bin/invoke)



# =====
# Setup
# =====

# Setup Python virtualenv.
setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venv)
	@$(pip) install --upgrade --prefer-binary wheel

# Install requirements for building the documentation.
virtualenv-docs: setup-virtualenv
	@$(pip) install --upgrade --prefer-binary --requirement=doc/source/requirements.txt

# Install requirements for development.
virtualenv-dev: setup-virtualenv
	@$(pip) install --upgrade --prefer-binary --requirement=requirements-test.txt
	@$(pip) install --upgrade --prefer-binary --requirement=requirements-full.txt

# Install requirements for releasing.
install-releasetools: setup-virtualenv
	@$(pip) install --upgrade --prefer-binary --requirement=requirements-release.txt



# =======
# Release
# =======

# Synopsis::
#
#    make release
#

release: push build pypi-upload

push:
	git push && git push --tags

build:
	$(python) -m build

pypi-upload: install-releasetools
	twine upload --skip-existing --verbose dist/*.tar.gz dist/*.whl

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
	$(coverage) run --concurrency=multiprocessing,thread --parallel-mode --timid $(pytest) kotori test
	$(coverage) combine
	$(coverage) report
	$(coverage) xml


# =============
# Documentation
# =============

# Build Sphinx documentation.
docs-html: virtualenv-docs
	touch doc/source/index.rst
	$(sphinx-build) -j auto -n -W --keep-going -b html doc/source doc/build

docs-autobuild: virtualenv-docs
	$(pip) install sphinx-autobuild
	$(sphinx-autobuild) --open-browser doc/source doc/build

# Run link checker on documentation.
docs-linkcheck: virtualenv-docs
	$(sphinx-build) -j auto -n -W --keep-going -b linkcheck doc/source doc/build


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
