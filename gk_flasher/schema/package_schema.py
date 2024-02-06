# -*- coding: utf-8 -*-
import enum
from typing import Any, List, Optional

from pydantic import BaseModel

SCHEMA_VERSION = 1


class Package(BaseModel):
    schema_version: int = SCHEMA_VERSION
    name: str
    version: str
    description: str
    changelog: str
    components: List["Component"]
    attributes: dict[str, Any]


class Component(BaseModel):
    filename: str
    version: str
    kind: str
    sha256: str
    size: int
    url: str
    attributes: dict[str, Any]


ESP_ATTRIBUTE_KEY = "esp"


class ESPPackageAttributes(BaseModel):
    class ESPChip(str, enum.Enum):
        ESP32 = "ESP32"
        ESP32_S2 = "ESP32-S2"
        ESP32_S3 = "ESP32-S3"
        ESP32_C3 = "ESP32-C3"
        ESP32_C6 = "ESP32-C6"

    target_chip: ESPChip
    target_flash_size: str


class ESPComponentAttributes(BaseModel):
    offset: int


GK_FLASHER_ATTRIBUTE_KEY = "gk_flasher"


class GKFlasherPackageAttributes(BaseModel):
    target_name: Optional[str]
    target_hardware_variant: Optional[str]
    target_photo_url: Optional[str]


class GKFlasherComponentAttributes(BaseModel):
    order: int
    flashable_by_default: bool


MUVOX_API_ATTRIBUTE_KEY = "muvox_api"


class MuvoxAPIPackageAttributes(BaseModel):
    subschema_version: int = 1
    hardware_project_identifier: str = ""
