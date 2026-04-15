import requests
from configs import API_URL


def upload_file(file):
    files = {
        "file": (file.name, file.getvalue(), file.type)
    }

    response = requests.post(
        f"{API_URL}/documents",
        files=files
    )

    response.raise_for_status()
    return response.json()