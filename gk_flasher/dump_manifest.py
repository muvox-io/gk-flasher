from zipfile import ZipFile
from tap import Tap 
import json


class DumpManifestArgs(Tap):
    package: str
    def configure(self):
        self.add_argument("package", help="Path to the package to dump the manifest of")

def dump_manifest(args: DumpManifestArgs):
    input_file = args.package
    zip_file = ZipFile(input_file, "r")

    manifest = json.loads(zip_file.read("manifest.json"))

    print(json.dumps(manifest, indent=4))

