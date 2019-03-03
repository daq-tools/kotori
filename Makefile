# -*- coding: utf-8 -*-
# (c) 2014-2019 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>

# ============
# Main targets
# ============


# -------------
# Configuration
# -------------

$(eval venvpath     := .venv_util)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval pytest       := $(venvpath)/bin/pytest)
$(eval bumpversion  := $(venvpath)/bin/bumpversion)
$(eval twine        := $(venvpath)/bin/twine)
$(eval sphinx       := $(venvpath)/bin/sphinx-build)

# Setup Python virtualenv
setup-virtualenv:
	@test -e $(python) || `command -v virtualenv` --python=python2 --no-site-packages $(venvpath)


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
#    make debian-package flavor=full arch=amd64 version=0.22.0
#
#    # armhf
#    make debian-package flavor=standard arch=armhf version=0.22.0
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
	echo "$(version) $(name) $(features)"

	# Build Python virtualenv and Linux distribution package
	#docker build --tag daq-tools/kotori-build-arm32v7:$(version) --build-arg VERSION=$(version) --build-arg NAME=$(name) --build-arg FEATURES=$(features) --file packaging/dockerfiles/Dockerfile.kotori.arm32v7 .
	#docker build --tag daq-tools/kotori-build-arm32v7:$(version) --build-arg BASE_IMAGE=hiveeyes/arm32v7-baseline --build-arg VERSION=$(version) --build-arg NAME=$(name) --build-arg FEATURES=$(features) --file packaging/dockerfiles/Dockerfile.kotori.arm32v7 .

	docker build --tag daq-tools/kotori-build-$(arch):$(version) --build-arg BASE_IMAGE=daq-tools/$(arch)-baseline:latest --build-arg VERSION=$(version) --build-arg NAME=$(name) --build-arg FEATURES=$(features) --file packaging/dockerfiles/Dockerfile.all.kotori .

	# Extract Debian package
	docker container rm -f finalize; true
	docker container create --name finalize daq-tools/kotori-build-$(arch):$(version)
	docker container cp finalize:/sources/dist/$(name)_$(version)-1_$(arch).deb ./dist/

	docker container rm -f finalize


publish-debian:
	# publish Debian packages
	rsync -auv --progress ./dist/kotori*$(version)*.deb workbench@packages.elmyra.de:/srv/packages/organizations/elmyra/foss/aptly/public/incoming/


build-debian-stretch-amd64-baseline:
	docker build --tag daq-tools/amd64-baseline:0.5.0 --build-arg BASE_IMAGE=balenalib/amd64-debian:stretch-build - < packaging/dockerfiles/Dockerfile.debian-stretch.baseline
	docker tag daq-tools/amd64-baseline:0.5.0 daq-tools/amd64-baseline:latest

build-debian-stretch-armhf-baseline:
	docker build --tag daq-tools/armhf-baseline:0.5.0 --build-arg BASE_IMAGE=balenalib/armv7hf-debian:stretch-build - < packaging/dockerfiles/Dockerfile.debian-stretch.baseline
	docker tag daq-tools/armhf-baseline:0.5.0 daq-tools/armhf-baseline:latest


# -----


testdrive-arm:
	docker build --tag testdrive/kotori-arm32v7:0.21.1 --build-arg KOTORI_DEB=kotori-standard_0.21.1-1_armhf.deb --file packaging/dockerfiles/Dockerfile.testdrive.arm32v7 .
	docker run -it --rm testdrive/kotori-arm32v7:0.21.1 /bin/bash

deb-pure: check-build-options
	fpm \
		-s python -t deb \
		$(fpm-options) \
		--python-scripts-executable '/usr/bin/env python' \
		--version $(version) --iteration 1 \
		--depends python \
		--depends python-pip \
		--architecture noarch \
		--verbose \
		--debug \
		--force \
		.



check-flavor-options:
	@if test "$(flavor)" = ""; then \
		echo "ERROR: 'flavor' not set, try 'make debian-package flavor={minimal,standard,full}'"; \
		exit 1; \
	fi


check-build-options:
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
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

install-releasetools: setup-virtualenv
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
test: virtualenv
	@# https://nose.readthedocs.org/en/latest/plugins/doctests.html
	@# https://nose.readthedocs.org/en/latest/plugins/cover.html
	@#export NOSE_IGNORE_FILES="c\.py";
	nosetests --with-doctest --doctest-tests --doctest-extension=rst --verbose \
		kotori/*.py kotori/daq/{application,graphing,services,storage} kotori/daq/intercom/{mqtt/paho.py,strategies.py,udp.py,wamp.py} kotori/firmware kotori/io kotori/vendor/hiveeyes

test-coverage: virtualenv
	nosetests \
		--with-doctest --doctest-tests --doctest-extension=rst \
		--with-coverage --cover-package=kotori --cover-tests \
		--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml

docs-html: virtualenv
	touch doc/source/index.rst
	export SPHINXBUILD="`pwd`/.venv2/bin/sphinx-build"; cd doc; make html

virtualenv:
	@test -e .venv2/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages .venv2
	@.venv2/bin/pip --quiet install --requirement requirements-dev.txt


# ==========================================
#           ptrace.getkotori.org
# ==========================================

# Don't commit media assets (screenshots, etc.) to the repository.
# Instead, upload them to https://ptrace.getkotori.org/
ptrace_target := root@ptrace.getkotori.org:/srv/www/organizations/daq-tools/ptrace.getkotori.org/htdocs/
ptrace_http   := https://ptrace.getkotori.org/
ptrace: check-ptrace-options
	$(eval prefix := $(shell date --iso-8601))
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
