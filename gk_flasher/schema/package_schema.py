from typing import Any, List
from pydantic import BaseModel
import enum
class Package(BaseModel):
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

