#!/usr/bin/env bash

# Program to build wheel packages for uploading them to a package repository.

# When seeing troubles with arm32v7, maybe populate `/lib/binfmt.d`.
# https://github.com/docker/for-linux/issues/56#issuecomment-502263368


function invoke_docker() {
  image=$1
  flavor=$2
  docker run -it --rm --volume=$(pwd)/packaging/wheels:/tools --volume=$(pwd)/pkgs:/pkgs --volume=$(pwd):/src ${image} /tools/build.sh ${flavor}
}

function invoke_build() {

  flavor=$1

  if [ $flavor = "full" ]; then
    extras="daq,daq-fineoffset,daq-geospatial,export,plotting,firmware,scientific"
  elif [ $flavor = "standard" ]; then
    extras="daq,daq-fineoffset,daq-geospatial,export"
  else
    echo "ERROR: Package flavor '${flavor}' unknown or not implemented"
    exit 1
  fi

  set -o xtrace

  # Install required Debian packages.
  export DEBIAN_FRONTEND=noninteractive
  apt-get update && apt-get upgrade --yes
  apt-get install --yes \
    python3 python3-dev python3-pip libssl-dev libffi-dev \
    liblzo2-dev libbz2-dev libblosc-dev libhdf5-dev libnetcdf-dev \
    gfortran libatlas-base-dev libopenblas-dev liblapack-dev libcoarrays-dev
  apt-get install --yes libblis-dev libmkl-dev || true

  # Use `wheel` package still compatible with Python 3.5.
  pip3 install --upgrade --force-reinstall "pip<21" wheel

  # Don't use Rust for building `cryptography`.
  export CRYPTOGRAPHY_DONT_BUILD_RUST=1

  # If wheels are already in repository, they don't have to be built again.
  export PIP_EXTRA_INDEX_URL=https://packages.elmyra.de/elmyra/foss/python/

  # Install Kotori, thus building all wheel packages.
  pip3 install /src[${extras}] --prefer-binary --upgrade --verbose

  # Copy compiled wheel packages to /pkgs path.
  find /root/.cache/pip/wheels -iname '*cp*.whl' -exec cp {} /pkgs/ \;
}

# Define Docker image names.
full_images=(
  ephemeral/stretch-amd64-baseline
  ephemeral/buster-amd64-baseline
  ephemeral/bionic-amd64-baseline
  ephemeral/focal-amd64-baseline
)
standard_images=(
  ephemeral/stretch-arm64v8-baseline
  ephemeral/buster-arm64v8-baseline
  ephemeral/stretch-arm32v7-baseline
  ephemeral/buster-arm32v7-baseline
)

function main() {

  # How to determine if a process runs inside Docker?
  # https://stackoverflow.com/a/25518345
  if [ -f /.dockerenv ]; then
    echo "I'm inside matrix ;("
    invoke_build $1

  else
    echo "I'm living in real world!"

    # Build wheels for `full` packages.
    for imagename in ${full_images[@]}; do
      echo "Building wheels on ${imagename}"
      invoke_docker ${imagename} full;
    done

    # Build wheels for `standard` packages.
    for imagename in ${standard_images[@]}; do
      echo "Building wheels on ${imagename}"
      invoke_docker ${imagename} standard;
    done

  fi

}

main $@
