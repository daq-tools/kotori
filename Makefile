# ==========================================
#             Debian packages
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
#   make fpm-full version=0.6.0
#   dpkg-deb --contents kotori_0.6.0-1_amd64.deb
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

deb-full: prepare-production-build

	# start super clean, even clear the pip cache
	#rm -rf build dist

	# start clean
	#rm -rf build/virt dist

	# prepare
	mkdir -p build dist

	# use "--always copy" to satisfy fpm
	# use "--python=python" to satisfy virtualenv-tools (doesn't grok "python2" when searching for shebangs to replace)
	virtualenv --always-copy --python=python ./build/virt

	# install package in development mode, enable extra feature "daq"
	#./build/virt/bin/python setup.py install

        # use different directory for temp files, because /tmp usually has noexec attributes
        # otherwise: _cffi_backend.so: failed to map segment from shared object: Operation not permitted
	# TMPDIR=/var/tmp

	# build from egg on package server
	# https://pip.pypa.io/en/stable/reference/pip_wheel/#cmdoption--extra-index-url
	#TMPDIR=/var/tmp ./build/virt/bin/pip install kotori[daq]==$(version) --extra-index-url=https://packages.elmyra.de/isarengineering/python/eggs/

	# build sdist egg locally
	./build/virt/bin/python setup.py sdist

	# install from local sdist egg
	# TODO: maybe use "--editable" for installing development mode
	# https://pip.pypa.io/en/stable/reference/pip_wheel/#cmdoption-f
	TMPDIR=/var/tmp ./build/virt/bin/pip install kotori[daq]==$(version) --download-cache=./build/pip-cache --find-links=./dist

	# update the python interpreter in the shebang of installed scripts
	# in order to relocate the virtualenv
	./build/virt/bin/pip install virtualenv-tools==1.0
	./build/virt/bin/virtualenv-tools --update-path=/opt/kotori ./build/virt

	#rm -f ./build/virt/{.Python,pip-selfcheck.json}

	fpm \
		-s dir -t deb \
		$(fpm-options) \
		--version $(version) \
		--deb-field 'Branch: $(branch) Commit: $(commit)' \
		--package ./dist/ \
		--config-files "/etc/kotori/kotori.ini" \
		--deb-default ./packaging/etc/default \
		--before-install ./packaging/scripts/before-install \
		--after-install ./packaging/scripts/after-install \
		--verbose \
		--force \
		./build/virt/=/opt/kotori \
		./etc/hiveeyes.ini=/etc/kotori/kotori.ini \
		./packaging/systemd/kotori.service=/usr/lib/systemd/system/kotori.service

#		--debug \


deb-pure: prepare-production-build
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



# ------------------
#   upload package
# ------------------

deb-upload:
	scp kotori_0.6.1-1_amd64.deb root@blur.cicer.de:/tmp/


# patch against deb.rb of fpm fame::
#
#   def write_meta_files
#      #files = attributes[:meta_files]
#      files = attributes[:deb_meta_file]


deb:
	fab deb_build_and_release:gitrepo=$(gitrepo),gitref=$(version),tenant=$(tenant),kind=$(kind),flavor=fpm

release-deb:
	$(MAKE) deb gitrepo=ssh://git@git.elmyra.de/isar-engineering/kotori-daq.git gitref=master tenant=elmyra/kotori kind=staging version=$(version)

prepare-production-build:
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
		exit 1; \
	fi

egg:
	fab egg_build_and_release:setup_py=setup.py

# ==========================================
#                 utilities
# ==========================================

# ------------------------------------------
#                   misc
# ------------------------------------------
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
	export SPHINXBUILD="`pwd`/.venv27/bin/sphinx-build"; cd doc; make html

virtualenv:
	@test -e .venv27/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages .venv27
	@.venv27/bin/pip --quiet install --requirement requirements-dev.txt


# ------------------------------------------
#                 releasing
# ------------------------------------------
#
# Release targets for convenient release cutting.
#
# Synopsis::
#
#    make release bump={patch,minor,major}
#

bumpversion:
	bumpversion $(bump)

push:
	git push && git push --tags

sdist:
	python setup.py sdist

upload:

	# Python Eggs
	rsync -auv ./dist/kotori-*.tar.gz hiveeyes@packages.elmyra.de:/srv/packages/organizations/hiveeyes/python/eggs/kotori/
	rsync -auv ./dist/kotori-*.tar.gz isareng@packages.elmyra.de:/srv/packages/organizations/isarengineering/python/eggs/kotori/

	# Debian packages
	rsync -auv ./dist/kotori_*.deb hiveeyes@packages.elmyra.de:/srv/packages/organizations/hiveeyes/debian/
	rsync -auv ./dist/kotori_*.deb isareng@packages.elmyra.de:/srv/packages/organizations/isarengineering/debian/


# sdist-only
#release: virtualenv bumpversion push sdist upload

# sdist plus debian package
release: virtualenv bumpversion push deb-full upload
