import dataclasses
import json
from pathlib import Path

from invoke import Context

from tasks.packaging.model import PackageRecipe, PackageSpecification
from tasks.util import print_header, run_commands, task


class PackageBuilder:
    """
    Build distribution packages reflecting stage two of the whole process.
    """

    recipes = [
        PackageRecipe(
            enabled=True,
            architecture="amd64",
            distributions=[
                "stretch",
                "buster",
                "bionic",
                "focal",
            ],
            flavors=[
                "full",
                "standard",
            ],
        ),
        PackageRecipe(
            enabled=True,
            architecture="arm64v8",
            distributions=[
                "stretch",  # ImportError: cannot import name '_BACKCOMPAT_MAGIC_NUMBER'
                "buster",
            ],
            flavors=["standard"],
        ),
        PackageRecipe(
            enabled=True,
            architecture="arm32v7",
            distributions=[
                "stretch",  # ImportError: cannot import name '_BACKCOMPAT_MAGIC_NUMBER'
                "buster",
            ],
            flavors=["standard"],
        ),
    ]

    def run(self, version=""):
        """
        Invoke the package building for all enabled recipes.
        """

        # Sanity checks. The version must be set and not empty.
        version = version.strip()
        if not version:
            raise ValueError("Unable to build without version")

        for recipe in self.recipes:

            # Skip recipes not enabled.
            if not recipe.enabled:
                continue

            architecture = recipe.architecture
            for distribution in recipe.distributions:
                for flavor in recipe.flavors:
                    spec = PackageSpecification(
                        distribution=distribution,
                        architecture=architecture,
                        flavor=flavor,
                        version=version,
                    )
                    self.deb(spec)

    @staticmethod
    def build_container_name(spec):
        return f"daq-tools/kotori-build-{spec.distribution}-{spec.architecture}:{spec.version}"

    def deb(self, spec: PackageSpecification):

        # Compute package name and path to `.deb` file.
        package_name = spec.deb_name()
        package_file = Path("dist") / package_name

        # Sanity checks.
        if package_file.exists():
            print(f"Package {package_file} already exists, skipping.")
            return

        print_header(
            f"Building package {spec.name} for {spec.distribution} on {spec.architecture}"
        )
        print(json.dumps(dataclasses.asdict(spec), indent=4))

        # Build Linux distribution package within Docker container.
        command = f"""
            docker build \
                --tag {self.build_container_name(spec)} \
                --build-arg BASE_IMAGE=daq-tools/{spec.distribution}-{spec.architecture}-baseline:latest \
                --build-arg NAME={spec.name} \
                --build-arg FEATURES={spec.features} \
                --build-arg VERSION={spec.version} \
                --build-arg DISTRIBUTION={spec.distribution} \
                --build-arg ARCHITECTURE={spec.architecture} \
                --file packaging/dockerfiles/debian-package.dockerfile .
        """
        run_commands(command)

        # Extract package from Docker container.
        tempname = "pkg_extract__"
        commands = [
            f"docker container rm --force {tempname}",
            f"docker container create --name={tempname} {self.build_container_name(spec)}",
            f"docker container cp {tempname}:/dist/{package_name} ./dist/",
            f"docker container rm --force {tempname}",
        ]
        run_commands(commands)
        print()


@task
def deb(
    context: Context,
    distribution: str = None,
    architecture: str = None,
    flavor: str = None,
    version: str = None,
):
    """
    Build an individual Debian package.
    """
    spec = PackageSpecification(
        distribution=distribution,
        architecture=architecture,
        flavor=flavor,
        version=version,
    )
    PackageBuilder().deb(spec)


@task
def run(context, version):
    """
    Build all operating system distribution packages (stage two).
    """
    print()
    print_header(f"Building packages for Kotori version {version}", "=")
    print()
    PackageBuilder().run(version=version)
