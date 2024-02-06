# -*- coding: utf-8 -*-


import asyncio
from typing import Optional

from tap import Tap

from gk_flasher.builders.esp_idf_builder import EspIDFBuilder
from gk_flasher.schema.package_schema import (
    MUVOX_API_ATTRIBUTE_KEY,
    MuvoxAPIPackageAttributes,
)
from gk_flasher.uploader.uploader import UploadArgs, upload


class PackageArgs(Tap):
    package_esp_idf: str  # Path to esp-idf's build/ directory to build a GK Flasher package from
    package_output: str  # Path to output GK Flasher package to
    muvox_api_hardware_project_identifier: Optional[
        str
    ]  # Identifier for the hardware project on muvox-api


def package(args: PackageArgs):
    if args.package_esp_idf is not None:
        if args.package_output is None:
            raise Exception(
                "--package-output must be specified if --package-esp-idf is specified"
            )
        builder = EspIDFBuilder(args.package_esp_idf, args.package_output)
        if args.muvox_api_hardware_project_identifier is not None:
            builder.schema.attributes[
                MUVOX_API_ATTRIBUTE_KEY
            ] = MuvoxAPIPackageAttributes(
                hardware_project_identifier=args.muvox_api_hardware_project_identifier
            )
        builder.build_package()


class Args(Tap):
    """Simple to use flash utility for microcontrollers."""

    def configure(self):
        self.add_subparsers(help="sub-command help", dest="subcommand")
        self.add_subparser("package", PackageArgs, help="Build gk_pkg")
        self.add_subparser("upload", UploadArgs, help="Upload gk_pkg to muvox-api")


async def async_main():
    args = Args(underscores_to_dashes=True).parse_args()

    if args.subcommand is None:
        import gk_flasher.gui.gk_flasher_gui as gui

        gui.run_gui()
    elif args.subcommand == "package":
        package(args)
    elif args.subcommand == "upload":
        await upload(args)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
