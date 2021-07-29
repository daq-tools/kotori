#
# Build Debian package using "fpm".
#
# https://getkotori.org/docs/development/releasing/packaging.html
# https://getkotori.org/docs/setup/linux-debian.html
#
# Synopsis:
#
#   make package-debian flavor=full dist=buster arch=amd64 version=0.26.6
#

ARG BASE_IMAGE


# =======================================
# Install package into Python environment
# =======================================
FROM ${BASE_IMAGE} AS python-environment

ARG PYTHON_PACKAGE=kotori
ARG PREFIX=/opt/kotori
ARG VERSION
ARG FEATURES

# Create Python virtualenv
RUN python3 -m venv ${PREFIX}

ARG pip=${PREFIX}/bin/pip

# Fix `pip` re. `PIP_EXTRA_INDEX_URL`.
# https://bugs.launchpad.net/ubuntu/+source/python-pip/+bug/1822842
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=837764
RUN ${pip} install --upgrade --force-reinstall "pip<21" wheel

# Announce extra PyPI repository containing pre-built packages for `aarch64` (arm64v8) and `armv7l` (arm32v7).
ENV PIP_EXTRA_INDEX_URL=https://packages.elmyra.de/elmyra/foss/python/

# Use a temporary directory allowing to execute programs.
ENV TMPDIR=/var/tmp

# Workaround for Python 3.5.
RUN \
    python3 -c 'import sys; assert (3, 5) <= sys.version_info < (3, 6)' \
    && ${pip} install 'incremental>=16.10.1' 'cffi!=1.11.3,>=1.8' \
    || true

# Install package from PyPI.
RUN ${pip} install ${PYTHON_PACKAGE}[${FEATURES}]==${VERSION} --prefer-binary --upgrade


# ===========================
# Create distribution package
# ===========================
FROM python-environment AS package

ARG NAME
ARG VERSION
ARG DISTRIBUTION
ARG ARCHITECTURE

ARG PREFIX=/opt/kotori


# Counter "ValueError: bad marshal data (unknown type code)".
RUN find ${PREFIX} -name '*.pyc' -delete
RUN find ${PREFIX} -name '__pycache__' -delete

# Copy over specific resources required for package building.
WORKDIR /
COPY README.rst README.rst
COPY CHANGES.rst CHANGES.rst
COPY etc etc
COPY packaging packaging

# Build package.
ENV TMPDIR=/var/tmp
RUN ./packaging/builder/fpm-package "${NAME}" "${VERSION}" "${DISTRIBUTION}" "${ARCHITECTURE}"
