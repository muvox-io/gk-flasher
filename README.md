# gk-flasher

A GUI and command line utility to flash software on ESP32 devices using convenient packages.

## Usage in project

### Packaging an esp32 project

```sh
poetry run gk-flasher package --package-esp-idf <ESP_IDF_BUILD_DIR> --package-output <PACKAGE_NAME> --muvox-api-hardware-project-identifier <HW PROJECT IDENT> --version <VERSION>
```

### Upload a package to the muvox-api

```sh
poetry run gk-flasher upload --package dupa.gk_pkg --api-key <API_KEY> --url <API_URL>
```
