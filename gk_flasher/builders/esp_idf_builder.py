# -*- coding: utf-8 -*-

import json
import os
import re
from typing import List, Optional

from gk_flasher.builders.base import BaseBuilder
from gk_flasher.schema.package_schema import (
    ESP_ATTRIBUTE_KEY,
    GK_FLASHER_ATTRIBUTE_KEY,
    ESPComponentAttributes,
    ESPPackageAttributes,
    GKFlasherComponentAttributes,
)


class EspIDFBuilder(BaseBuilder):
    build_dir: str

    def __init__(self, build_dir: str, *args, **kwargs):
        super(EspIDFBuilder, self).__init__(*args, **kwargs)
        self.build_dir = build_dir

    def build_package(self):
        flash_args_data: dict = {}
        with open(f"{self.build_dir}/flasher_args.json", "r") as flash_args_file:
            flash_args_data = json.load(flash_args_file)
        chip_mappings = {
            "esp32": ESPPackageAttributes.ESPChip.ESP32,
            "esp32s2": ESPPackageAttributes.ESPChip.ESP32_S2,
            "esp32s3": ESPPackageAttributes.ESPChip.ESP32_S3,
            "esp32c3": ESPPackageAttributes.ESPChip.ESP32_C3,
            "esp32c6": ESPPackageAttributes.ESPChip.ESP32_C6,
        }
        data_chip = flash_args_data["extra_esptool_args"]["chip"]
        if data_chip not in chip_mappings:
            raise Exception(f"Unknown chip {data_chip}")
        target_chip = chip_mappings[data_chip]

        self.schema.attributes[ESP_ATTRIBUTE_KEY] = ESPPackageAttributes(
            target_chip=target_chip,
            target_flash_size=flash_args_data["flash_settings"]["flash_size"],
        )

        files_flashable_by_default: List[str] = []

        for k, v in flash_args_data["flash_files"].items():
            files_flashable_by_default.append(v)

        # find files ending with -flash_args in build_dir
        # tuple of (offset, filename)
        all_files: List[(int, str)] = []
        for file in os.listdir(self.build_dir):
            if file.endswith("-flash_args"):
                contents: Optional[str] = None
                with open(f"{self.build_dir}/{file}", "r") as flash_args_file:
                    contents = flash_args_file.read()
                # split it into segments splitting on space or newline
                segments = re.split(r"[\n\s]", contents)
                i = 0
                curr_offset_str: Optional[str] = None

                while i < len(segments):
                    if segments[i].startswith("-"):
                        # this is a flag
                        i += 2
                        continue
                    if curr_offset_str is None:
                        curr_offset_str = segments[i]
                        i += 1
                        continue
                    else:
                        # strip 0x
                        curr_offset = int(curr_offset_str[2:], 16)
                        all_files.append((curr_offset, segments[i]))
                        curr_offset_str = None
                        i += 1
                        continue
        # sort by offset
        all_files.sort(key=lambda x: x[0])
        # now we have a list of all files and their offsets
        for offset, filename in all_files:
            print(f"Adding file {filename} at offset {offset}")

            self.add_file(
                f"{self.build_dir}/{filename}",
                attributes={
                    ESP_ATTRIBUTE_KEY: ESPComponentAttributes(
                        offset=offset
                    ).model_dump(),
                    GK_FLASHER_ATTRIBUTE_KEY: GKFlasherComponentAttributes(
                        order=all_files.index((offset, filename)),
                        flashable_by_default=filename in files_flashable_by_default,
                    ).model_dump(),
                },
                kind="FIRMWARE_IMAGE",
            )

        self.finalize()
