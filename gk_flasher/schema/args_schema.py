# -*- coding: utf-8 -*-
from typing import Optional

from tap import Tap


class PackageArgs(Tap):
    package_esp_idf: str  # Path to esp-idf's build/ directory to build a GK Flasher package from
    package_output: str  # Path to output GK Flasher package to
    muvox_api_hardware_project_identifier: Optional[
        str
    ]  # Identifier for the hardware project on muvox-api
    version: Optional[str]  # Version of the package
    release_channels: Optional[str]  # Comma-separated list of release channels to publish to
