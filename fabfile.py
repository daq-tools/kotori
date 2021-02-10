import os

from fabric import task

docker_image_version = "0.8.0"
python_version = "3.8"
debian_distributions = ["buster", "stretch"]  # "bullseye"
debian_architectures = ["amd64", "aarch64", "armv7hf"]
ubuntu_builds = [
    {"distribution": "bionic", "image": "ubuntu:bionic-20210118"},
    {"distribution": "focal", "image": "ubuntu:focal-20210119"},
]


@task
def build_docker_debian_baseline_images(context):
    for distribution in debian_distributions:
        for architecture in debian_architectures:
            commands = [
                f"""
                docker build \
                    --tag daq-tools/{distribution}-{architecture}-baseline:{docker_image_version} \
                    --build-arg BASE_IMAGE=balenalib/{architecture}-debian-python:{python_version}-{distribution}-build - \
                    < packaging/dockerfiles/Dockerfile.debian.baseline
                """,
                f"""
                docker tag daq-tools/{distribution}-{architecture}-baseline:{docker_image_version} daq-tools/{distribution}-{architecture}-baseline:latest
                """
            ]
            run_commands(commands)


@task
def build_docker_ubuntu_baseline_images(context):
    architecture = "amd64"
    for build in ubuntu_builds:
        distribution = build["distribution"]
        image = build["image"]
        commands = [
            f"""
            docker build \
                --tag daq-tools/{distribution}-{architecture}-baseline:{docker_image_version} \
                --build-arg BASE_IMAGE={image} - \
                < packaging/dockerfiles/Dockerfile.debian.baseline
            """,
            f"""
            docker tag daq-tools/{distribution}-{architecture}-baseline:{docker_image_version} daq-tools/{distribution}-{architecture}-baseline:latest
            """
        ]
        run_commands(commands)


def run_commands(commands):
    for command in commands:
        command = command.strip()
        print(command)
        os.system(command)
