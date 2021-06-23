import dataclasses
import os
from datetime import datetime
from pathlib import Path
from typing import List

import requests
import sh
from invoke import Context

from tasks.packaging.model import DockerImageRecipe, PackageSpecification
from tasks.util import print_header, run_commands, task


@dataclasses.dataclass
class DockerImage:
    name: str
    architecture: str
    version: str

    base_image: str
    dockerfile: str

    errors: str

    @property
    def tag(self):
        architecture = self.architecture
        if architecture == "arm32v7":
            architecture = "armv7"
        return f"daqzilla/{self.name}-{architecture}:{self.version}"

    def build(self, package_file: Path):

        # Sanity checks.
        if not package_file.exists():
            message = f"Package {package_file} missing."
            if self.errors == "raise":
                raise FileNotFoundError(message)
            else:
                print(f"WARNING: {message}")
                return

        # Build Docker image.
        print_header(f"Building Docker image {self.tag} for {self.architecture}")
        release_date = datetime.utcnow().strftime("%Y-%m-%d")
        os.environ["DOCKER_BUILDKIT"] = "1"
        commands = [
            f"""
            docker build \
                --tag {self.tag} \
                --build-arg BASE_IMAGE={self.base_image} \
                --build-arg PACKAGE_FILE={package_file} \
                --build-arg VERSION={self.version} \
                --build-arg RELEASE_DATE={release_date} \
                --file {self.dockerfile} .
            """,
            # f"docker tag daqzilla/kotori:{spec.version} daqzilla/kotori:nightly",
            # f"docker tag daqzilla/kotori:$(version) daqzilla/kotori:latest"
        ]
        run_commands(commands)
        print()

    def publish(self):
        command = f"docker push {self.tag}"
        run_commands(command)


class DockerImageBuilder:

    recipes: List[DockerImageRecipe] = [
        DockerImageRecipe(
            enabled=True,
            architecture="amd64",
            flavors=["full", "standard"],
            base_distribution="buster",
            base_image="{architecture}/debian:buster-slim",
            platform="linux/amd64",
        ),
        DockerImageRecipe(
            enabled=True,
            architecture="arm64v8",
            flavors=["standard"],
            base_distribution="buster",
            base_image="{architecture}/debian:buster-slim",
            platform="linux/arm64/v8",
        ),
        DockerImageRecipe(
            enabled=True,
            architecture="arm32v7",
            flavors=["standard"],
            base_distribution="buster",
            base_image="{architecture}/debian:buster-slim",
            platform="linux/arm/v7",
        ),
    ]

    manifest_tool_url = "https://github.com/estesp/manifest-tool/releases/download/v1.0.3/manifest-tool-darwin-amd64"
    manifest_tool_path = Path("./var/bin/manifest-tool")

    def __init__(self, errors="ignore"):
        self.errors = errors
        self.manifest_tool = None
        self.download_manifest_tool()

    def download_manifest_tool(self):
        if not self.manifest_tool_path.exists():
            self.manifest_tool_path.parent.mkdir(parents=True, exist_ok=True)
            response = requests.get(self.manifest_tool_url, allow_redirects=True)
            open(self.manifest_tool_path, "wb").write(response.content)
            self.manifest_tool_path.chmod(0o777)
        self.manifest_tool = sh.Command(self.manifest_tool_path)

    @staticmethod
    def check_manifest_tool():
        if "DOCKER_USERNAME" not in os.environ or "DOCKER_PASSWORD" not in os.environ:
            raise ValueError(
                "Unable to build without DOCKER_USERNAME and DOCKER_PASSWORD"
            )

    def run(self, version: str = ""):

        # Sanity checks.
        version = version.strip()
        if not version:
            raise ValueError("Unable to build without version")

        self.check_manifest_tool()

        for recipe in self.recipes:

            if not recipe.enabled:
                continue

            for flavor in recipe.flavors:

                spec = PackageSpecification(
                    distribution=recipe.base_distribution,
                    architecture=recipe.architecture,
                    flavor=flavor,
                    version=version,
                )

                docker_image = DockerImage(
                    name=spec.name,
                    architecture=recipe.architecture,
                    version=version,
                    base_image=recipe.base_image.format(
                        architecture=recipe.architecture
                    ),
                    dockerfile="packaging/dockerfiles/docker-image.dockerfile",
                    errors=self.errors,
                )

                # Compute path to `.deb` file.
                package_name = spec.deb_name()
                package_file = Path("dist") / package_name

                # Build Docker image.
                docker_image.build(package_file=package_file)

                # Publish Docker image.
                docker_image.publish()

        # Publish manifest needed for multi-architecture images.
        self.manifest(basename="kotori", platforms=self.platforms, version=version)
        self.manifest(
            basename="kotori-standard", platforms=self.platforms, version=version
        )

    @property
    def platforms(self):
        platforms = set()
        for recipe in self.recipes:
            platforms.add(recipe.platform)
        return list(platforms)

    def manifest(
        self, basename: str, platforms: List[str], version: str, tag: str = None
    ):
        """
        Create multi-architecture Docker images.

        - https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/
        - https://docs.docker.com/docker-for-mac/multi-arch/
        - https://developer.ibm.com/tutorials/createmulti-architecture-docker-images/
        - https://github.com/estesp/manifest-tool
        """

        self.check_manifest_tool()

        print_header(
            f"Creating Docker manifest for {basename} on platforms {platforms}"
        )

        # Sanity checks.
        if self.manifest_tool is None:
            raise FileNotFoundError(
                f"Docker manifest-tool not found at {self.manifest_tool_path}"
            )

        if tag is None:
            tag = version

        print(
            self.manifest_tool(
                "--username", os.environ["DOCKER_USERNAME"],
                "--password", os.environ["DOCKER_PASSWORD"],
                "push",
                "from-args",
                "--ignore-missing",
                "--platforms", ",".join(platforms),
                "--template", f"daqzilla/{basename}-ARCHVARIANT:{version}",
                "--target", f"daqzilla/{basename}:{tag}",
            )
        )

    def link(self, version: str, tag: str):

        self.check_manifest_tool()

        # Publish manifest for specific tag (e.g. "nightly", "latest").
        self.manifest(
            basename="kotori", platforms=self.platforms, version=version, tag=tag
        )
        self.manifest(
            basename="kotori-standard",
            platforms=self.platforms,
            version=version,
            tag=tag,
        )

    def qa(self, tag: str = None):
        for recipe in self.recipes:

            if not recipe.enabled:
                continue

            for flavor in recipe.flavors:

                # TODO: This is currently only needed to resolve the "name" from the "flavor". Refactor it!
                spec = PackageSpecification(
                    distribution=recipe.base_distribution,
                    architecture=recipe.architecture,
                    flavor=flavor,
                    version="n/a",
                )

                image_name = f"daqzilla/{spec.name}"
                if tag:
                    image_name += f":{tag}"

                print_header(
                    f"Running QA for Docker image {image_name} on {recipe.platform}"
                )

                command = f"docker run -it --rm --platform={recipe.platform} {image_name} kotori --version"
                run_commands(command)

                print()


@task
def images(context: Context, version: str = None):
    """
    Build all designated images for pushing to Docker Hub (stage three).
    """
    DockerImageBuilder().run(version=version)


@task
def link(context: Context, version: str = None, tag: str = None):
    """
    Link image versions to tags (stage three).
    """
    if not version or not tag:
        raise ValueError("Linking a repository needs version and tag")
    DockerImageBuilder().link(version=version, tag=tag)


@task
def qa(context: Context, tag: str = None):
    """
    Run basic quality assurance on Docker images (stage four).
    """
    if not tag:
        tag = None
    DockerImageBuilder().qa(tag=tag)
