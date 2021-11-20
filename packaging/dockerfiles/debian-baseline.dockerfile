#
# Build baseline Docker images for building distribution packages.
#
# https://getkotori.org/docs/development/releasing/packaging.html
#
# Synopsis:
#
#   make package-baseline-images
#

ARG BASE_IMAGE

FROM ${BASE_IMAGE} AS debian-fpm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade --yes

# On `arm32v7/debian:buster-slim`, Ruby croaks with certificate errors.
# https://guides.rubygems.org/ssl-certificate-update/
# https://stackoverflow.com/questions/40549268/certificate-verify-failed-while-using-http-rubygems-org-instead-of-https
RUN test -e /etc/debian_version && test $(uname --machine) = "armv7l" && \
    apt-get install --yes wget && \
    wget --output-document=/usr/lib/ssl/cert.pem \
        https://raw.githubusercontent.com/rubygems/rubygems/master/lib/rubygems/ssl_certs/rubygems.org/GlobalSignRootCA_R3.pem \
    ; true

# Install essential dependencies.
RUN apt-get install --yes --no-install-recommends \
    inetutils-ping nano git \
    build-essential pkg-config libffi-dev \
    ruby ruby-dev

# Install fpm (Effing package management).
RUN gem install fpm --version=1.14.1


FROM debian-fpm

# Build foundation and header files
#RUN apt-get install --yes --no-install-recommends apt-utils
RUN apt-get install --yes --no-install-recommends \
    python3 python3-dev python3-venv \
    libssl-dev libyaml-dev libpng-dev libfreetype6-dev

    #python3-setuptools python3-virtualenv virtualenv

# NumPy, pandas, Matplotlib, PyTables, PyNetCDF and more
RUN # apt-get install --yes --install-recommends \
    \
    # baseline \
    python3-requests python3-openssl python3-cryptography python3-certifi \
    \
    # extra: export \
    python3-pandas \
    \
    # extra: plotting \
    python3-matplotlib \
    \
    # extra: scientific \
    python3-tables python3-netcdf4 libatlas3-base

    # python3-scipy

#RUN apt-get install --yes --no-install-recommends \
#    gfortran libatlas-base-dev libopenblas-dev liblapack-dev libcoarrays-dev \
#    libhdf5-dev libnetcdf-dev liblzo2-dev libbz2-dev libblosc-dev
