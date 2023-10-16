# -*- coding: utf-8 -*-
import argparse

from gk_flasher.builders.esp_idf_builder import EspIDFBuilder


def package(args):
    if args.package_esp_idf is not None:
        if args.package_output is None:
            raise Exception(
                "--package-output must be specified if --package-esp-idf is specified"
            )
        builder = EspIDFBuilder(args.package_output, args.package_esp_idf)
        builder.build_package()


def upload(args):
    # Upload logic here. For now, just a placeholder.
    print("Upload functionality not yet implemented.")


def main():
    parser = argparse.ArgumentParser(
        description="Simple to use flash utility for microcontrollers"
    )
    
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    
    # Define the package subcommand
    package_parser = subparsers.add_parser("package", help="Package the esp-idf's build/")
    package_parser.add_argument(
        "--package-esp-idf",
        help="Path to esp-idf's build/ directory to build a GK Flasher package from",
        type=str,
    )
    package_parser.add_argument(
        "--package-output",
        help="Path to output GK Flasher package to",
        type=str,
    )
    package_parser.set_defaults(func=package)
    
    # Define the upload subcommand
    upload_parser = subparsers.add_parser("upload", help="Upload the GK Flasher package")
    # You can add specific arguments for the upload subcommand here
    # For example:
    # upload_parser.add_argument("--target", help="Upload target", type=str)
    upload_parser.set_defaults(func=upload)
    
    args = parser.parse_args()

    if args.subcommand is None:
        import gk_flasher.gui.gk_flasher_gui as gui
        gui.run_gui()

    # Call the function associated with the chosen subcommand
    args.func(args)


if __name__ == "__main__":
    main()
