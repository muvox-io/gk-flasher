# -*- coding: utf-8 -*-
import argparse

from gk_flasher.builders.esp_idf_builder import EspIDFBuilder


def main():
    parser = argparse.ArgumentParser(
        description="Simple to use flash utility for microcontrollers"
    )
    parser.add_argument(
        "--package-esp-idf",
        help="Path to esp-idf's build/ directory to\
             build a GK Flasher package from",
        type=str,
    )
    parser.add_argument(
        "--package-output",
        help="Path to output GK Flasher package to",
        type=str,
    )
    args = parser.parse_args()

    if args.package_esp_idf is not None:
        if args.package_output is None:
            raise Exception(
                "--package-output must be specified if --package-esp-idf is specified"
            )
        builder = EspIDFBuilder(args.package_output, args.package_esp_idf)
        builder.build_package()


if __name__ == "__main__":
    main()
