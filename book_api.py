import unicodedata
import requests
import streamlit as st  # デバッグ表示用に追記
from config import *

def get_book_info(title, api_key):
    title = unicodedata.normalize("NFC", title)

    params = {
        "q": title,
        "maxResults": MAX_RESULTS,
        "key": api_key,
    }

    response = requests.get(
        GOOGLE_BOOKS_URL,
        params=params,
        timeout=10
    )

    # 🛠️ デバッグ①：ステータスコードをチェック
    st.write(f"【デバッグ】APIステータスコード: {response.status_code}")

    if response.status_code != 200:
        st.write(f"【デバッグ】APIエラー内容: {response.text}")
        return None

    data = response.json()

    # 🛠️ デバッグ②：検索ヒット件数をチェック
    total_items = data.get("totalItems", 0)
    st.write(f"【デバッグ】API全体のヒット件数: {total_items}")

    if "items" not in data:
        return None

    # 🛠️ デバッグ③：APIが返してきた本のタイトルを一覧表示
    api_titles = [item["volumeInfo"].get("title", "") for item in data["items"]]
    st.write(f"【デバッグ】APIが返したタイトル一覧: {api_titles}")

    for item in data["items"]:
        volume = item["volumeInfo"]

        api_title = unicodedata.normalize(
            "NFC",
            volume.get("title", "")
        )

        # 部分一致チェック
        if (title in api_title) or (api_title in title):
            return {
                "title": api_title,
                "authors": ", ".join(volume.get("authors", [])),
                "publisher": volume.get("publisher", ""),
                "publishedDate": volume.get("publishedDate", ""),
                "description": volume.get("description", ""),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail", "")
            }

    return None
