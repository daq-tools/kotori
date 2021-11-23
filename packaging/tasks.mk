# ***************
# Packaging tasks
# ***************


# =====================
# Distribution packages
# =====================

# Build Docker baseline images for packaging.

package-baseline-images:
	$(invoke) packaging.environment.baseline-images


# Build all operating system distribution packages.
#
# Synopsis::
#
#    # amd64
#    make package-all version=0.26.6

package-all: check-version
	mkdir -p dist
	$(invoke) packaging.ospackage.run --version=$(version)


# Build Debian package.
#
# Synopsis::
#
#    # amd64
#    make package-debian flavor=full dist=buster arch=amd64 version=0.26.6
#
#    # arm64v8
#    make package-debian flavor=standard dist=buster arch=arm64v8 version=0.26.6
#
#    # arm32v7
#    make package-debian flavor=standard dist=buster arch=arm32v7 version=0.26.6

package-debian:
	mkdir -p dist
	$(invoke) packaging.ospackage.deb --version=$(version) --flavor=$(flavor) --distribution=$(dist) --architecture=$(arch)


publish-debian:
	# Publish all Debian packages
	rsync -auv --progress ./dist/kotori*$(version)*.deb workbench@packages.elmyra.de:/srv/packages/organizations/elmyra/foss/aptly/public/incoming/



# =================
# Docker Hub images
# =================

package-docker-images:
	$(invoke) packaging.docker.images --version=$(version)

package-docker-link:
	$(invoke) packaging.docker.link --version=$(version) --tag=$(tag)

package-docker-qa:
	$(invoke) packaging.docker.qa --tag=$(tag)



# =================
# Packaging helpers
# =================

check-version:
	@if test "$(version)" = ""; then \
		echo "ERROR: 'version' not set"; \
		exit 1; \
	fi

check-flavor-options:
	@if test "$(flavor)" = ""; then \
		echo "ERROR: 'flavor' not set, try 'make package-debian flavor={minimal,standard,full}'"; \
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
