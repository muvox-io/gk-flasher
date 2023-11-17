
from tap import Tap
from httpx import AsyncClient

class UploadArgs(Tap):
    package: str # Path to GK Flasher package to upload
    api_key: str # API key to use when uploading
    url: str # Root API URL to upload to

async def upload(args: UploadArgs):
    """
        Uploads the GK Flasher package to the specified muvox-api URL using the specified API key.

        :param args: The arguments to use when uploading
    """
    full_url = args.url + "/admin-api/v1/software-releases/ingest"
    # full_url = "https://enm182jmizilj.x.pipedream.net"
    async with AsyncClient() as client:
        with open(args.package, "rb") as package_file:

           
            response = await client.post(
                full_url,
                headers = {
                    "Authorization": "Bearer " + args.api_key,
                },
                files = {
                    "file": package_file
                }
            )
            response.raise_for_status()
            
    
