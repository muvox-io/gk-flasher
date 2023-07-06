# -*- coding: utf-8 -*-
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Simple to use flash utility for microcontrollers"
    )
    parser.add_argument(
        "--package-esp32",
        help="Path to esp-idf's build/ directory to\
             build a GK Flasher package from",
        type=str,
    )
    parser.parse_args()


if __name__ == "__main__":
    main()
