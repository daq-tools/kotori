#
# Build Docker image for publishing on Docker Hub.
#
# https://getkotori.org/docs/development/releasing/packaging.html
# https://getkotori.org/docs/setup/docker.html
#
# Synopsis:
#
#   make package-dockerhub-image version=0.24.5
#

ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ARG VERSION
ARG RELEASE_DATE

ARG PACKAGE_FILE

LABEL version="${VERSION}"
LABEL release-date="${RELEASE_DATE}"
LABEL description="Kotori is a data acquisition, processing and graphing toolkit for humans"
LABEL maintainer="Andreas Motl <andreas.motl@elmyra.de>"

#ARG package_name=kotori_${VERSION}-1~buster_amd64.deb

#RUN timedatectl set-ntp true

# Tweak: Use `kotori*.deb` from local filesystem.
COPY ./${PACKAGE_FILE} /tmp

# Ramping up.
RUN \
    apt-get update && \
#    apt-get install --yes wget && \
\
# Add repository key.
# Don't use "apt-key add" for adding key.
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=851774
#    wget -q https://packages.elmyra.de/elmyra/foss/debian/pubkey.txt -O /etc/apt/trusted.gpg.d/daqzilla.asc && \
\
# Add package repository.
# Don't use "apt-add-repository".
#    echo 'deb https://packages.elmyra.de/elmyra/foss/debian/ buster main foundation' > /etc/apt/sources.list.d/daqzilla-buster.list && \
\
# Install infrastructure services.
#    apt-get update && apt-get install --yes --install-recommends systemd- influxdb- grafana- mongodb- mosquitto- mosquitto-clients- && \
\
# Install Kotori.
#apt-get update && apt-get install --yes --install-recommends kotori=${VERSION}* && \
\
# Tweak: Use `kotori*.deb` from local filesystem.
apt-get install --yes --install-recommends /tmp/$(basename ${PACKAGE_FILE}) && \
ln -s /opt/kotori/bin/kotori /usr/local/sbin/ && \
\
# Tearing down.
    apt-get remove --purge --yes wget && \
    apt-get remove --purge --yes build-essential gcc gcc-8 g++-8 libgcc-8-dev libstdc++-8-dev libc-dev-bin linux-libc-dev python-dev libpython-dev libexpat1-dev manpages-dev && \
    apt-get autoremove --yes && apt-get autoclean --yes && \
    rm -rf /var/lib/apt/lists/* \
    rm /tmp/*

EXPOSE 24642

CMD [ "kotori" ]
