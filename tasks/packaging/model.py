import dataclasses
from typing import ClassVar, List


@dataclasses.dataclass
class DockerBaselineImageRecipe:
    """
    Data structure for holding information about a recipe for building baseline
    Docker images. Those images will be used for building the actual operating
    system distribution packages.
    """

    # Whether this recipe is enabled.
    enabled: bool

    # The operating system vendor, e.g. Debian, Ubuntu.
    vendor: str

    # List of operating system distributions, e.g. stretch, buster.
    distributions: List[str]

    # List of architectures, e.g. amd64, arm64v8, arm32v7.
    architectures: List[str]

    # Docker image to use.
    image: str


@dataclasses.dataclass
class PackageSpecification:
    """
    Data structure for holding information about individual distribution
    packages.
    """

    # Package flavor, e.g. minimal, standard, full.
    flavor: str

    # Package version.
    version: str

    # Distribution name, e.g. stretch, buster.
    distribution: str

    # Architecture, e.g. amd64, arm64v8, arm32v7.
    architecture: str

    # Computed package name, taking `flavor` into account.
    name: str = None

    # List of Python `extra` labels, taking `flavor` into account.
    features: str = None

    # Map architecture labels to Debian distribution package architecture name.
    debian_architecture_map: ClassVar = {
        "arm64v8": "arm64",
        "arm32v7": "armhf",
    }

    def __post_init__(self):
        self.resolve()
        self.validate()

    def validate(self):
        """
        Sanity checks. All designated specification fields must be set and not
        be empty.
        """
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if value is None:
                raise ValueError(
                    f'Package specification field "{field.name}" is required.'
                )

    def resolve(self):
        """
        Resolve the designated package flavor to a list of Python package
        `extra` labels.
        """
        if self.flavor == "minimal":
            self.name = "kotori-minimal"
            self.features = "daq"
        elif self.flavor == "standard":
            self.name = "kotori-standard"
            self.features = "daq,daq_geospatial,export"
        elif self.flavor == "full":
            self.name = "kotori"
            self.features = "daq,daq_geospatial,export,plotting,firmware,scientific"
        else:
            raise ValueError("Unknown package flavor")

    @property
    def debian_architecture(self):
        """
        Resolve the architecture label to a Debian package architecture suffix.
        """
        return self.debian_architecture_map.get(self.architecture, self.architecture)

    def deb_name(self):
        """
        Compute the full name of the Debian `.deb` package.
        """
        return f"{self.name}_{self.version}-1~{self.distribution}_{self.debian_architecture}.deb"


@dataclasses.dataclass
class PackageRecipe:
    """
    Data structure for holding information about a recipe for building
    distribution packages.
    """

    # Whether this recipe is enabled.
    enabled: bool

    # Architecture, e.g. amd64, arm64v8, arm32v7.
    architecture: str

    # List of operating system distributions, e.g. stretch, buster.
    distributions: List[str]

    # List of package flavors, e.g. minimal, standard, full.
    flavors: List[str]


@dataclasses.dataclass
class DockerImageRecipe:
    enabled: bool
    architecture: str
    flavors: List[str]
    base_distribution: str
    base_image: str
    platform: str
