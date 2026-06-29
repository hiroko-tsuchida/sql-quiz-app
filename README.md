# SQL 問題集アプリ（MySQL）

**🚀 デモはこちら → https://sql-quiz-app-gwxtxysinus2s8fmtnappae.streamlit.app/**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sql-quiz-app-gwxtxysinus2s8fmtnappae.streamlit.app/)

SQL を **やさしいレベルから順番に** 学べる、3択クイズ形式の学習アプリです。
レベルを1つずつ攻略していく「ステージ制」で、各問題は **正しい SQL（MySQL 構文）を
4つの選択肢から選ぶ** 形式。答え合わせをすると、**やさしい日本語の解説** と
**よくある間違い** が表示されます。

> Streamlit 製。データベースは不要（サンプルデータをアプリ内に持っています）。

## 特長

- **全12レベル**：Lv1（超基礎の SELECT）→ WHERE・条件・データ操作（INSERT/
  UPDATE/DELETE）→ 集計・結合 → Lv12（ウィンドウ関数）まで、やさしい順に挑戦。
  どのレベルからでも自由に選べます
- **3択クイズ**：選択肢は「ありがちな間違い」で構成。答え合わせで正誤・解説・
  ポイントを表示
- **合格判定と再挑戦**：レベルの問題を解き切ると点数を表示。間違えた問題だけを
  **「もう一度」** で再挑戦でき、**全問正解で合格**
- **構文のヒント**：各問題に「💡 ヒントを見る（構文の意味）」を用意（見なくても解ける）
- **レベルごとの点数** をサイドバーに表示
- 全 47 問。すべてに段階的な解説とヒント付き

## 題材のテーブル

| テーブル | 内容 |
|----------|------|
| `departments` | 部署 |
| `employees`   | 社員（部署・月給・入社日・上司など） |
| `products`    | 商品 |
| `orders`      | 注文（どの社員がどの商品を売ったか） |

テーブル定義とサンプルデータは、アプリ内（折りたたみ）でいつでも参照できます。
答え合わせをすると、正解 SQL を **インメモリの SQLite で実際に実行した結果（表）** も
表示されるので、「この SQL を書くと何が出るのか」を目で確かめながら学べます。

## 起動方法

```bash
# 1. 依存パッケージのインストール
pip install -r requirements.txt

# 2. 起動
streamlit run app.py
```

起動するとブラウザが開きます。サイドバーで Lv1 を選び「▶️ スタート」から挑戦してください。

## ファイル構成

```
sql-quiz-app/
├── app.py                 # Streamlit 本体（画面・レベル攻略の流れ）
├── quiz_logic.py          # 画面に依存しない純粋ロジック（出題・進捗の保存/復元）
├── runner.py              # 正解 SQL をインメモリ SQLite で実行し結果表を作る
├── problems.py            # 問題データ（47問）とレベルの定義
├── schema.py              # テーブル定義とサンプルデータ
├── tests/                 # pytest によるテスト（純関数 + 問題データの整合性）
├── requirements.txt       # 依存パッケージ
├── requirements-dev.txt   # 開発・テスト用の追加パッケージ
└── README.md              # このファイル
```

## テスト

純粋ロジック（`quiz_logic.py`）と、問題データ（`problems.py`）の整合性を
pytest で検証しています。データ検証では「`answer_sql` が正解の選択肢と一致するか」
「`id` の重複が無いか」「全レベルに問題があるか」などを47問すべてについて自動チェックします。

```bash
pip install -r requirements-dev.txt
pytest
```

## カスタマイズ

- **問題を追加する**：`problems.py` の `PROBLEMS` に辞書を1つ足すだけです。
  `id` / `topic` / `level`(1〜12) / `question` / `hint` / `choices`(4つ) /
  `answer_index` / `answer_sql` / `explanation` / `points` を埋めてください。
  追加後は `pytest` を実行すると、データの書き間違いをまとめて確認できます。
- **レベルを変える**：`problems.py` の `LEVELS`（タイトル・説明）を編集します。
- **題材データを変える**：`schema.py` の各 DataFrame と `CREATE_STATEMENTS` を編集します。
