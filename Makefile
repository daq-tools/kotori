# -*- coding: utf-8 -*-
# (c) 2014-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>

# ==========================================
#               prerequisites
# ==========================================

# FPM on the build slave has to be patched:
#
# patch against deb.rb of fpm fame::
#
#   def write_meta_files
#      #files = attributes[:meta_files]
#      files = attributes[:deb_meta_file]



# ==========================================
#             build and release
# ==========================================
#
# Release targets for convenient release cutting.
# Uses the fine ``bumpversion`` utility.
#
# Status: Stable
#
# Synopsis::
#
#    make release bump={patch,minor,major}
#    make python-package
#    make debian-package flavor=daq
#

release: virtualenv bumpversion
#release: virtualenv bumpversion push

# build and publish python package (sdist)
python-package: sdist publish-sdist

# build and publish debian package with flavor
# Hint: Should be run on an appropriate build slave matching the deployment platform
debian-package: check-flavor-options sdist deb-build-$(flavor) publish-debian
#debian-package-test: check-flavor-options deb-build-$(flavor)


# ==========================================
#                 releasing
# ==========================================
#
# Release targets for convenient release cutting.
#
# Synopsis::
#
#    make release bump={patch,minor,major}
#
# Setup:
#
#    - Make sure you have e.g. ``bumpversion==0.5.3`` in your ``requirements.txt``
#    - Add a ``.bumpversion.cfg`` to your project root properly reflecting
#      the current version and the list of files to bump versions in. Example::
#
#        [bumpversion]
#        current_version = 0.1.0
#        files = doc/source/conf.py
#        commit = True
#        tag = True
#        tag_name = {new_version}
#

bumpversion: check-bump-options
	bumpversion $(bump)

push:
	git push && git push --tags

sdist:
	python setup.py sdist

publish-sdist:
	# publish Python Eggs to eggserver
	# TODO: use localshop or one of its sisters
	rsync -auv --progress ./dist/kotori-*.tar.gz hiveeyes@packages.elmyra.de:/srv/packages/organizations/hiveeyes/python/eggs/kotori/
	rsync -auv --progress ./dist/kotori-*.tar.gz isareng@packages.elmyra.de:/srv/packages/organizations/isarengineering/python/eggs/kotori/

publish-debian:
	# publish Debian packages
	rsync -auv ./dist/kotori_*.deb hiveeyes@packages.elmyra.de:/srv/packages/organizations/hiveeyes/debian/
	rsync -auv ./dist/kotori_*.deb isareng@packages.elmyra.de:/srv/packages/organizations/isarengineering/debian/

check-bump-options:
	@if test "$(bump)" = ""; then \
		echo "ERROR: 'bump' not set, try 'make release bump={patch,minor,major}'"; \
		exit 1; \
	fi

check-flavor-options:
	@if test "$(flavor)" = ""; then \
		echo "ERROR: 'flavor' not set, try 'make debian-package flavor=daq' or 'make debian-package flavor=daq-binary'"; \
		exit 1; \
	fi


# ==========================================
#                packaging
# ==========================================
#
# Makefile-based poor man's version of:
#
#   - https://hynek.me/articles/python-app-deployment-with-native-packages/
#   - https://parcel.readthedocs.org/
#
# Status: Work in progress
#
# Synopsis::
#
#   make deb-build-daq
#   make deb-build-daq-binary
#
# Build package from designated version::
#
#   make deb-build-daq version=0.6.0
#
# List content of package::
#
#   dpkg-deb --contents dist/kotori_0.6.0-1_amd64.deb
#

fpm-options := \
	--name kotori \
	--iteration 1 \
	--deb-user kotori \
	--deb-group kotori \
	--no-deb-use-file-permissions \
	--no-python-obey-requirements-txt \
	--no-python-dependencies \
	--depends "python" \
	--provides "kotori" \
	--provides "kotori-daq" \
	--deb-suggests "influxdb, mosquitto, mosquitto-clients, grafana" \
	--maintainer "andreas.motl@elmyra.de" \
	--vendor "Elmyra UG" \
	--license "Other/Proprietary" \
	--deb-changelog CHANGES.rst \
	--deb-meta-file README.rst \
	--description "Kotori data acquisition and graphing toolkit" \
	--url "http://isarengineering.de/docs/kotori/"


# get branch and commit identifiers
branch   := $(shell git symbolic-ref HEAD | sed -e 's/refs\/heads\///')
commit   := $(shell git rev-parse --short HEAD)
version  := $(shell python setup.py --version)


deb-build-daq:
	$(MAKE) deb-build name=kotori-daq features=daq

deb-build-daq-binary:
	$(MAKE) deb-build name=kotori-daq-binary features=daq,daq_binary

deb-build: check-build-options

	$(eval buildpath := "./build/$(name)")

	# start super clean, even clear the pip cache
	#rm -rf build dist

	# start clean
	# take care: enable only with caution
	# TODO: sanity check whether buildpath is not empty
	#rm -r $(buildpath) dist

	# prepare
	mkdir -p build dist

	# use "--always copy" to satisfy fpm
	# use "--python=python" to satisfy virtualenv-tools (doesn't grok "python2" when searching for shebangs to replace)
	virtualenv --always-copy --python=python $(buildpath)

	# install package in development mode, enable extra feature "daq"
	#$(buildpath)/bin/python setup.py install

	# use different directory for temp files, because /tmp usually has noexec attributes
	# otherwise: _cffi_backend.so: failed to map segment from shared object: Operation not permitted
	# TMPDIR=/var/tmp

	# build from egg on package server
	# https://pip.pypa.io/en/stable/reference/pip_wheel/#cmdoption--extra-index-url
	#TMPDIR=/var/tmp $(buildpath)/bin/pip install kotori[$(features)]==$(version) --extra-index-url=https://packages.elmyra.de/isarengineering/python/eggs/

	# build sdist egg locally
	TMPDIR=/var/tmp $(buildpath)/bin/python setup.py sdist

	# install from local sdist egg
	# TODO: maybe use "--editable" for installing in development mode
	# https://pip.pypa.io/en/stable/reference/pip_wheel/#cmdoption-f
	TMPDIR=/var/tmp $(buildpath)/bin/pip install kotori[$(features)]==$(version) --download-cache=./build/pip-cache --find-links=./dist

	# Relocate the virtualenv by updating the python interpreter in the shebang of installed scripts.
	# Currently must force reinstall because virtualenv-tools will harm itself (2016-02-21).
	$(buildpath)/bin/pip install virtualenv-tools==1.0 --upgrade --force-reinstall
	$(buildpath)/bin/virtualenv-tools --update-path=/opt/kotori $(buildpath)

	#rm -f $(buildpath)/{.Python,pip-selfcheck.json}

	fpm \
		-s dir -t deb \
		$(fpm-options) \
		--name $(name) \
		--version $(version) \
		--deb-field 'Branch: $(branch) Commit: $(commit)' \
		--package ./dist/ \
		--config-files "/etc/kotori/kotori.ini" \
		--deb-default ./packaging/etc/default \
		--before-install ./packaging/scripts/before-install \
		--after-install ./packaging/scripts/after-install \
		--before-remove ./packaging/scripts/before-remove \
		--verbose \
		--force \
		$(buildpath)/=/opt/kotori \
		./etc/kotori.ini=/etc/kotori/kotori.ini \
		./packaging/systemd/kotori.service=/usr/lib/systemd/system/kotori.service

#		--debug \


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

# -------------------------------------------------------------
#   development options on your fingertips (enable on demand)
# -------------------------------------------------------------

# general debugging
#		--debug \

# don't delete working directory (to introspect the cruft in case something went wrong)
		--debug-workspace \

# we don't prefix, instead use the convenient mapping syntax {source}={target}
#		--prefix /opt/kotori \

# we don't set any architecture, let the package builder do it
#		--architecture noarch \

# there are currently just --deb-init and --deb-upstart options for designating an init- or upstart script
# we already use systemd

# Add FILEPATH as /etc/default configuration
#		--deb-default abc \

# amend the shebang of scripts
#	--python-scripts-executable '/usr/bin/env python' \

# Add custom fields to DEBIAN/control file
#		--deb-field 'Branch: master Commit: deadbeef' \


check-build-options:
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
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


# --------------------------------------
#  Fabric based multi-tenant releasing
# --------------------------------------

#deb-fab:
#	fab deb_build_and_release:gitrepo=$(gitrepo),gitref=$(version),tenant=$(tenant),kind=$(kind),flavor=fpm

#release-deb:
#	$(MAKE) deb gitrepo=ssh://git@git.elmyra.de/isar-engineering/kotori-daq.git gitref=master tenant=elmyra/kotori kind=staging version=$(version)

#egg:
#	fab egg_build_and_release:setup_py=setup.py



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
	nosetests --with-doctest --doctest-tests --doctest-extension=rst

test-coverage: virtualenv
	nosetests \
		--with-doctest --doctest-tests --doctest-extension=rst \
		--with-coverage --cover-package=kotori --cover-tests \
		--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml

docs-html: virtualenv
	touch doc/source/index.rst
	export SPHINXBUILD="`pwd`/.venv27/bin/sphinx-build"; cd doc; make html

virtualenv:
	@test -e .venv27/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages .venv27
	@.venv27/bin/pip --quiet install --requirement requirements-dev.txt


# ==========================================
#         ptrace.isarengineering.de
# ==========================================

# Don't commit media assets (screenshots, etc.) to the repository.
# Instead, upload them to https://ptrace.isarengineering.de/
ptrace_target := root@ptrace.isarengineering.de:/data/web/basti/ptrace.isarengineering.de/htdocs/
ptrace_http   := https://ptrace.isarengineering.de/
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

