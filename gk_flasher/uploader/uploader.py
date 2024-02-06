# -*- coding: utf-8 -*-
from httpx import AsyncClient, HTTPStatusError, RequestError
from tap import Tap


class UploadArgs(Tap):
    package: str  # Path to GK Flasher package to upload
    api_key: str  # API key to use when uploading
    url: str  # Root API URL to upload to


async def upload(args: UploadArgs):
    """Uploads the GK Flasher package to the specified muvox-api URL using the specified
    API key.

    :param args: The arguments to use when uploading
    """
    full_url = args.url + "/admin-api/v1/software-releases/ingest"
    try:
        async with AsyncClient() as client:
            with open(args.package, "rb") as package_file:
                response = await client.post(
                    full_url,
                    headers={"Authorization": "Bearer " + args.api_key},
                    files={"file": package_file},
                )
                response.raise_for_status()  # Raises an exception for 4XX/5XX responses
    except HTTPStatusError as e:
        # Handle HTTP errors that return a response (e.g., 404, 401)
        content_preview = e.response.content[
            :2048
        ]  # Limit the content preview to 2048 bytes
        print("HTTP error occurred.")
        print(
            f"Response status code: {e.response.status_code}. Response content: {str(content_preview)}"
        )
    except RequestError as e:
        # Handle client-side request errors (e.g., network issues)
        print(f"Request error occurred: {e}")
    except Exception as e:
        # Handle other possible errors (e.g., file not found, permission errors)
        print(f"An error occurred: {e}")
