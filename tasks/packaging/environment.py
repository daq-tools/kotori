from typing import List

from tasks.packaging.model import DockerBaselineImageRecipe
from tasks.util import print_header, run_commands, task


class DockerBaselineImageBuilder:
    """
    Build baseline images reflecting stage one of the whole process.
    """

    recipes: List[DockerBaselineImageRecipe] = [
        # Vanilla Debian.
        DockerBaselineImageRecipe(
            enabled=True,
            vendor="Debian",
            distributions=[
                "bullseye",
                "buster",
                "stretch",
            ],
            architectures=[
                "amd64",
                "arm64v8",
                "arm32v7",
            ],
            image="{architecture}/debian:{distribution}-slim",
        ),
        # Ubuntu.
        DockerBaselineImageRecipe(
            enabled=True,
            vendor="Ubuntu",
            distributions=[
                "focal",
                "bionic",
            ],
            architectures=[
                "amd64",
            ],
            image="{architecture}/ubuntu:{distribution}",
        ),
    ]

    docker_image_version = "0.11.0"

    def run(self):
        """
        Invoke the image building for all enabled recipes.
        """

        for recipe in self.recipes:

            # Skip recipes not enabled.
            if not recipe.enabled:
                continue

            # Build all distributions.
            for distribution in recipe.distributions:

                # Build all architectures per distribution.
                for architecture in recipe.architectures:
                    print_header(
                        f'Building baseline image for {recipe.vendor} "{distribution}" on {architecture}'
                    )
                    image = recipe.image.format(**locals())
                    commands = [
                        f"""
                        docker build \
                            --pull \
                            --tag ephemeral/{distribution}-{architecture}-baseline:{self.docker_image_version} \
                            --tag ephemeral/{distribution}-{architecture}-baseline:latest \
                            --build-arg BASE_IMAGE={image} - \
                            < packaging/dockerfiles/debian-baseline.dockerfile
                        """,
                    ]
                    run_commands(commands)
                    print()


@task
def baseline_images(context):
    """
    Build all Docker baseline images (stage one).
    """
    DockerBaselineImageBuilder().run()
