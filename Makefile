
egg:
	fab egg_build_and_release:setup_py=src/kotori.node/setup.py


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

release:
	$(MAKE) deb gitrepo=ssh://git@git.elmyra.de/isar-engineering/kotori-daq.git gitref=master tenant=elmyra/kotori kind=staging version=$(version)

upload:
	rsync -auv kotori-daq*.deb root@elbanco.hiveeyes.org:/tmp/

prepare-production-build:
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
		exit 1; \
	fi
