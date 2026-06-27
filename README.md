# SQL 問題集アプリ（MySQL）

**🚀 デモはこちら → https://sql-quiz-app-gwxtxysinus2s8fmtnappae.streamlit.app/**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sql-quiz-app-gwxtxysinus2s8fmtnappae.streamlit.app/)

SQL を **やさしいレベルから順番に** 学べる、4択クイズ形式の学習アプリです。
レベルを1つずつ攻略していく「ステージ制」で、各問題は **正しい SQL（MySQL 構文）を
4つの選択肢から選ぶ** 形式。答え合わせをすると、**やさしい日本語の解説** と
**よくある間違い** が表示されます。

> Streamlit 製。データベースは不要（サンプルデータをアプリ内に持っています）。

## 特長

- **全5レベルのステージ制**：Lv1（超基礎の SELECT/WHERE）→ Lv5（サブクエリ・
  ウィンドウ関数）まで、やさしい順に挑戦
- **4択クイズ**：選択肢は「ありがちな間違い」で構成。答え合わせで正誤・解説・
  ポイントを表示
- **合格判定と再挑戦**：レベルの問題を解き切ると点数を表示。間違えた問題だけを
  **「もう一度」** で再挑戦でき、**全問正解で合格 → 次のレベルが解放**
- **構文のヒント**：各問題に「💡 ヒントを見る（構文の意味）」を用意（見なくても解ける）
- **レベルごとの点数** をサイドバーに表示
- 全 27 問。すべてに段階的な解説とヒント付き

## 題材のテーブル

| テーブル | 内容 |
|----------|------|
| `departments` | 部署 |
| `employees`   | 社員（部署・月給・入社日・上司など） |
| `products`    | 商品 |
| `orders`      | 注文（どの社員がどの商品を売ったか） |

テーブル定義とサンプルデータは、アプリ内（折りたたみ）でいつでも参照できます。
※ SQL を実際に実行はしません。「正しい SQL を選んで解説で学ぶ」ことに集中できます。

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
├── app.py            # Streamlit 本体（画面・レベル攻略の流れ）
├── problems.py       # 問題データ（27問）とレベルの定義
├── schema.py         # テーブル定義とサンプルデータ
├── requirements.txt  # 依存パッケージ
└── README.md         # このファイル
```

## カスタマイズ

- **問題を追加する**：`problems.py` の `PROBLEMS` に辞書を1つ足すだけです。
  `id` / `topic` / `level`(1〜5) / `question` / `hint` / `choices`(4つ) /
  `answer_index` / `answer_sql` / `explanation` / `points` を埋めてください。
- **レベルを変える**：`problems.py` の `LEVELS`（タイトル・説明）を編集します。
- **題材データを変える**：`schema.py` の各 DataFrame と `CREATE_STATEMENTS` を編集します。
