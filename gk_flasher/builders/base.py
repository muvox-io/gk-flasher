# -*- coding: utf-8 -*-
import hashlib
import json
import os
from typing import Any, Optional
from zipfile import ZipFile

from gk_flasher.schema.args_schema import PackageArgs
from gk_flasher.schema.package_schema import Component, Package


class BaseBuilder:
    schema: Package
    zipFile: ZipFile
    output: str

    def __init__(
        self,
        args: PackageArgs,
    ):
        self.output = args.package_output
        self.zipFile = ZipFile(self.output, "w")
        self.schema = Package(
            name="NO_NAME",
            version=args.version,
            description="NO_DESCRIPTION",
            changelog="NO_CHANGELOG",
            attributes={},
            components=[],
        )

    def add_file(
        self,
        path: str,
        filename: Optional[str] = None,
        version: Optional[str] = None,
        kind: Optional[str] = None,
        attributes: Optional[dict[str, Any]] = None,
    ):
        # get size and sha256
        size = os.path.getsize(path)
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha256.update(data)
        if filename is None:
            filename = os.path.basename(path)
        if version is None:
            version = "NO_VERSION"
        if kind is None:
            kind = "FILE"
        self.zipFile.write(path, filename)
        self.schema.components.append(
            Component(
                filename=filename,
                version=version,
                kind=kind,
                sha256=sha256.hexdigest(),
                size=size,
                url="file://" + filename,
                attributes=attributes,
            )
        )

    def finalize(self):
        json_data = json.dumps(self.schema.dict(), indent=4)
        self.zipFile.writestr("manifest.json", json_data)
        self.zipFile.close()
