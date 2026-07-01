import streamlit as st
import numpy as np
import json
import requests
import unicodedata
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# 設定
THRESHOLD = 0.80  # その他と判定する閾値

API_KEY = st.secrets["GOOGLE_BOOKS_API_KEY"]


# Google Books API
API_KEY = st.secrets["GOOGLE_BOOKS_API_KEY"]


def get_book_info(title):

    # Unicodeを正規化
    title = unicodedata.normalize("NFC", title)

    url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        "q": f'intitle:"{title}"',
        "maxResults": 10,
        "key": API_KEY
    }

    response = requests.get(url, params=params)

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

        # タイトル完全一致
        if api_title == title:

            return {
                "title": api_title,
                "authors": ", ".join(volume.get("authors", [])),
                "publisher": volume.get("publisher", ""),
                "publishedDate": volume.get("publishedDate", ""),
                "description": volume.get("description", ""),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail", "")
            }

    # 完全一致なし
    return None
# Streamlit設定
st.set_page_config(
    page_title="本の表紙判定",
    page_icon="📚"
)

st.title("📚 本の表紙判定アプリ")


# モデル読み込み
@st.cache_resource
def load_ai_model():
    return load_model("model.keras")


model = load_ai_model()


# クラス名読み込み
@st.cache_data
def load_class_names():
    with open("class_names.json", encoding="utf-8") as f:
        return json.load(f)


class_names = load_class_names()


# 画像アップロード
uploaded_file = st.file_uploader(
    "画像をアップロードしてください",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="アップロード画像",
        use_container_width=True
    )

    if st.button("判定する"):

        # 前処理
        img = image.resize((256, 256))

        x = img_to_array(img)
        x = x / 255.0
        x = np.expand_dims(x, axis=0)

        # 推論
        pred = model.predict(x, verbose=0)

        pred_index = np.argmax(pred)

        score = pred[0][pred_index]

        # 判定結果
        if score >= THRESHOLD:

            title = class_names[pred_index]

            st.success(f"📚 予測：{title}")

            st.write(f"信頼度：{score:.2%}")

        else:

            title = "その他"

            st.warning("📕 登録されていない本の可能性があります")

            st.write(f"最高信頼度：{score:.2%}")

        # Top3表示
        st.divider()

        st.subheader("Top3候補")

        top3_index = np.argsort(pred[0])[::-1][:3]

        for rank, i in enumerate(top3_index, start=1):

            prob = pred[0][i]

            st.write(f"{rank}位　{class_names[i]}")

            st.progress(float(prob))

            st.write(f"{prob:.2%}")
        # Google Books API
        if title != "その他":

            book = get_book_info(title)

            if book:

                st.divider()

                st.subheader("📖 書籍情報")

                if book["thumbnail"]:
                    st.image(book["thumbnail"], width=200)

                st.write(f"**タイトル**：{book['title']}")

                st.write(f"**著者**：{book['authors']}")

                st.write(f"**出版社**：{book['publisher']}")

                st.write(f"**発売日**：{book['publishedDate']}")

                st.write("### あらすじ")

                st.write(book["description"])