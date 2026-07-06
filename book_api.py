import unicodedata
import requests
from config import *

def get_book_info(title, api_key):
    title = unicodedata.normalize("NFC", title)

    params = {
        "q": f'intitle:"{title}"',
        "maxResults": MAX_RESULTS,
        "key": api_key,
    }

    response = requests.get(
        GOOGLE_BOOKS_URL,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if "items" not in data:
        return None

    for item in data["items"]:
        volume = item["volumeInfo"]

        api_title = unicodedata.normalize(
            "NFC",
            volume.get("title", "")
        )

        if api_title == title:
            return {
                "title": api_title,
                "authors": ", ".join(volume.get("authors", [])),
                "publisher": volume.get("publisher", ""),
                "publishedDate": volume.get("publishedDate", ""),
                "description": volume.get("description", ""),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail", "")
            }

    return None