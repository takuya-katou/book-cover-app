# Book Cover Recognition App

本の表紙画像をアップロードすると、AIが書籍を判定し、Google Books APIから書籍情報を取得するWebアプリです。
判定対象は2026年までの本屋大賞受賞作品のみです。

## デモ

### 主な機能

* 本の表紙画像をアップロード
* TensorFlowモデルによる書籍判定
* Top3の予測候補を表示
* Google Books APIから書籍情報を取得
* タイトル・著者・出版社・発売日・あらすじ・表紙画像を表示

---

## システム構成

```text
画像アップロード
        │
        ▼
画像前処理
        │
        ▼
TensorFlowモデルで推論
        │
        ▼
Top3候補表示
        │
        ▼
Google Books API
        │
        ▼
書籍情報表示
```

---

## 使用技術

- Python
- TensorFlow
- Keras
- Streamlit
- Google Books API

---

## ディレクトリ構成

```text
book-cover-app/
│
├── app.py                # Streamlitアプリ
├── book_api.py           # Google Books API処理
├── config.py             # 定数管理
├── class_names.json      # クラス名一覧
├── model.keras           # 学習済みモデル
├── requirements.txt
└── README.md
```

---

## セットアップ

### リポジトリをクローン

```bash
git clone https://github.com/takuya-katou/book-cover-app.git

cd book-cover-app
```

### ライブラリをインストール

```bash
pip install -r requirements.txt
```

### Google Books APIキーを設定

`.streamlit/secrets.toml`

```toml
GOOGLE_BOOKS_API_KEY = "YOUR_API_KEY"
```

---

## 起動方法

```bash
streamlit run app.py
```

ブラウザで表示されたURLへアクセスするとアプリを利用できます。
