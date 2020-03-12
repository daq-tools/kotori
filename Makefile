# -*- coding: utf-8 -*-
# (c) 2014-2020 Andreas Motl <andreas.motl@getkotori.org>

# ============
# Main targets
# ============


# -------------
# Configuration
# -------------

$(eval venvpath     := .venv2)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval pytest       := $(venvpath)/bin/pytest)
$(eval bumpversion  := $(venvpath)/bin/bumpversion)
$(eval twine        := $(venvpath)/bin/twine)

$(eval venv3        := .venv3)
$(eval pip3         := $(venv3)/bin/pip)
$(eval python3      := $(venv3)/bin/python)
$(eval sphinx       := $(venv3)/bin/sphinx-build)


# Setup Python virtualenv
setup-virtualenv2:
	@test -e $(python) || `command -v virtualenv` --python=python2 --no-site-packages $(venvpath)

setup-virtualenv3:
	@test -e $(python3) || `command -v virtualenv` --python=python3 --no-site-packages $(venv3)

virtualenv-docs: setup-virtualenv3
	@$(pip3) --quiet install --requirement requirements-docs.txt

virtualenv-dev: setup-virtualenv2
	@$(pip) install --upgrade --requirement requirements-dev.txt
	@$(pip) install --upgrade --requirement requirements-test.txt
	@$(pip) install --upgrade -e.[daq,daq_geospatial,export,firmware]


# =======
# Release
# =======
#
# Release this piece of software
# Uses the fine ``bumpversion`` utility.
#
# Synopsis::
#
#    make release bump={patch,minor,major}
#

release: bumpversion push sdist pypi-upload


publish-sdist: sdist
	# publish Python Eggs to eggserver
	# TODO: use localshop or one of its sisters
	rsync -auv --progress ./dist/kotori-*.tar.gz workbench@packages.elmyra.de:/srv/packages/organizations/elmyra/foss/htdocs/python/kotori/




# ==========================================
#                packaging
# ==========================================


# Build and publish debian package with flavor
# Hint: Should be run on an appropriate build slave matching the deployment platform

# Synopsis::
#
#    # amd64
#    make debian-package flavor=full dist=buster arch=amd64 version=0.22.0
#
#    # armhf
#    make debian-package flavor=standard dist=buster arch=armhf version=0.22.0
#

debian-package: check-flavor-options deb-build-$(flavor) publish-debian


deb-build-minimal:
	$(MAKE) deb-build name=kotori-minimal features=daq

deb-build-standard:
	$(MAKE) deb-build name=kotori-standard features=daq,export

deb-build-standard-binary:
	$(MAKE) deb-build name=kotori-standard-binary features=daq,export,daq_binary

deb-build-full:
	$(MAKE) deb-build name=kotori features=daq,daq_geospatial,export,plotting,firmware,scientific


deb-build: check-build-options

	@# https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
	@# https://en.wikipedia.org/wiki/ANSI_escape_code
	$(eval RED := "\033[0;31m")
	$(eval YELLOW := \033[0;33m\033[1m)
	$(eval NC := \033[0m)

	@echo "Building package $(YELLOW)$(name)$(NC) version $(YELLOW)$(version)$(NC) with features $(YELLOW)$(features)$(NC)"

	# Build Python virtualenv and Linux distribution package
	@#docker build --tag daq-tools/kotori-build-arm32v7:$(version) --build-arg VERSION=$(version) --build-arg NAME=$(name) --build-arg FEATURES=$(features) --file packaging/dockerfiles/Dockerfile.kotori.arm32v7 .
	@#docker build --tag daq-tools/kotori-build-arm32v7:$(version) --build-arg BASE_IMAGE=hiveeyes/arm32v7-baseline --build-arg VERSION=$(version) --build-arg NAME=$(name) --build-arg FEATURES=$(features) --file packaging/dockerfiles/Dockerfile.kotori.arm32v7 .

	docker build --tag daq-tools/kotori-build-$(arch):$(version) --build-arg BASE_IMAGE=daq-tools/$(dist)-$(arch)-baseline:latest --build-arg DISTRIBUTION=$(dist) --build-arg VERSION=$(version) --build-arg NAME=$(name) --build-arg FEATURES=$(features) --file packaging/dockerfiles/Dockerfile.all.kotori .

	# Extract Debian package
	docker container rm -f finalize; true
	docker container create --name finalize daq-tools/kotori-build-$(arch):$(version)
	docker container cp finalize:/dist/$(name)_$(version)-1~$(dist)_$(arch).deb ./dist/

	docker container rm -f finalize


publish-debian:
	# Publish all Debian packages
	rsync -auv --progress ./dist/kotori*$(version)*.deb workbench@packages.elmyra.de:/srv/packages/organizations/elmyra/foss/aptly/public/incoming/


build-debian-stretch-amd64-baseline:
	docker build --tag daq-tools/stretch-amd64-baseline:0.7.0 --build-arg BASE_IMAGE=balenalib/amd64-debian:stretch-build - < packaging/dockerfiles/Dockerfile.debian.baseline
	docker tag daq-tools/stretch-amd64-baseline:0.7.0 daq-tools/stretch-amd64-baseline:latest

build-debian-stretch-armhf-baseline:
	docker build --tag daq-tools/stretch-armhf-baseline:0.7.0 --build-arg BASE_IMAGE=balenalib/armv7hf-debian:stretch-build - < packaging/dockerfiles/Dockerfile.debian.baseline
	docker tag daq-tools/stretch-armhf-baseline:0.7.0 daq-tools/stretch-armhf-baseline:latest


build-debian-buster-amd64-baseline:
	docker build --tag daq-tools/buster-amd64-baseline:0.7.0 --build-arg BASE_IMAGE=balenalib/amd64-debian:buster-build - < packaging/dockerfiles/Dockerfile.debian.baseline
	docker tag daq-tools/buster-amd64-baseline:0.7.0 daq-tools/buster-amd64-baseline:latest

build-debian-buster-armhf-baseline:
	docker build --tag daq-tools/buster-armhf-baseline:0.7.0 --build-arg BASE_IMAGE=balenalib/armv7hf-debian:buster-build - < packaging/dockerfiles/Dockerfile.debian.baseline
	docker tag daq-tools/buster-armhf-baseline:0.7.0 daq-tools/buster-armhf-baseline:latest


build-ubuntu-bionic-amd64-baseline:
	docker build --tag daq-tools/bionic-amd64-baseline:0.7.0 --build-arg BASE_IMAGE=ubuntu:bionic-20200219 - < packaging/dockerfiles/Dockerfile.debian.baseline
	docker tag daq-tools/bionic-amd64-baseline:0.7.0 daq-tools/bionic-amd64-baseline:latest


check-flavor-options:
	@if test "$(flavor)" = ""; then \
		echo "ERROR: 'flavor' not set, try 'make debian-package flavor={minimal,standard,full}'"; \
		exit 1; \
	fi


check-build-options:
	@if test "$(dist)" = ""; then \
		echo "ERROR: 'dist' not set"; \
		exit 1; \
	fi
	@if test "$(arch)" = ""; then \
		echo "ERROR: 'arch' not set"; \
		exit 1; \
	fi
	@if test "$(name)" = ""; then \
		echo "ERROR: 'name' not set"; \
		exit 1; \
	fi
	@if test "$(features)" = ""; then \
		echo "ERROR: 'features' not set"; \
		exit 1; \
	fi
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
		exit 1; \
	fi


# =============
# Docker images
# =============

check-dockerbuild:
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
		exit 1; \
	fi

build-dockerhub-image: check-dockerbuild
	docker build --tag daqzilla/kotori:$(version) --build-arg version=$(version) - < packaging/dockerfiles/Dockerfile.hub.kotori
	docker tag daqzilla/kotori:$(version) daqzilla/kotori:latest



# ===============
# Utility targets
# ===============
bumpversion: install-releasetools check-bump-options
	$(bumpversion) $(bump)

push:
	git push && git push --tags

sdist:
	$(python) setup.py sdist

pypi-upload: install-releasetools
	twine upload --skip-existing --verbose dist/*.tar.gz

install-releasetools: setup-virtualenv2
	@$(pip) install --quiet --requirement requirements-release.txt --upgrade


check-bump-options:
	@if test "$(bump)" = ""; then \
		echo "ERROR: 'bump' not set, try 'make release bump={patch,minor,major}'"; \
		exit 1; \
	fi



# ==========================================
#                 environment
# ==========================================
#
# Miscellaneous tools:
# Software tests, Documentation builder, Virtual environment builder
#

.PHONY: test
pytest:

	# Run pytest.
	$(venvpath)/bin/pytest kotori test --verbose --log-level DEBUG --log-cli-level DEBUG --log-format='%(asctime)-15s [%(name)-35s] %(levelname)-8s: %(message)s' --log-date-format='%Y-%m-%dT%H:%M:%S%z'

nosetest:

	# Run nosetest.
	@# https://nose.readthedocs.org/en/latest/plugins/doctests.html
	@# https://nose.readthedocs.org/en/latest/plugins/cover.html
	export NOSE_IGNORE_FILES="test_.*\.py"; \
	$(venvpath)/bin/nosetests --with-doctest --doctest-tests --doctest-extension=rst --verbose \
		kotori/*.py kotori/daq/{application,graphing,services,storage} kotori/daq/intercom/{mqtt/paho.py,strategies.py,udp.py,wamp.py} kotori/firmware kotori/io kotori/vendor/hiveeyes

test: pytest nosetest

test-coverage:
	$(venvpath)/bin/nosetests \
		--with-doctest --doctest-tests --doctest-extension=rst \
		--with-coverage --cover-package=kotori --cover-tests \
		--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml

docs-html: virtualenv-docs
	touch doc/source/index.rst
	export SPHINXBUILD="`pwd`/$(sphinx)"; cd doc; make html


# ==========================================
#           ptrace.getkotori.org
# ==========================================

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



# ==========================================
#               infrastructure
# ==========================================
mongodb-start:
	mongod --dbpath=./var/lib/mongodb/ --smallfiles
