#!/bin/bash

pkgnames=$(ls pkgs/*.whl | perl -pe 's!.+/(.+?)-.*$!$1!' | uniq)

for pkgname in ${pkgnames}
do
  cmd="rsync -auv ./pkgs/${pkgname}* root@pulp.cicer.de:/srv/packages/organizations/elmyra/foss/htdocs/python/${pkgname}/"
  echo $cmd
  $cmd
done
