# 🩺 Doctor Support AI

**Doctor Support AI** は、FastAPIとGradioをベースにした日本語対応の医療質問応答システムです。
ユーザーの質問に対して、RAG（Retrieval-Augmented Generation）手法で医療ドキュメントから情報を検索し、OpenAIのGPTモデルを用いてカジュアルかつ簡潔に回答を生成します。

---

## 🚀 機能概要

* FastAPI 経由のAPIエンドポイント `/ask` による質問応答
* Gradio UIによる対話型Webチャット
* Ragie API を利用した情報検索（スコープフィルタリングあり）
* GPT-3.5-turbo による自然な日本語応答生成
* トークン数制限に基づく検索コンテキストのトリミング
* Markdown装飾による読みやすい回答出力

---

## 📁 ファイル構成

```
.
├── app.py   # FastAPIとGradio UIの両方を提供するメインアプリケーション
├── .env     # APIキーなどの環境変数を定義
├── requirements.txt # 依存パッケージの定義  
```

---

## 🧑‍💻 使用方法

### 1. 依存パッケージのインストール

本プロジェクトで必要なPythonパッケージは `requirements.txt` にまとめています。
以下のコマンドで一括インストールしてください。

```bash
pip install -r requirements.txt
```

---

これをREADMEの「🧑‍💻 使用方法」セクションの先頭などに追加するとわかりやすいです。必要があれば全文に組み込みもできます。

### 2. `.env` ファイルの作成

以下のようにAPIキーを設定します。

```env
OPENAI_API_KEY=your_openai_api_key
RAGIE_API_KEY=your_ragie_api_key
```

### 3. Gradio UI の起動

```bash
python app.py
```

ブラウザで `http://localhost:7860` を開くと、対話型チャットUIが利用可能です。

### 4. FastAPI API の起動

別途、FastAPI APIを起動するには：

```bash
uvicorn app:app --reload
```

APIエンドポイント `POST /ask` に以下のようなJSONを送信します：

```json
{
  "query": "高血圧の治療方法は？",
  "history": []
}
```

---

## 🔧 内部仕様

### 🔎 情報検索（Ragie）

* Ragie API を使って、`scope="tutorial"` に該当する情報を取得します。
* トークン数制限（最大10,000トークン）を超えないように検索結果をフィルタリング。

### 💬 回答生成（OpenAI GPT）

* 取得した情報をプロンプトとして `gpt-3.5-turbo` に送信。
* 応答はMarkdownで装飾され、日本語で簡潔かつカジュアルに返されます。

---

## 📌 注意点

* APIキーの取り扱いには十分ご注意ください。

---

## 🛠 今後の展望

* 質問履歴（`history`）の活用による文脈応答の強化
* スコープの動的切替対応
* UI改善と多言語対応

---

## 📃 ライセンス

このプロジェクトは商用利用を前提としていません。個人または研究用途での使用を推奨します。

---

何か問題があればIssueやPRでご報告ください！
