
egg:
	fab egg_build_and_release:setup_py=setup.py


# make fpm version=0.3.0
# dpkg-deb --contents kotori-daq_0.3.0-1_all.deb

fpm: prepare-production-build
	fpm \
		-s python -t deb \
		--prefix /opt/elmyra/kotori-daq \
		--python-scripts-executable '/usr/bin/env python' \
		--python-obey-requirements-txt \
		--name kotori-daq \
		--force \
		--version $(version) --iteration 1 \
		--depends influxdb \
		--depends grafana \
		--no-python-dependencies \
		--architecture noarch \
		--vendor "Elmyra UG" --maintainer "andreas.motl@elmyra.de" \
		--no-deb-use-file-permissions \
		--verbose \
		--debug \
		--debug-workspace \
		src/kotori.node/setup.py


	#--deb-user kotori \
	#--deb-group kotori \
    #--config-files '/etc/hydro2motion.ini' \
    #--config-files '/etc/hiveeyes.ini' \

deb:
	fab deb_build_and_release:gitrepo=$(gitrepo),gitref=$(version),tenant=$(tenant),kind=$(kind),flavor=fpm

release-deb:
	$(MAKE) deb gitrepo=ssh://git@git.elmyra.de/isar-engineering/kotori-daq.git gitref=master tenant=elmyra/kotori kind=staging version=$(version)

prepare-production-build:
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
		exit 1; \
	fi


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
	rsync -auv ./dist/kotori-*.tar.gz isareng@packages.elmyra.de:/srv/packages/customers/isarengineering/python/eggs/kotori/

release: virtualenv bumpversion push sdist upload
