from invoke import Collection

from . import docker, environment, ospackage

namespace = Collection(environment, ospackage, docker)
