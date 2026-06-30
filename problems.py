"""SQL 問題集のデータ（MySQL 構文）。

1 問は辞書（dict）で表します。キーの意味:
  id          … 通し番号
  topic       … 項目（トピック）。学習の区分け
  level       … 攻略レベル 1〜15（小さいほどやさしい。下の LEVELS と対応）
  question    … 問題文
  choices     … 4つの選択肢（SQL 文字列のリスト）。1つだけが正解
  answer_index… choices の中で正解が何番目か（0〜3）
  answer_sql  … 正解の SQL（= choices[answer_index] と同じ内容）
  explanation … なぜそうなるかの解説（やさしい日本語）
  points      … ポイント / よくある間違い

題材のテーブルは schema.py を参照してください。
"""

# 項目（トピック）の並び順。アプリのメニューでこの順に出します。
TOPICS = [
    "SELECT と WHERE",
    "データ操作（INSERT/UPDATE/DELETE）",
    "並び替え・重複除去",
    "集計関数と GROUP BY",
    "テーブル結合（JOIN）",
    "サブクエリ",
    "文字列・日付の関数",
    "CASE 式と条件分岐",
    "ウィンドウ関数",
]

# レベル（攻略の段階）。やさしい順に Lv1〜Lv15。
# 各問題の "level" がこの番号に対応します。どのレベルからでも挑戦できます。
LEVELS = [
    {"level": 1,  "title": "SQL はじめの一歩", "desc": "まずはここから・SELECT で取り出す・* はすべての列"},
    {"level": 2,  "title": "SELECT の基本", "desc": "全部のデータを取り出す・列を選ぶ・* の使い方"},
    {"level": 3,  "title": "列の選び方と計算", "desc": "別の表・列の順番・別名(AS)・計算した列"},
    {"level": 4,  "title": "WHERE で絞り込む", "desc": "条件で行を選ぶ・比較・NULL / NOT NULL"},
    {"level": 5,  "title": "いろいろな条件①", "desc": "文字列・以下(<=)・等しくない(<>)・IN"},
    {"level": 6,  "title": "いろいろな条件②", "desc": "AND/OR・LIKE・BETWEEN の組み合わせ"},
    {"level": 7,  "title": "データの追加・更新・削除", "desc": "INSERT / UPDATE / DELETE（データ操作の基本）"},
    {"level": 8,  "title": "並び替えと重複", "desc": "ORDER BY（昇順/降順）・DISTINCT・LIMIT"},
    {"level": 9,  "title": "集計（GROUP BY）", "desc": "COUNT/SUM/AVG/MAX・GROUP BY・HAVING"},
    {"level": 10,  "title": "CASE と関数", "desc": "CASE 式・条件分岐・日付のしぼり込み"},
    {"level": 11, "title": "簡単なテーブル結合①", "desc": "2つの表を ON でつなぐ・JOIN のいちばん基本"},
    {"level": 12, "title": "テーブル結合②", "desc": "LEFT JOIN・3つの表・名前（部署名）の組み立て"},
    {"level": 13, "title": "簡単なサブクエリ①", "desc": "() の中で1つの値を求めて = や > で比べる・基本"},
    {"level": 14, "title": "サブクエリ②", "desc": "クエリの中にクエリ・IN / NOT IN・相関サブクエリ"},
    {"level": 15, "title": "ウィンドウ関数", "desc": "RANK・ROW_NUMBER などの総仕上げ"},
]


PROBLEMS = [
    # =====================================================================
    # 項目1: SELECT と WHERE
    # =====================================================================
    {
        "id": 1,
        "hint": (
            "- `WHERE` … 条件にあう「行だけ」を残すフィルター\n"
            "- `>=` は「以上」。ちょうどの値も含みます"
        ),
        "topic": "SELECT と WHERE",
        "level": 4,
        "question": "employees（社員）テーブルの、月給（salary）が 30万円以上の社員の名前（name）と月給（salary）を表示してください。",
        "answer_sql": "SELECT name, salary\nFROM employees\nWHERE salary >= 300000;",
        "choices": [
            "SELECT name, salary\nFROM employees\nWHERE salary > 300000;",
            "SELECT name, salary\nFROM employees\nWHERE salary = 300000;",
            "SELECT name, salary\nFROM employees\nWHERE salary >= 300000;",
            "SELECT name, salary\nFROM employees\nHAVING salary >= 300000;",
        ],
        "answer_index": 2,
        "explanation": (
            "SQL の基本は『どの列を（SELECT）』『どの表から（FROM）』『どの行だけ（WHERE）』の3つです。\n\n"
            "1. `SELECT name, salary` … 表示したい列を指定します。ここでは名前と月給。\n"
            "2. `FROM employees` … どの表を使うか。社員の表ですね。\n"
            "3. `WHERE salary >= 300000` … 条件にあう行だけを残します。"
            "`>=` は『以上』という意味なので、ちょうど 30万円の人も含まれます。"
        ),
        "points": (
            "WHERE は『条件にあう行だけ残すフィルター』だと考えると分かりやすいです。\n"
            "・『30万円より大きい（30万は含まない）』なら `>` を使います。`>=` との違いに注意。"
        ),
    },
    {
        "id": 2,
        "hint": (
            "- `AND` … 2つの条件を「両方とも」満たす\n"
            "- `OR` なら「どちらか一方」でOK"
        ),
        "topic": "SELECT と WHERE",
        "level": 6,
        "question": "employees（社員）テーブルの、営業部（department_id が 1）で月給（salary）が 30万円以上の社員の名前（name）と月給（salary）を表示してください。",
        "answer_sql": (
            "SELECT name, salary\n"
            "FROM employees\n"
            "WHERE department_id = 1\n"
            "  AND salary >= 300000;"
        ),
        "choices": [
            "SELECT name, salary\nFROM employees\nWHERE department_id = 1\n  AND salary >= 300000;",
            "SELECT name, salary\nFROM employees\nWHERE department_id = 1\n  OR salary >= 300000;",
            "SELECT name, salary\nFROM employees\nWHERE department_id = 1\n  AND salary > 300000;",
            "SELECT name, salary\nFROM employees\nWHERE salary >= 300000;",
        ],
        "answer_index": 0,
        "explanation": (
            "条件が2つあるときは `AND` でつなぎます。`AND` は『両方とも満たす』という意味です。\n\n"
            "・`department_id = 1` … 所属が営業部\n"
            "・`salary >= 300000` … 月給が30万円以上\n\n"
            "この2つを `AND` で結ぶと、『営業部 かつ 30万円以上』の人だけが残ります。"
        ),
        "points": (
            "・『どちらか一方でも満たせばよい』ときは `AND` ではなく `OR` を使います。\n"
            "・条件をたくさんつなぐときは、`( )` でくくると意味のまとまりが分かりやすくなります。"
        ),
    },
    {
        "id": 3,
        "hint": (
            "- 値が空っぽの状態を `NULL` と呼ぶ\n"
            "- 空かどうかは `=` ではなく `IS NULL` で調べる"
        ),
        "topic": "SELECT と WHERE",
        "level": 4,
        "question": "employees（社員）テーブルの、上司がいない（manager_id が NULL の）社員の名前（name）を表示してください。",
        "answer_sql": "SELECT name\nFROM employees\nWHERE manager_id IS NULL;",
        "choices": [
            "SELECT name\nFROM employees\nWHERE manager_id = NULL;",
            "SELECT name\nFROM employees\nWHERE manager_id IS NOT NULL;",
            "SELECT name\nFROM employees\nWHERE manager_id <> NULL;",
            "SELECT name\nFROM employees\nWHERE manager_id IS NULL;",
        ],
        "answer_index": 3,
        "explanation": (
            "『値が入っていない』状態を SQL では NULL（ヌル）と呼びます。NULL は特別な存在で、"
            "`= NULL` のように普通のイコールでは比べられません（必ず空振りになります）。\n\n"
            "そのため NULL かどうかを調べるときは、専用の `IS NULL` を使います。\n"
            "・`manager_id IS NULL` … 上司の欄が空っぽの人\n"
            "・逆に『値が入っている人』を出したいときは `IS NOT NULL` を使います。"
        ),
        "points": (
            "よくある間違い: `WHERE manager_id = NULL` と書いてしまうこと。これでは1件も取れません。\n"
            "NULL は『未入力・不明』を表すので、必ず `IS NULL` / `IS NOT NULL` で判定します。"
        ),
    },

    # =====================================================================
    # 項目2: 並び替え・重複除去
    # =====================================================================
    {
        "id": 4,
        "hint": (
            "- `ORDER BY 列` … その列で並び替え\n"
            "- `DESC`=大きい順、`ASC`（省略時）=小さい順"
        ),
        "topic": "並び替え・重複除去",
        "level": 8,
        "question": "employees（社員）テーブルを月給（salary）の高い順に並べて、名前（name）と月給（salary）を表示してください。",
        "answer_sql": "SELECT name, salary\nFROM employees\nORDER BY salary DESC;",
        "choices": [
            "SELECT name, salary\nFROM employees\nORDER BY salary ASC;",
            "SELECT name, salary\nFROM employees\nORDER BY salary DESC;",
            "SELECT name, salary\nFROM employees\nORDER BY salary;",
            "SELECT name, salary\nFROM employees\nSORT BY salary DESC;",
        ],
        "answer_index": 1,
        "explanation": (
            "並び替えは `ORDER BY 列名` で行います。\n\n"
            "・`DESC` … 大きい順（降順）。Descending（下っていく）の略。\n"
            "・`ASC` または何も書かない … 小さい順（昇順）。Ascending（上っていく）の略。\n\n"
            "ここでは月給の高い順なので `ORDER BY salary DESC` とします。"
        ),
        "points": (
            "・`ORDER BY` は SELECT 文のいちばん後ろの方に書きます。\n"
            "・複数の基準で並べたいときは `ORDER BY department_id, salary DESC` のようにカンマで続けます。"
        ),
    },
    {
        "id": 5,
        "hint": (
            "- `DISTINCT` … 同じ値の重複を1つにまとめる\n"
            "- 書く場所は `SELECT` のすぐ後ろ"
        ),
        "topic": "並び替え・重複除去",
        "level": 8,
        "question": "products（商品）テーブルの、カテゴリ（category）を重複なしで一覧表示してください。",
        "answer_sql": "SELECT DISTINCT category\nFROM products;",
        "choices": [
            "SELECT category\nFROM products;",
            "SELECT DISTINCT category\nFROM products;",
            "SELECT UNIQUE category\nFROM products;",
            "SELECT category\nFROM products\nDISTINCT;",
        ],
        "answer_index": 1,
        "explanation": (
            "同じ値が何度も出てくるのを1つにまとめたいときは `DISTINCT` を使います。\n\n"
            "商品表には『電子機器』が2件、『家具』が2件…のように同じカテゴリが複数あります。"
            "`SELECT DISTINCT category` と書くと、重複を取り除いて『電子機器・家具・文具』のように"
            "1種類ずつ表示されます。"
        ),
        "points": (
            "・`DISTINCT` は SELECT の直後に1つだけ書きます。\n"
            "・複数列を指定すると『その組み合わせ』が重複しない行を返します（列ごとに別々ではありません）。"
        ),
    },
    {
        "id": 6,
        "hint": (
            "- まず `ORDER BY` で並べ、`LIMIT 3` で先頭3件\n"
            "- 「上位◯件」は並び替え＋件数しぼりのセット"
        ),
        "topic": "並び替え・重複除去",
        "level": 8,
        "question": "employees（社員）テーブルの、月給（salary）が高い順にトップ3の名前（name）と月給（salary）を表示してください。",
        "answer_sql": (
            "SELECT name, salary\n"
            "FROM employees\n"
            "ORDER BY salary DESC\n"
            "LIMIT 3;"
        ),
        "choices": [
            "SELECT TOP 3 name, salary\nFROM employees\nORDER BY salary DESC;",
            "SELECT name, salary\nFROM employees\nLIMIT 3;",
            "SELECT name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 3;",
            "SELECT name, salary\nFROM employees\nORDER BY salary ASC\nLIMIT 3;",
        ],
        "answer_index": 2,
        "explanation": (
            "『上位◯件だけ』を取り出すには、まず並び替えてから `LIMIT` で件数を絞ります。\n\n"
            "1. `ORDER BY salary DESC` … 月給の高い順に並べる\n"
            "2. `LIMIT 3` … 先頭から3行だけ取り出す\n\n"
            "この2つはセットで使うのがポイントです。並び替えをしないと『どの3件か』が決まりません。"
        ),
        "points": (
            "・`LIMIT` は MySQL の書き方です（SQL Server では `TOP`、Oracle では別の書き方になります）。\n"
            "・『4位以降を飛ばして次の3件』が欲しいときは `LIMIT 3 OFFSET 3` のように OFFSET を足します。"
        ),
    },

    # =====================================================================
    # 項目3: 集計関数と GROUP BY
    # =====================================================================
    {
        "id": 7,
        "hint": (
            "- `COUNT(*)` … 行数（件数）を数える\n"
            "- `*` は「すべての行」"
        ),
        "topic": "集計関数と GROUP BY",
        "level": 9,
        "question": "employees（社員）テーブルに社員が何人いるか数えてください。",
        "answer_sql": "SELECT COUNT(*) AS 人数\nFROM employees;",
        "choices": [
            "SELECT COUNT(*) AS 人数\nFROM employees;",
            "SELECT SUM(*) AS 人数\nFROM employees;",
            "SELECT COUNT(manager_id) AS 人数\nFROM employees;",
            "SELECT COUNT() AS 人数\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "行数（件数）を数えるには `COUNT(*)` を使います。`*` は『すべての行』という意味です。\n\n"
            "・`AS 人数` … 結果の列に分かりやすい見出し（別名）を付けています。なくても動きます。\n\n"
            "COUNT のように、たくさんの行を1つの数字にまとめる関数を『集計関数』と呼びます。"
        ),
        "points": (
            "・`COUNT(*)` は行数を数えます。\n"
            "・`COUNT(manager_id)` のように列名を入れると、その列が NULL の行は数えません。"
            "（＝値が入っている行だけ数える）この違いはよく問われます。"
        ),
    },
    {
        "id": 8,
        "hint": (
            "- `GROUP BY 列` … 同じ値ごとにまとめる\n"
            "- `AVG`=平均（`SUM`=合計, `MAX`/`MIN`=最大/最小）"
        ),
        "topic": "集計関数と GROUP BY",
        "level": 9,
        "question": "employees（社員）テーブルの、部署（department_id）ごとの平均月給を、部署IDとあわせて表示してください。",
        "answer_sql": (
            "SELECT department_id, AVG(salary) AS 平均給料\n"
            "FROM employees\n"
            "GROUP BY department_id;"
        ),
        "choices": [
            "SELECT department_id, AVG(salary) AS 平均給料\nFROM employees;",
            "SELECT department_id, AVG(salary) AS 平均給料\nFROM employees\nGROUP BY department_id;",
            "SELECT department_id, SUM(salary) AS 平均給料\nFROM employees\nGROUP BY department_id;",
            "SELECT department_id, AVG(salary) AS 平均給料\nFROM employees\nGROUP BY salary;",
        ],
        "answer_index": 1,
        "explanation": (
            "『◯◯ごとに集計』と言われたら `GROUP BY` の出番です。\n\n"
            "1. `GROUP BY department_id` … 同じ部署の社員を1つのグループにまとめます。\n"
            "2. `AVG(salary)` … グループごとに月給の平均を計算します。\n\n"
            "結果は『部署ID と その部署の平均給料』が部署の数だけ並びます。"
        ),
        "points": (
            "・SELECT に書ける列は、基本的に『GROUP BY で指定した列』か『集計関数』だけです。\n"
            "・平均=AVG、合計=SUM、最大=MAX、最小=MIN と覚えておくと便利です。"
        ),
    },
    {
        "id": 9,
        "hint": (
            "- まとめた「後」にかける条件は `HAVING`\n"
            "- `WHERE` はまとめる「前」の1行ずつにかける"
        ),
        "topic": "集計関数と GROUP BY",
        "level": 9,
        "question": "employees（社員）テーブルの、社員が 2人以上いる部署の部署IDと人数を表示してください。",
        "answer_sql": (
            "SELECT department_id, COUNT(*) AS 人数\n"
            "FROM employees\n"
            "GROUP BY department_id\n"
            "HAVING COUNT(*) >= 2;"
        ),
        "choices": [
            "SELECT department_id, COUNT(*) AS 人数\nFROM employees\nWHERE COUNT(*) >= 2\nGROUP BY department_id;",
            "SELECT department_id, COUNT(*) AS 人数\nFROM employees\nGROUP BY department_id\nHAVING COUNT(*) >= 2;",
            "SELECT department_id, COUNT(*) AS 人数\nFROM employees\nHAVING COUNT(*) >= 2;",
            "SELECT department_id, COUNT(*) AS 人数\nFROM employees\nGROUP BY department_id\nWHERE COUNT(*) >= 2;",
        ],
        "answer_index": 1,
        "explanation": (
            "『グループにまとめた後の結果』に条件をつけたいときは、`WHERE` ではなく `HAVING` を使います。\n\n"
            "1. `GROUP BY department_id` で部署ごとにまとめる\n"
            "2. `COUNT(*)` で各部署の人数を数える\n"
            "3. `HAVING COUNT(*) >= 2` で『人数が2以上の部署』だけ残す\n\n"
            "WHERE は『まとめる前の1行ずつ』に、HAVING は『まとめた後のグループ』にかける、と覚えましょう。"
        ),
        "points": (
            "よくある間違い: `WHERE COUNT(*) >= 2` と書くこと。COUNT のような集計結果には WHERE は使えません。\n"
            "集計した値で絞り込むときは必ず HAVING を使います。"
        ),
    },

    # =====================================================================
    # 項目4: テーブル結合（JOIN）
    # =====================================================================
    {
        # Lv11 のいちばん最初に置く、やさしい入門の JOIN 問題。
        # 列名がぶつからない orders × products で「ON でつなぐ」基本だけを問う。
        "id": 52,
        "hint": (
            "- `JOIN` … 2つの表をつなげる\n"
            "- `ON A = B` でどの列どうしを合わせるか指定する"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 11,
        "question": "orders（注文）テーブルと products（商品）テーブルを結合して、各注文の商品名（name）と数量（quantity）を表示してください。",
        "answer_sql": (
            "SELECT products.name, orders.quantity\n"
            "FROM orders\n"
            "INNER JOIN products\n"
            "  ON orders.product_id = products.id;"
        ),
        "choices": [
            "SELECT products.name, orders.quantity\nFROM orders\nINNER JOIN products\n  ON orders.product_id = products.id;",
            "SELECT products.name, orders.quantity\nFROM orders\nINNER JOIN products;",
            "SELECT products.name, orders.quantity\nFROM orders\nINNER JOIN products\n  ON orders.id = products.id;",
            "SELECT products.name, orders.quantity\nFROM orders, products;",
        ],
        "answer_index": 0,
        "explanation": (
            "注文の表には商品の『ID（product_id）』しかなく、商品の『名前』は商品の表にあります。"
            "2つの表をつなげて名前を取り出すのが JOIN（結合）です。\n\n"
            "・`INNER JOIN products` … 商品の表をつなげる\n"
            "・`ON orders.product_id = products.id` … "
            "『注文の商品ID』と『商品のID』が一致する行どうしを結びつけます。\n\n"
            "つなげたあとは `products.name`（商品名）や `orders.quantity`（数量）のように"
            "『表名.列名』で取り出せます。"
        ),
        "points": (
            "・JOIN の決め手は `ON` のつなぎ方（どの列とどの列が一致するか）です。\n"
            "・`ON` を書き忘れたり、`FROM orders, products` だけにすると、行が正しく結びつきません。"
        ),
    },
    {
        # Lv11② 注文 × 社員。担当した社員の名前を引いてくる。
        "id": 53,
        "hint": (
            "- 注文の `employee_id` と、社員の `id` を `ON` で合わせる\n"
            "- つなげたら `employees.name` で担当者名を取り出せる"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 11,
        "question": "orders（注文）テーブルと employees（社員）テーブルを結合して、各注文の担当社員の名前（name）と数量（quantity）を表示してください。",
        "answer_sql": (
            "SELECT employees.name, orders.quantity\n"
            "FROM orders\n"
            "INNER JOIN employees\n"
            "  ON orders.employee_id = employees.id;"
        ),
        "choices": [
            "SELECT employees.name, orders.quantity\nFROM orders\nINNER JOIN employees\n  ON orders.employee_id = employees.id;",
            "SELECT employees.name, orders.quantity\nFROM orders\nINNER JOIN employees;",
            "SELECT employees.name, orders.quantity\nFROM orders\nINNER JOIN employees\n  ON orders.id = employees.id;",
            "SELECT employees.name, orders.quantity\nFROM orders, employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "注文の表には『担当した社員のID（employee_id）』しかありません。"
            "社員の名前は社員の表にあるので、JOIN でつなげて取り出します。\n\n"
            "・`INNER JOIN employees` … 社員の表をつなげる\n"
            "・`ON orders.employee_id = employees.id` … "
            "『注文の担当社員ID』と『社員のID』が一致する行どうしを結びつけます。"
        ),
        "points": (
            "・どの列とどの列を合わせるかを `ON` で正しく指定するのが大事です。\n"
            "・`ON` を書かない／`FROM orders, employees` だけ、では正しく結びつきません。"
        ),
    },
    {
        # Lv11③ 社員 × 部署。部署名は別表にあるので JOIN で引く。
        # name が両表にあるので、部署側は AS 部署名 で見出しを分かりやすくする（AS は Lv3 で学習済み）。
        "id": 54,
        "hint": (
            "- 社員の `department_id` と、部署の `id` を `ON` で合わせる\n"
            "- 同じ `name` がぶつかるので部署側は `AS 部署名` で見出しを付ける"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 11,
        "question": "employees（社員）テーブルと departments（部署）テーブルを結合して、各社員の名前（name）と所属する部署名（departments.name）を表示してください。",
        "answer_sql": (
            "SELECT employees.name, departments.name AS 部署名\n"
            "FROM employees\n"
            "INNER JOIN departments\n"
            "  ON employees.department_id = departments.id;"
        ),
        "choices": [
            "SELECT employees.name, departments.name AS 部署名\nFROM employees\nINNER JOIN departments\n  ON employees.department_id = departments.id;",
            "SELECT employees.name, departments.name AS 部署名\nFROM employees\nINNER JOIN departments;",
            "SELECT employees.name, departments.name AS 部署名\nFROM employees\nINNER JOIN departments\n  ON employees.id = departments.id;",
            "SELECT employees.name, departments.name AS 部署名\nFROM employees, departments;",
        ],
        "answer_index": 0,
        "explanation": (
            "社員の表には部署の『ID（department_id）』しかなく、部署名は部署の表にあります。"
            "JOIN でつなげて名前を取り出します。\n\n"
            "・`ON employees.department_id = departments.id` … "
            "『社員の部署ID』と『部署のID』が一致する行どうしを結びつけます。\n"
            "・社員にも部署にも `name` 列があるので、`departments.name AS 部署名` のように"
            "別名（AS）を付けると、どちらの名前か分かりやすくなります。"
        ),
        "points": (
            "・つなぐ列は『社員の department_id』と『部署の id』。`ON` の左右をまちがえないこと。\n"
            "・同じ列名がぶつかるときは `表名.列名` で区別し、`AS` で見出しを付けると読みやすいです。"
        ),
    },
    {
        # Lv11④ 注文 × 商品（id52 と同じ結合を、別の列で練習）。
        "id": 55,
        "hint": (
            "- つなぎ方は id の小さい注文×商品の問題と同じ\n"
            "- 取り出す列を `orders.order_date`（注文日）に変えるだけ"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 11,
        "question": "orders（注文）テーブルと products（商品）テーブルを結合して、各注文の商品名（name）と注文日（order_date）を表示してください。",
        "answer_sql": (
            "SELECT products.name, orders.order_date\n"
            "FROM orders\n"
            "INNER JOIN products\n"
            "  ON orders.product_id = products.id;"
        ),
        "choices": [
            "SELECT products.name, orders.order_date\nFROM orders\nINNER JOIN products\n  ON orders.product_id = products.id;",
            "SELECT products.name, orders.order_date\nFROM orders\nINNER JOIN products;",
            "SELECT products.name, orders.order_date\nFROM orders\nINNER JOIN products\n  ON orders.id = products.id;",
            "SELECT products.name, orders.order_date\nFROM orders, products;",
        ],
        "answer_index": 0,
        "explanation": (
            "つなぎ方は商品名・数量を出したときと同じで、`ON orders.product_id = products.id` です。\n\n"
            "取り出す列を変えるだけで、いろいろな情報を組み合わせて表示できます。"
            "ここでは商品名（`products.name`）と注文日（`orders.order_date`）を並べています。"
        ),
        "points": (
            "・JOIN の `ON` が同じなら、SELECT で取り出す列は自由に選べます。\n"
            "・どの表の列かは `表名.列名` ではっきりさせると、まちがいが減ります。"
        ),
    },
    {
        # Lv11⑤ 社員 × 部署（3列）。54 と同じ結合で、月給も一緒に出す。
        "id": 56,
        "hint": (
            "- 社員 × 部署のつなぎ方は前と同じ（`ON` で department_id = id）\n"
            "- SELECT に `employees.salary` を足すだけ"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 11,
        "question": "employees（社員）テーブルと departments（部署）テーブルを結合して、各社員の名前（name）・部署名（departments.name）・月給（salary）を表示してください。",
        "answer_sql": (
            "SELECT employees.name, departments.name AS 部署名, employees.salary\n"
            "FROM employees\n"
            "INNER JOIN departments\n"
            "  ON employees.department_id = departments.id;"
        ),
        "choices": [
            "SELECT employees.name, departments.name AS 部署名, employees.salary\nFROM employees\nINNER JOIN departments\n  ON employees.department_id = departments.id;",
            "SELECT employees.name, departments.name AS 部署名, employees.salary\nFROM employees\nINNER JOIN departments;",
            "SELECT employees.name, departments.name AS 部署名, employees.salary\nFROM employees\nINNER JOIN departments\n  ON employees.id = departments.id;",
            "SELECT employees.name, departments.name AS 部署名, employees.salary\nFROM employees, departments;",
        ],
        "answer_index": 0,
        "explanation": (
            "結合のしかたは社員名・部署名を出したときと同じです。"
            "`ON employees.department_id = departments.id` でつなぎます。\n\n"
            "あとは SELECT に `employees.salary`（月給）を足すだけで、3列を並べて表示できます。"
        ),
        "points": (
            "・一度つなげてしまえば、両方の表の列を自由に組み合わせて取り出せます。\n"
            "・`employees.salary` のように、どの表の列かを `表名.列名` で示すと安全です。"
        ),
    },
    {
        "id": 10,
        "hint": (
            "- `JOIN` … 2つの表をつなげる\n"
            "- `ON A = B` でどの列どうしを一致させるか指定"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 12,
        "question": "employees（社員）テーブルの各社員について、名前（name）と所属する部署の名前を表示してください。（社員の表にある部署番号を、部署の表で名前に置きかえるイメージです。）",
        "answer_sql": (
            "SELECT employees.name, departments.name AS 部署名\n"
            "FROM employees\n"
            "INNER JOIN departments\n"
            "  ON employees.department_id = departments.id;"
        ),
        "choices": [
            "SELECT employees.name, departments.name AS 部署名\nFROM employees\nINNER JOIN departments\n  ON employees.department_id = departments.id;",
            "SELECT employees.name, departments.name AS 部署名\nFROM employees\nINNER JOIN departments;",
            "SELECT employees.name, departments.name AS 部署名\nFROM employees\nINNER JOIN departments\n  ON employees.id = departments.id;",
            "SELECT employees.name, departments.name AS 部署名\nFROM employees, departments;",
        ],
        "answer_index": 0,
        "explanation": (
            "社員表には部署の『ID』しかなく、部署の『名前』は部署表にあります。"
            "2つの表をつなげて名前を取り出すのが JOIN（結合）です。\n\n"
            "・`INNER JOIN departments` … 部署表をつなげる\n"
            "・`ON employees.department_id = departments.id` … "
            "『社員の部署ID』と『部署のID』が一致する行どうしを結びつける、という指示です。\n\n"
            "同じ name という列が両方の表にあるので、`employees.name` のように"
            "『表名.列名』で区別しています。"
        ),
        "points": (
            "・JOIN の決め手は `ON` のつなぎ方（どの列とどの列が一致するか）です。\n"
            "・`INNER JOIN` は『両方の表にそろっている行』だけを返します。"
        ),
    },
    {
        "id": 11,
        "hint": (
            "- `LEFT JOIN` … 左の表は全部残す（右が無くても消えない）\n"
            "- `COUNT(列名)` は NULL を数えない（0人を正しく出せる）"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 12,
        "question": "departments（部署）テーブルのすべての部署について、部署名と社員数を表示してください。社員が 0人の部署も 0と表示してください。",
        "answer_sql": (
            "SELECT departments.name AS 部署名, COUNT(employees.id) AS 人数\n"
            "FROM departments\n"
            "LEFT JOIN employees\n"
            "  ON departments.id = employees.department_id\n"
            "GROUP BY departments.id, departments.name;"
        ),
        "choices": [
            "SELECT departments.name AS 部署名, COUNT(employees.id) AS 人数\nFROM departments\nINNER JOIN employees\n  ON departments.id = employees.department_id\nGROUP BY departments.id, departments.name;",
            "SELECT departments.name AS 部署名, COUNT(employees.id) AS 人数\nFROM departments\nLEFT JOIN employees\n  ON departments.id = employees.department_id\nGROUP BY departments.id, departments.name;",
            "SELECT departments.name AS 部署名, COUNT(*) AS 人数\nFROM departments\nLEFT JOIN employees\n  ON departments.id = employees.department_id\nGROUP BY departments.id, departments.name;",
            "SELECT departments.name AS 部署名, COUNT(employees.id) AS 人数\nFROM departments\nRIGHT JOIN employees\n  ON departments.id = employees.department_id\nGROUP BY departments.id, departments.name;",
        ],
        "answer_index": 1,
        "explanation": (
            "『社員がいない部署も表示したい』がポイントです。ここで `LEFT JOIN` を使います。\n\n"
            "・`FROM departments LEFT JOIN employees` … 左の表（部署）は全部残し、"
            "右の表（社員）はあれば付ける、という結合です。社員がいない部署も消えません。\n"
            "・`COUNT(employees.id)` … 列名を指定して数えると、NULL（社員がいない部分）は数えません。"
            "だから社員ゼロの部署はちゃんと 0 になります。"
        ),
        "points": (
            "・`INNER JOIN` だと、社員がいない部署は消えてしまいます。『片方しかなくても残したい』なら LEFT JOIN。\n"
            "・ここで `COUNT(*)` にすると、社員ゼロの部署が 1 と数えられてしまうので `COUNT(employees.id)` にします。"
        ),
    },
    {
        "id": 12,
        "hint": (
            "- `JOIN` は何回でも続けて書ける\n"
            "- つなぐたびに `ON` で一致条件を指定する"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 12,
        "question": "orders（注文）テーブルの注文ごとに、担当社員の名前・商品名・数量（quantity）を表示してください。",
        "answer_sql": (
            "SELECT employees.name AS 担当者, products.name AS 商品名, orders.quantity AS 数量\n"
            "FROM orders\n"
            "INNER JOIN employees ON orders.employee_id = employees.id\n"
            "INNER JOIN products  ON orders.product_id  = products.id;"
        ),
        "choices": [
            "SELECT employees.name AS 担当者, products.name AS 商品名, orders.quantity AS 数量\nFROM orders\nINNER JOIN employees ON orders.employee_id = employees.id\nINNER JOIN products  ON orders.product_id  = products.id;",
            "SELECT employees.name AS 担当者, products.name AS 商品名, orders.quantity AS 数量\nFROM orders\nINNER JOIN employees ON orders.employee_id = employees.id;",
            "SELECT employees.name AS 担当者, products.name AS 商品名, orders.quantity AS 数量\nFROM orders\nINNER JOIN employees ON orders.employee_id = employees.id\nINNER JOIN products  ON orders.employee_id = products.id;",
            "SELECT employees.name AS 担当者, products.name AS 商品名, orders.quantity AS 数量\nFROM orders, employees, products;",
        ],
        "answer_index": 0,
        "explanation": (
            "注文表には『社員ID』と『商品ID』しかないので、名前を出すには表を2回つなげます。\n\n"
            "1. まず orders に employees をつなげて、担当者の名前を取れるようにする\n"
            "2. さらに products をつなげて、商品の名前も取れるようにする\n\n"
            "JOIN は何回でも続けて書けます。それぞれに `ON` で『どの列が一致するか』を指定するのがコツです。"
        ),
        "points": (
            "・3つ以上の表をつなぐときも、考え方は2つのときと同じ。1つずつ ON で結んでいきます。\n"
            "・表名が長いときは `FROM orders o` のように別名（エイリアス）を付けると、SQL が短く読みやすくなります。"
        ),
    },

    # =====================================================================
    # 項目5: サブクエリ
    # =====================================================================
    {
        # Lv13 のいちばん最初に置く、やさしい入門のサブクエリ問題。
        # 「() の中で1つの値を求めて、それと = で比べる」基本だけを問う。
        "id": 57,
        "hint": (
            "- `( SELECT ... )` … カッコの中を先に計算して1つの値にする（サブクエリ）\n"
            "- 最高額は `MAX(price)`。その値と `=` で比べる"
        ),
        "topic": "サブクエリ",
        "level": 13,
        "question": "products（商品）テーブルから、単価（price）がいちばん高い商品の名前（name）を表示してください。（サブクエリで最高額を求めて使いましょう。）",
        "answer_sql": (
            "SELECT name\n"
            "FROM products\n"
            "WHERE price = (SELECT MAX(price) FROM products);"
        ),
        "choices": [
            "SELECT name\nFROM products\nWHERE price = (SELECT MAX(price) FROM products);",
            "SELECT name\nFROM products\nWHERE price = MAX(price);",
            "SELECT name\nFROM products\nWHERE price = (SELECT price FROM products);",
            "SELECT name\nFROM products\nWHERE price = (SELECT MAX(price));",
        ],
        "answer_index": 0,
        "explanation": (
            "いちばん高い単価の商品を出すには、まず『最高額』を求めて、その値と一致する商品をさがします。\n\n"
            "・`(SELECT MAX(price) FROM products)` … この丸かっこの中だけで、商品の最高単価を"
            "1つの数字として求めます。これを『サブクエリ（入れ子の SELECT）』と呼びます。\n"
            "・`WHERE price = (…)` … 求めた最高額と同じ単価の商品だけを残します。\n\n"
            "SQL は内側のサブクエリを先に計算し、その結果を使って外側を実行します。"
        ),
        "points": (
            "・`MAX(price)` のような集計は WHERE に直接は書けません。"
            "いったんサブクエリ `(SELECT MAX(price) FROM products)` にして1つの値にしてから比べます。\n"
            "・サブクエリの中でも `FROM products` を書き忘れないようにします。"
        ),
    },
    {
        # Lv13② 社員の最高月給。57 と同じ「= (SELECT MAX ...)」を社員の表で練習。
        "id": 58,
        "hint": (
            "- 最高月給は `MAX(salary)`。サブクエリで1つの値にする\n"
            "- その値と `=` で比べて、同じ月給の社員をさがす"
        ),
        "topic": "サブクエリ",
        "level": 13,
        "question": "employees（社員）テーブルから、月給（salary）がいちばん高い社員の名前（name）を表示してください。（サブクエリで最高額を求めて使いましょう。）",
        "answer_sql": (
            "SELECT name\n"
            "FROM employees\n"
            "WHERE salary = (SELECT MAX(salary) FROM employees);"
        ),
        "choices": [
            "SELECT name\nFROM employees\nWHERE salary = (SELECT MAX(salary) FROM employees);",
            "SELECT name\nFROM employees\nWHERE salary = MAX(salary);",
            "SELECT name\nFROM employees\nWHERE salary = (SELECT salary FROM employees);",
            "SELECT name\nFROM employees\nWHERE salary = (SELECT MAX(salary));",
        ],
        "answer_index": 0,
        "explanation": (
            "いちばん月給が高い社員を出すには、まず『最高月給』を求めて、その値と一致する社員をさがします。\n\n"
            "・`(SELECT MAX(salary) FROM employees)` … この丸かっこの中だけで最高月給を1つの数字として求めます（サブクエリ）。\n"
            "・`WHERE salary = (…)` … 求めた最高額と同じ月給の社員だけを残します。"
        ),
        "points": (
            "・`MAX(salary)` を WHERE に直接は書けません。サブクエリにして1つの値にしてから比べます。\n"
            "・`(SELECT salary FROM employees)` のように複数行を返すサブクエリは `=` では比べられません。"
        ),
    },
    {
        # Lv13③ 最安値の商品。MIN を使うパターン。
        "id": 59,
        "hint": (
            "- 最安値は `MIN(price)`。サブクエリで1つの値にする\n"
            "- その値と `=` で比べて、同じ単価の商品をさがす"
        ),
        "topic": "サブクエリ",
        "level": 13,
        "question": "products（商品）テーブルから、単価（price）がいちばん安い商品の名前（name）を表示してください。（サブクエリで最安値を求めて使いましょう。）",
        "answer_sql": (
            "SELECT name\n"
            "FROM products\n"
            "WHERE price = (SELECT MIN(price) FROM products);"
        ),
        "choices": [
            "SELECT name\nFROM products\nWHERE price = (SELECT MIN(price) FROM products);",
            "SELECT name\nFROM products\nWHERE price = MIN(price);",
            "SELECT name\nFROM products\nWHERE price = (SELECT price FROM products);",
            "SELECT name\nFROM products\nWHERE price = (SELECT MIN(price));",
        ],
        "answer_index": 0,
        "explanation": (
            "いちばん安い商品を出すには、まず『最安値』を `MIN(price)` で求めて、その値と一致する商品をさがします。\n\n"
            "・`(SELECT MIN(price) FROM products)` … 最安値を1つの数字として求めるサブクエリです。\n"
            "・`WHERE price = (…)` … その最安値と同じ単価の商品だけを残します。"
        ),
        "points": (
            "・最大は `MAX`、最小は `MIN`。求めたい値で使い分けます。\n"
            "・集計（MIN）は WHERE に直接書けないので、サブクエリにして1つの値にしてから比べます。"
        ),
    },
    {
        # Lv13④ 平均より高い（> AVG）。比較が = ではなく > のパターン。
        "id": 60,
        "hint": (
            "- 平均は `AVG(price)`。サブクエリで1つの値にする\n"
            "- 「より高い」は `>` で比べる"
        ),
        "topic": "サブクエリ",
        "level": 13,
        "question": "products（商品）テーブルから、平均単価（price の平均）より高い商品の名前（name）と単価（price）を表示してください。",
        "answer_sql": (
            "SELECT name, price\n"
            "FROM products\n"
            "WHERE price > (SELECT AVG(price) FROM products);"
        ),
        "choices": [
            "SELECT name, price\nFROM products\nWHERE price > (SELECT AVG(price) FROM products);",
            "SELECT name, price\nFROM products\nWHERE price > AVG(price);",
            "SELECT name, price\nFROM products\nHAVING price > (SELECT AVG(price) FROM products);",
            "SELECT name, price\nFROM products\nWHERE price > (SELECT price FROM products);",
        ],
        "answer_index": 0,
        "explanation": (
            "平均より高い商品を出すには、まず平均単価を求めて、その値より大きい商品をさがします。\n\n"
            "・`(SELECT AVG(price) FROM products)` … 平均単価を1つの数字として求めるサブクエリです。\n"
            "・`WHERE price > (…)` … 求めた平均より単価が高い商品だけを残します。\n\n"
            "比べ方を `=` から `>` に変えるだけで、『平均より上』が取り出せます。"
        ),
        "points": (
            "・1つの値を返すサブクエリは、`=` だけでなく `>` や `<` でも比べられます。\n"
            "・`AVG(price)` を WHERE に直接は書けません。サブクエリにして1つの値にしてから比べます。"
        ),
    },
    {
        # Lv13⑤ 最も月給が低い社員（MIN を社員の表で）。
        "id": 61,
        "hint": (
            "- 最低額は `MIN(salary)`。サブクエリで1つの値にする\n"
            "- その値と `=` で比べて、同じ月給の社員をさがす"
        ),
        "topic": "サブクエリ",
        "level": 13,
        "question": "employees（社員）テーブルから、月給（salary）がいちばん低い社員の名前（name）を表示してください。（サブクエリで最低額を求めて使いましょう。）",
        "answer_sql": (
            "SELECT name\n"
            "FROM employees\n"
            "WHERE salary = (SELECT MIN(salary) FROM employees);"
        ),
        "choices": [
            "SELECT name\nFROM employees\nWHERE salary = (SELECT MIN(salary) FROM employees);",
            "SELECT name\nFROM employees\nWHERE salary = MIN(salary);",
            "SELECT name\nFROM employees\nWHERE salary = (SELECT salary FROM employees);",
            "SELECT name\nFROM employees\nWHERE salary = (SELECT MIN(salary));",
        ],
        "answer_index": 0,
        "explanation": (
            "いちばん月給が低い社員を出すには、まず『最低月給』を `MIN(salary)` で求めて、その値と一致する社員をさがします。\n\n"
            "・`(SELECT MIN(salary) FROM employees)` … 最低月給を1つの数字として求めるサブクエリです。\n"
            "・`WHERE salary = (…)` … その最低額と同じ月給の社員だけを残します。"
        ),
        "points": (
            "・やり方は最高月給のときと同じで、`MAX` を `MIN` に変えるだけです。\n"
            "・集計は WHERE に直接書けないので、サブクエリにして1つの値にしてから比べます。"
        ),
    },
    {
        "id": 13,
        "hint": (
            "- `( SELECT ... )` … カッコの中を先に計算（サブクエリ）\n"
            "- 1つの値を返すサブクエリは `>` などで比較できる"
        ),
        "topic": "サブクエリ",
        "level": 14,
        "question": "employees（社員）テーブルの、全社員の平均月給より月給（salary）が高い社員の名前（name）と月給（salary）を表示してください。",
        "answer_sql": (
            "SELECT name, salary\n"
            "FROM employees\n"
            "WHERE salary > (SELECT AVG(salary) FROM employees);"
        ),
        "choices": [
            "SELECT name, salary\nFROM employees\nWHERE salary > AVG(salary);",
            "SELECT name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees);",
            "SELECT name, salary\nFROM employees\nHAVING salary > (SELECT AVG(salary) FROM employees);",
            "SELECT name, salary\nFROM employees\nWHERE salary > (SELECT salary FROM employees);",
        ],
        "answer_index": 1,
        "explanation": (
            "『平均より高い人』を出すには、まず平均を計算し、その値と各社員を比べます。\n\n"
            "・`(SELECT AVG(salary) FROM employees)` … この丸かっこの中だけで平均月給を1つの数字として求めます。"
            "これを『サブクエリ（入れ子の SELECT）』と呼びます。\n"
            "・`WHERE salary > (…)` … 求めた平均よりも月給が高い人だけを残します。\n\n"
            "SQL は内側のサブクエリを先に計算し、その結果を使って外側を実行します。"
        ),
        "points": (
            "・1つの値を返すサブクエリは、`> (…)` のように普通の比較で使えます。\n"
            "・平均などの集計をその場で計算して条件に使えるのがサブクエリの便利なところです。"
        ),
    },
    {
        "id": 14,
        "hint": (
            "- `IN (...)` … 一覧の「どれかに一致」\n"
            "- `NOT IN (...)` … 一覧の「どれにも一致しない」"
        ),
        "topic": "サブクエリ",
        "level": 14,
        "question": "employees（社員）テーブルの、一度も注文（orders）を担当していない社員の名前（name）を表示してください。",
        "answer_sql": (
            "SELECT name\n"
            "FROM employees\n"
            "WHERE id NOT IN (SELECT employee_id FROM orders);"
        ),
        "choices": [
            "SELECT name\nFROM employees\nWHERE id IN (SELECT employee_id FROM orders);",
            "SELECT name\nFROM employees\nWHERE id <> (SELECT employee_id FROM orders);",
            "SELECT name\nFROM employees\nWHERE id NOT IN (SELECT employee_id FROM orders);",
            "SELECT name\nFROM employees\nWHERE employee_id NOT IN (SELECT id FROM orders);",
        ],
        "answer_index": 2,
        "explanation": (
            "考え方は『注文を担当した社員のID一覧を作り、その中に入っていない社員を探す』です。\n\n"
            "・`(SELECT employee_id FROM orders)` … 注文を担当した社員IDの一覧（複数の値）を作ります。\n"
            "・`WHERE id NOT IN (…)` … その一覧に『含まれない』社員だけを残します。"
            "`IN` は『どれかに一致』、`NOT IN` は『どれにも一致しない』という意味です。"
        ),
        "points": (
            "・複数の値を返すサブクエリには `IN` / `NOT IN` を組み合わせます。\n"
            "・注意: `NOT IN` の中身に NULL が混ざると結果が0件になることがあります。"
            "今回の employee_id には NULL がないので安全です。"
        ),
    },
    {
        "id": 15,
        "hint": (
            "- 外側の1行ごとに内側を計算し直す（相関サブクエリ）\n"
            "- `department_id = e.department_id` で「同じ部署内」を指す"
        ),
        "topic": "サブクエリ",
        "level": 14,
        "question": "employees（社員）テーブルの、各部署で最も月給（salary）が高い社員の部署ID・名前・月給を表示してください。",
        "answer_sql": (
            "SELECT e.department_id, e.name, e.salary\n"
            "FROM employees e\n"
            "WHERE e.salary = (\n"
            "    SELECT MAX(salary)\n"
            "    FROM employees\n"
            "    WHERE department_id = e.department_id\n"
            ");"
        ),
        "choices": [
            "SELECT e.department_id, e.name, e.salary\nFROM employees e\nWHERE e.salary = (\n    SELECT MAX(salary)\n    FROM employees\n    WHERE department_id = e.department_id\n);",
            "SELECT e.department_id, e.name, e.salary\nFROM employees e\nWHERE e.salary = (\n    SELECT MAX(salary)\n    FROM employees\n);",
            "SELECT e.department_id, e.name, e.salary\nFROM employees e\nWHERE e.salary = MAX(e.salary);",
            "SELECT e.department_id, e.name, e.salary\nFROM employees e\nWHERE e.salary = (\n    SELECT MAX(salary)\n    FROM employees\n    WHERE department_id = department_id\n);",
        ],
        "answer_index": 0,
        "explanation": (
            "『部署ごとの最高額』と『その人自身の月給』が一致する社員を探します。\n\n"
            "・外側の `employees e` は、社員を1人ずつ見ていくイメージです（e は employees の別名）。\n"
            "・内側のサブクエリ `SELECT MAX(salary) ... WHERE department_id = e.department_id` は、"
            "『その社員と同じ部署の中での最高月給』を求めます。外側の e を参照しているのがポイントで、"
            "これを『相関サブクエリ』と呼びます。\n"
            "・両者が一致すれば、その人は部署内トップというわけです。"
        ),
        "points": (
            "・相関サブクエリは、外側の1行ごとに内側を計算し直します。少し難しいですが強力です。\n"
            "・同じことはウィンドウ関数（項目8）でも書けます。上級では複数のやり方を知っておくと役立ちます。"
        ),
    },

    # =====================================================================
    # 項目6: 文字列・日付の関数
    # =====================================================================
    {
        "id": 16,
        "hint": (
            "- `LIKE` … あいまい検索（部分一致など）\n"
            "- `%` は「任意の文字0個以上」。`'%藤%'` で藤を含む"
        ),
        "topic": "文字列・日付の関数",
        "level": 6,
        "question": "employees（社員）テーブルの、名前（name）に『藤』を含む社員の名前（name）を表示してください。",
        "answer_sql": "SELECT name\nFROM employees\nWHERE name LIKE '%藤%';",
        "choices": [
            "SELECT name\nFROM employees\nWHERE name = '%藤%';",
            "SELECT name\nFROM employees\nWHERE name LIKE '藤';",
            "SELECT name\nFROM employees\nWHERE name LIKE '%藤%';",
            "SELECT name\nFROM employees\nWHERE name LIKE '_藤_';",
        ],
        "answer_index": 2,
        "explanation": (
            "『◯◯を含む』のように、あいまいに文字を探すときは `LIKE` を使います。\n\n"
            "・`%`（パーセント）は『任意の文字が0個以上』を表す記号です。\n"
            "・`'%藤%'` は『前に何かあってもよく、後ろに何かあってもよいが、途中に藤がある』という意味。"
            "つまり『藤を含む』名前すべてにマッチします（佐藤・伊藤など）。"
        ),
        "points": (
            "・『藤で始まる』なら `'藤%'`、『藤で終わる』なら `'%藤'` と書きます。\n"
            "・`_`（アンダースコア）は『ちょうど1文字』を表す別の記号です。"
        ),
    },
    {
        "id": 17,
        "hint": (
            "- 日付は `'2020-01-01'`（年-月-日）の形で大小比較できる\n"
            "- `>=` で「その日以降」"
        ),
        "topic": "文字列・日付の関数",
        "level": 10,
        "question": "employees（社員）テーブルの、2020年1月1日以降に入社した（hire_date）社員の名前（name）と入社日（hire_date）を表示してください。",
        "answer_sql": (
            "SELECT name, hire_date\n"
            "FROM employees\n"
            "WHERE hire_date >= '2020-01-01';"
        ),
        "choices": [
            "SELECT name, hire_date\nFROM employees\nWHERE YEAR(hire_date) = 2020;",
            "SELECT name, hire_date\nFROM employees\nWHERE hire_date >= '2020-01-01';",
            "SELECT name, hire_date\nFROM employees\nWHERE hire_date > '2020-01-01';",
            "SELECT name, hire_date\nFROM employees\nWHERE hire_date >= 2020;",
        ],
        "answer_index": 1,
        "explanation": (
            "日付は `'2020-01-01'` のように『年-月-日』の文字列の形で比べられます。\n\n"
            "・`hire_date >= '2020-01-01'` … 2020年の元日以降に入社した人を残します。"
            "日付も数字と同じように、大小（前か後か）を比較できます。\n\n"
            "別解として、年だけを取り出す `YEAR(hire_date) >= 2020` という書き方もあります。"
        ),
        "points": (
            "・MySQL では `YEAR(日付)` で年を、`MONTH(日付)` で月を取り出せます。\n"
            "・範囲で絞るなら `BETWEEN '2020-01-01' AND '2020-12-31'` のような書き方も便利です。"
        ),
    },
    {
        "id": 18,
        "hint": (
            "- `CONCAT(a, b, ...)` … 文字を順につなげて1つにする\n"
            "- MySQL では `+` で文字はつなげない（`+` は計算になる）"
        ),
        "topic": "文字列・日付の関数",
        "level": 12,
        "question": "employees（社員）テーブルの社員一覧を、『佐藤（営業）』のように『名前（部署名）』の形の1列で表示してください。",
        "answer_sql": (
            "SELECT CONCAT(employees.name, '（', departments.name, '）') AS 表示名\n"
            "FROM employees\n"
            "INNER JOIN departments\n"
            "  ON employees.department_id = departments.id;"
        ),
        "choices": [
            "SELECT CONCAT(employees.name, '（', departments.name, '）') AS 表示名\nFROM employees\nINNER JOIN departments\n  ON employees.department_id = departments.id;",
            "SELECT employees.name + '（' + departments.name + '）' AS 表示名\nFROM employees\nINNER JOIN departments\n  ON employees.department_id = departments.id;",
            "SELECT CONCAT(employees.name, '（', departments.name, '）') AS 表示名\nFROM employees;",
            "SELECT CONCAT(employees.name '（' departments.name '）') AS 表示名\nFROM employees\nINNER JOIN departments\n  ON employees.department_id = departments.id;",
        ],
        "answer_index": 0,
        "explanation": (
            "複数の文字をつなげて1つの文字列にするには `CONCAT` を使います。\n\n"
            "・`CONCAT(A, B, C, ...)` … カッコの中の値を順番につなげます。\n"
            "・ここでは『名前』『（』『部署名』『）』の4つをつなげて『佐藤（営業）』を作っています。\n"
            "・部署名は部署表にあるので、JOIN でつなげてから使います。"
        ),
        "points": (
            "・MySQL では `CONCAT` を使います（`+` で文字はつなげません。`+` は計算になります）。\n"
            "・つなげる材料の中に NULL があると、結果全体が NULL になることがあります。"
            "その場合は `COALESCE(列, '')` で空文字に置き換えると安全です。"
        ),
    },

    # =====================================================================
    # 項目7: CASE 式と条件分岐
    # =====================================================================
    {
        "id": 19,
        "hint": (
            "- `CASE WHEN 条件 THEN 値 ELSE 値 END` … if のような分岐\n"
            "- 最後は必ず `END` で閉じる"
        ),
        "topic": "CASE 式と条件分岐",
        "level": 10,
        "question": "employees（社員）テーブルの名前（name）と月給（salary）に加え、月給が 40万円以上なら『高い』、そうでなければ『普通』と表示する列を作ってください。",
        "answer_sql": (
            "SELECT name, salary,\n"
            "       CASE WHEN salary >= 400000 THEN '高い'\n"
            "            ELSE '普通'\n"
            "       END AS 給料区分\n"
            "FROM employees;"
        ),
        "choices": [
            "SELECT name, salary,\n       CASE WHEN salary >= 400000 THEN '高い'\n            ELSE '普通'\n       END AS 給料区分\nFROM employees;",
            "SELECT name, salary,\n       CASE WHEN salary >= 400000 THEN '高い'\n            ELSE '普通'\nFROM employees;",
            "SELECT name, salary,\n       IF salary >= 400000 THEN '高い' ELSE '普通' AS 給料区分\nFROM employees;",
            "SELECT name, salary,\n       CASE WHERE salary >= 400000 THEN '高い'\n            ELSE '普通'\n       END AS 給料区分\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "条件によって表示を変えたいときは `CASE` 式を使います。プログラミングの if 文に似ています。\n\n"
            "・`CASE WHEN 条件 THEN 値 ... ELSE 値 END` という形が基本です。\n"
            "・`WHEN salary >= 400000 THEN '高い'` … 月給40万以上なら『高い』\n"
            "・`ELSE '普通'` … それ以外は『普通』\n"
            "・`END` で CASE の終わりを示し、`AS 給料区分` で列に見出しを付けています。"
        ),
        "points": (
            "・`CASE` は必ず `END` で閉じます。閉じ忘れがよくある間違いです。\n"
            "・`WHEN` は何個でも並べられます。上から順に判定され、最初に当てはまったものが採用されます。"
        ),
    },
    {
        "id": 20,
        "hint": (
            "- `WHEN` は複数並べられ、上から順に最初に当たった所で決まる\n"
            "- 条件は「大きい方から」書くと重なりを防げる"
        ),
        "topic": "CASE 式と条件分岐",
        "level": 10,
        "question": "employees（社員）テーブルの名前（name）と月給（salary）に加え、月給を『40万以上=A』『30万以上=B』『それ未満=C』で表示する列を作ってください。",
        "answer_sql": (
            "SELECT name, salary,\n"
            "       CASE WHEN salary >= 400000 THEN 'A'\n"
            "            WHEN salary >= 300000 THEN 'B'\n"
            "            ELSE 'C'\n"
            "       END AS ランク\n"
            "FROM employees;"
        ),
        "choices": [
            "SELECT name, salary,\n       CASE WHEN salary >= 400000 THEN 'A'\n            WHEN salary >= 300000 THEN 'B'\n            ELSE 'C'\n       END AS ランク\nFROM employees;",
            "SELECT name, salary,\n       CASE WHEN salary >= 300000 THEN 'B'\n            WHEN salary >= 400000 THEN 'A'\n            ELSE 'C'\n       END AS ランク\nFROM employees;",
            "SELECT name, salary,\n       CASE WHEN salary >= 400000 THEN 'A'\n            WHEN salary >= 300000 THEN 'B'\n            ELSE 'C'\nFROM employees;",
            "SELECT name, salary,\n       CASE WHEN salary >= 400000 THEN 'A'\n            ELSEIF salary >= 300000 THEN 'B'\n            ELSE 'C'\n       END AS ランク\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "3段階以上に分けたいときは、`WHEN` を複数並べます。\n\n"
            "ポイントは『上から順に判定され、最初に当てはまった所で止まる』ことです。\n"
            "・まず `salary >= 400000`（40万以上）か調べ、当てはまれば 'A'。\n"
            "・当てはまらなければ次の `salary >= 300000`（30万以上）を調べ、'B'。\n"
            "・どれにも当てはまらなければ `ELSE` の 'C'。\n\n"
            "上から順なので、30万の条件を先に書くと40万以上も全部 B になってしまいます。順番が大切です。"
        ),
        "points": (
            "・条件は『厳しい方（大きい方）から』書くと、重なりを気にせず正しく分けられます。\n"
            "・`ELSE` を省くと、どれにも当てはまらない行はその列が NULL になります。"
        ),
    },
    {
        "id": 21,
        "hint": (
            "- 条件にあう行を数える定番: `SUM(CASE WHEN 条件 THEN 1 ELSE 0 END)`\n"
            "- 1と0に置き換えて合計＝「1の個数」"
        ),
        "topic": "CASE 式と条件分岐",
        "level": 10,
        "question": "employees（社員）テーブルの、部署ごとに月給が 40万円以上の社員の人数を数え、部署IDと人数を表示してください。",
        "answer_sql": (
            "SELECT department_id,\n"
            "       SUM(CASE WHEN salary >= 400000 THEN 1 ELSE 0 END) AS 高給社員数\n"
            "FROM employees\n"
            "GROUP BY department_id;"
        ),
        "choices": [
            "SELECT department_id,\n       SUM(CASE WHEN salary >= 400000 THEN 1 ELSE 0 END) AS 高給社員数\nFROM employees\nGROUP BY department_id;",
            "SELECT department_id,\n       COUNT(CASE WHEN salary >= 400000 THEN 1 ELSE 0 END) AS 高給社員数\nFROM employees\nGROUP BY department_id;",
            "SELECT department_id,\n       SUM(salary >= 400000) AS 高給社員数\nFROM employees\nGROUP BY department_id;",
            "SELECT department_id,\n       SUM(CASE WHEN salary >= 400000 THEN 1 ELSE 0 END) AS 高給社員数\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "『条件にあう行だけ数える』には、CASE と集計をうまく組み合わせます。\n\n"
            "・`CASE WHEN salary >= 400000 THEN 1 ELSE 0 END` … "
            "40万以上の人は 1、そうでない人は 0 に置き換えます。\n"
            "・その 1 と 0 を `SUM` で合計すると、結果として『1の個数＝条件にあう人数』になります。\n"
            "・`GROUP BY department_id` で部署ごとに計算します。\n\n"
            "これは『条件付きで数える』ときの定番テクニックです。"
        ),
        "points": (
            "・`SUM(CASE WHEN 条件 THEN 1 ELSE 0 END)` は『条件を満たす行の数』を数える決まり文句です。\n"
            "・複数の条件別の人数を、1回の集計で横並びに出せるのが強みです（売上集計などで大活躍します）。"
        ),
    },

    # =====================================================================
    # 項目8: ウィンドウ関数
    # =====================================================================
    {
        "id": 22,
        "hint": (
            "- `RANK() OVER (ORDER BY ...)` … 並べた順に順位を付ける\n"
            "- `OVER(...)` の中で「どう並べるか」を指定"
        ),
        "topic": "ウィンドウ関数",
        "level": 15,
        "question": "employees（社員）テーブルの全社員に、月給（salary）の高い順の順位を付け、名前・月給・順位を表示してください。",
        "answer_sql": (
            "SELECT name, salary,\n"
            "       RANK() OVER (ORDER BY salary DESC) AS 順位\n"
            "FROM employees;"
        ),
        "choices": [
            "SELECT name, salary,\n       RANK() OVER (ORDER BY salary DESC) AS 順位\nFROM employees;",
            "SELECT name, salary,\n       RANK() AS 順位\nFROM employees\nORDER BY salary DESC;",
            "SELECT name, salary,\n       RANK(salary) OVER (ORDER BY salary DESC) AS 順位\nFROM employees;",
            "SELECT name, salary,\n       ROW_NUMBER() (ORDER BY salary DESC) AS 順位\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "順位を付けるには『ウィンドウ関数』の `RANK()` が便利です。\n\n"
            "・`RANK() OVER (ORDER BY salary DESC)` … "
            "『月給の高い順に並べたときの順位』を各行に付けます。\n"
            "・`OVER (...)` の中で『どう並べて順位を付けるか』を指定するのが特徴です。\n\n"
            "GROUP BY と違い、ウィンドウ関数は行をまとめずに、1行ずつ残したまま順位や合計を計算できます。"
        ),
        "points": (
            "・`RANK` は同じ値（同順位）があると、次の順位を飛ばします（1,1,3…）。\n"
            "・飛ばしたくないときは `DENSE_RANK`（1,1,2…）、単純な連番なら `ROW_NUMBER` を使います。"
        ),
    },
    {
        "id": 23,
        "hint": (
            "- `PARTITION BY 列` … グループごとに順位をやり直す\n"
            "- `ORDER BY` で各グループ内の並び順を決める"
        ),
        "topic": "ウィンドウ関数",
        "level": 15,
        "question": "employees（社員）テーブルを部署ごとに分け、月給（salary）の高い順に順位を付けて、部署ID・名前・月給と部署内順位を表示してください。",
        "answer_sql": (
            "SELECT department_id, name, salary,\n"
            "       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS 部署内順位\n"
            "FROM employees;"
        ),
        "choices": [
            "SELECT department_id, name, salary,\n       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS 部署内順位\nFROM employees;",
            "SELECT department_id, name, salary,\n       RANK() OVER (ORDER BY salary DESC) AS 部署内順位\nFROM employees;",
            "SELECT department_id, name, salary,\n       RANK() OVER (GROUP BY department_id ORDER BY salary DESC) AS 部署内順位\nFROM employees;",
            "SELECT department_id, name, salary,\n       RANK() OVER (PARTITION BY department_id) AS 部署内順位\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "『部署ごとに順位をやり直す』には、`OVER` の中に `PARTITION BY` を足します。\n\n"
            "・`PARTITION BY department_id` … 部署ごとにグループを区切ります。\n"
            "・`ORDER BY salary DESC` … その区切りの中で月給の高い順に順位を付けます。\n\n"
            "結果として、各部署ごとに『その部署の中での1位・2位…』が付きます。"
            "部署が変わると順位は1に戻ります。"
        ),
        "points": (
            "・`PARTITION BY` は GROUP BY の『グループ分け』に似ていますが、行はまとめずに残します。\n"
            "・`PARTITION BY`（どう区切るか）と `ORDER BY`（区切りの中でどう並べるか）はセットで考えます。"
        ),
    },
    {
        "id": 24,
        "hint": (
            "- ウィンドウ関数の結果は、いったんサブクエリにしてから `WHERE` で絞る\n"
            "- `ROW_NUMBER()` は 1,2,3… の連番"
        ),
        "topic": "ウィンドウ関数",
        "level": 15,
        "question": "employees（社員）テーブルの、各部署で月給（salary）が最も高い社員（部署内1位）の部署ID・名前・月給を表示してください。",
        "answer_sql": (
            "SELECT department_id, name, salary\n"
            "FROM (\n"
            "    SELECT department_id, name, salary,\n"
            "           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn\n"
            "    FROM employees\n"
            ") AS ranked\n"
            "WHERE rn = 1;"
        ),
        "choices": [
            "SELECT department_id, name, salary\nFROM (\n    SELECT department_id, name, salary,\n           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn\n    FROM employees\n) AS ranked\nWHERE rn = 1;",
            "SELECT department_id, name, salary,\n       ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn\nFROM employees\nWHERE rn = 1;",
            "SELECT department_id, name, salary\nFROM (\n    SELECT department_id, name, salary,\n           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn\n    FROM employees\n)\nWHERE rn = 1;",
            "SELECT department_id, name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 1;",
        ],
        "answer_index": 0,
        "explanation": (
            "ウィンドウ関数で付けた順位は、そのままでは WHERE で絞れません（計算の順番の都合です）。"
            "そこで『順位を付けた結果』をいったん中の SELECT で作り、それを外側から絞り込みます。\n\n"
            "1. 内側: `ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC)` で"
            "部署ごとに月給の高い順の連番（rn）を付ける。\n"
            "2. 外側: その結果（ranked という名前を付けた表）から `WHERE rn = 1` で1位だけを取り出す。\n\n"
            "この『サブクエリ＋ウィンドウ関数』は、グループごとの代表を取り出す定番パターンです。"
        ),
        "points": (
            "・同点1位を全員出したいなら `ROW_NUMBER` の代わりに `RANK` を使います"
            "（ROW_NUMBER は同点でも1人だけに 1 を付けます）。\n"
            "・FROM の中のサブクエリには `AS ranked` のように必ず名前（別名）を付けます。"
        ),
    },

    # =====================================================================
    # 追加: Lv1 用のやさしい入門問題（SELECT のいちばん基本）
    # =====================================================================
    {
        "id": 25,
        "hint": (
            "- `SELECT 列 FROM 表` が基本の形\n"
            "- 条件（WHERE）を書かなければ全部の行が出る"
        ),
        "topic": "SELECT と WHERE",
        "level": 2,
        "question": "employees（社員）テーブルにいる社員全員の名前（name）を表示してください。",
        "answer_sql": "SELECT name\nFROM employees;",
        "choices": [
            "SELECT name\nFROM employees;",
            "SELECT employees\nFROM name;",
            "GET name\nFROM employees;",
            "SELECT name;",
        ],
        "answer_index": 0,
        "explanation": (
            "SQL のいちばん基本の形は『どの列を（SELECT）』『どの表から（FROM）』の2つです。\n\n"
            "・`SELECT name` … 表示したい列（ここでは名前）を書きます。\n"
            "・`FROM employees` … どの表から取り出すか（社員の表）を書きます。\n\n"
            "条件（WHERE）を付けなければ、表の全部の行が対象になります。"
        ),
        "points": (
            "・取り出すのは『列の名前』、`FROM` のあとに書くのは『表の名前』です。順番を逆にしないこと。\n"
            "・データを取り出す命令は `GET` ではなく必ず `SELECT` です。"
        ),
    },
    {
        "id": 26,
        "hint": (
            "- `*` … すべての列、という意味\n"
            "- 表は必ず `FROM 表名` で指定する"
        ),
        "topic": "SELECT と WHERE",
        "level": 2,
        "question": "products（商品）テーブルの、すべての列・すべての行を表示してください。",
        "answer_sql": "SELECT *\nFROM products;",
        "choices": [
            "SELECT ALL\nFROM products;",
            "SELECT *\nFROM products;",
            "SELECT *\nproducts;",
            "SELECT products;",
        ],
        "answer_index": 1,
        "explanation": (
            "『すべての列』を表示したいときは、列名を1つずつ書く代わりに `*`（アスタリスク）を使います。\n\n"
            "・`SELECT *` … その表の全部の列、という意味です。\n"
            "・`FROM products` … 商品の表から取り出します。\n\n"
            "条件を付けていないので、全部の行が表示されます。"
        ),
        "points": (
            "・『全部の列』は `*` です。`ALL` ではありません。\n"
            "・表を指定するときは必ず `FROM 表名` の形にします（`FROM` を省けません）。"
        ),
    },
    {
        "id": 27,
        "hint": (
            "- `WHERE` … 条件にあう行だけ残す\n"
            "- SQL の「等しい」は `=`（`==` ではない）。数値はクォート不要"
        ),
        "topic": "SELECT と WHERE",
        "level": 4,
        "question": "employees（社員）テーブルの、営業部（department_id が 1）の社員の名前（name）を表示してください。",
        "answer_sql": "SELECT name\nFROM employees\nWHERE department_id = 1;",
        "choices": [
            "SELECT name\nFROM employees\nWHERE department_id == 1;",
            "SELECT name\nFROM employees\nWHERE department_id = '1';",
            "SELECT name\nFROM employees\nWHERE department_id = 1;",
            "SELECT name\nFROM employees\nIF department_id = 1;",
        ],
        "answer_index": 2,
        "explanation": (
            "『ある条件にあう行だけ』を取り出すときは `WHERE` を使います。\n\n"
            "・`WHERE department_id = 1` … 所属部署の番号が 1（営業部）の人だけを残します。\n"
            "・SQL では『等しい』を `=`（イコール1つ）で書きます。\n\n"
            "数値の 1 と比べるので、クォート（' '）は付けずにそのまま `1` と書きます。"
        ),
        "points": (
            "・SQL の『等しい』は `=` です。プログラミング言語のような `==` は使いません。\n"
            "・行を絞り込むキーワードは `IF` ではなく `WHERE` です。"
        ),
    },

    # =====================================================================
    # 追加: Lv1（SELECT の基本）
    # =====================================================================
    {
        "id": 28,
        "hint": (
            "- 取り出す列が複数あるときは、カンマ `,` で区切って並べる\n"
            "- 書いた順に左から表示される"
        ),
        "topic": "SELECT と WHERE",
        "level": 2,
        "question": "products（商品）テーブルの、名前（name）と単価（price）を表示してください。",
        "answer_sql": "SELECT name, price\nFROM products;",
        "choices": [
            "SELECT name, price\nFROM products;",
            "SELECT name price\nFROM products;",
            "SELECT name AND price\nFROM products;",
            "SELECT name, price;",
        ],
        "answer_index": 0,
        "explanation": (
            "複数の列を取り出すときは、列名をカンマ `,` で区切って並べます。\n\n"
            "・`SELECT name, price` … 名前と単価の2つの列を取り出します。\n"
            "・`FROM products` … 商品の表から取り出します。\n\n"
            "書いた順（name → price）のとおり、左から並んで表示されます。"
        ),
        "points": (
            "・列の区切りは『カンマ』です。スペースだけや `AND` ではつなげません。\n"
            "・`AND` は WHERE の中で条件をつなぐ言葉で、列を並べる役目ではありません。"
        ),
    },
    {
        "id": 29,
        "hint": (
            "- `*` … すべての列、という意味\n"
            "- 表は必ず `FROM 表名` で指定する"
        ),
        "topic": "SELECT と WHERE",
        "level": 3,
        "question": "departments（部署）テーブルの、すべての列・すべての行を表示してください。",
        "answer_sql": "SELECT *\nFROM departments;",
        "choices": [
            "SELECT *\nFROM departments;",
            "SELECT ALL\nFROM departments;",
            "SELECT *\ndepartments;",
            "SELECT departments;",
        ],
        "answer_index": 0,
        "explanation": (
            "『すべての列』を表示したいときは、列名を1つずつ書く代わりに `*`（アスタリスク）を使います。\n\n"
            "・`SELECT *` … その表の全部の列、という意味です。\n"
            "・`FROM departments` … 部署の表から取り出します。"
        ),
        "points": (
            "・『全部の列』は `*` です。`ALL` ではありません。\n"
            "・表を指定するときは必ず `FROM 表名` の形にします。"
        ),
    },
    {
        "id": 30,
        "hint": (
            "- `SELECT` のあとに書いた順番で、列が左から並ぶ\n"
            "- 列の区切りはカンマ `,`"
        ),
        "topic": "SELECT と WHERE",
        "level": 3,
        "question": "employees（社員）テーブルの月給（salary）と名前（name）を、『月給 → 名前』の順で表示してください。",
        "answer_sql": "SELECT salary, name\nFROM employees;",
        "choices": [
            "SELECT salary, name\nFROM employees;",
            "SELECT name, salary\nFROM employees;",
            "SELECT salary name\nFROM employees;",
            "SELECT salary, name;",
        ],
        "answer_index": 0,
        "explanation": (
            "表示される列の順番は、`SELECT` のあとに書いた順番で決まります。\n\n"
            "・`SELECT salary, name` … 月給・名前の順で表示されます。\n"
            "・もし `name, salary` と書くと、名前・月給の順になってしまいます。"
        ),
        "points": (
            "・列の並び順は『書いた順』。指定された順番どおりに書きましょう。\n"
            "・列の区切りはカンマです（`salary name` のようにスペースだけではダメ）。"
        ),
    },

    # =====================================================================
    # 追加: Lv2（WHERE で絞り込む）
    # =====================================================================
    {
        "id": 31,
        "hint": (
            "- 文字（文字列）と比べるときは、値を `' '`（シングルクォート）で囲む\n"
            "- 数値はクォート不要だが、文字は必要"
        ),
        "topic": "SELECT と WHERE",
        "level": 5,
        "question": "products（商品）テーブルの、カテゴリ（category）が「家具」の商品の名前（name）を表示してください。",
        "answer_sql": "SELECT name\nFROM products\nWHERE category = '家具';",
        "choices": [
            "SELECT name\nFROM products\nWHERE category = '家具';",
            "SELECT name\nFROM products\nWHERE category = 家具;",
            "SELECT name\nFROM products\nWHERE name = '家具';",
            "SELECT name\nFROM products\nHAVING category = '家具';",
        ],
        "answer_index": 0,
        "explanation": (
            "文字（文字列）で絞り込むときは、比べる値を `' '`（シングルクォート）で囲みます。\n\n"
            "・`WHERE category = '家具'` … カテゴリが『家具』の行だけを残します。\n\n"
            "数値（たとえば 1）はクォートなしで書きますが、文字はクォートで囲むのが決まりです。"
        ),
        "points": (
            "・文字をクォートで囲み忘れると、SQL は『家具』を列の名前だと勘違いしてエラーになります。\n"
            "・行をしぼり込むのは `WHERE`。`HAVING` は集計（GROUP BY）と一緒に使うものです。"
        ),
    },
    {
        "id": 32,
        "hint": (
            "- `<=` は「以下」。ちょうどの値も含む\n"
            "- 不等号は `<=` の順で書く（`=<` とは書かない）"
        ),
        "topic": "SELECT と WHERE",
        "level": 5,
        "question": "products（商品）テーブルの、単価（price）が 2500円以下の商品の名前（name）と単価（price）を表示してください。",
        "answer_sql": "SELECT name, price\nFROM products\nWHERE price <= 2500;",
        "choices": [
            "SELECT name, price\nFROM products\nWHERE price <= 2500;",
            "SELECT name, price\nFROM products\nWHERE price < 2500;",
            "SELECT name, price\nFROM products\nWHERE price =< 2500;",
            "SELECT name, price\nFROM products\nWHERE price >= 2500;",
        ],
        "answer_index": 0,
        "explanation": (
            "『◯◯以下』は `<=` で表します。`<=` は『その値も含めて、それより小さい』という意味です。\n\n"
            "・`WHERE price <= 2500` … 単価が 2500円ちょうど、または それより安い商品が残ります。\n\n"
            "もし `<`（小なり）だけだと、2500円ちょうどの商品が外れてしまいます。"
        ),
        "points": (
            "・『以下』は `<=`、『より小さい（その値は含まない）』は `<`。ちょうどを含むかで使い分けます。\n"
            "・不等号は `<=` の順で書きます。`=<` と書くとエラーになります。"
        ),
    },

    # =====================================================================
    # 追加: Lv3（条件の組み合わせ）
    # =====================================================================
    {
        "id": 33,
        "hint": (
            "- `OR` … 2つの条件の「どちらか一方」を満たせばよい\n"
            "- 両方を満たす必要があるときは `AND`"
        ),
        "topic": "SELECT と WHERE",
        "level": 6,
        "question": "employees（社員）テーブルの、営業部（department_id が 1）、または月給（salary）が 40万円以上の社員の名前（name）を表示してください。",
        "answer_sql": (
            "SELECT name\n"
            "FROM employees\n"
            "WHERE department_id = 1\n"
            "  OR salary >= 400000;"
        ),
        "choices": [
            "SELECT name\nFROM employees\nWHERE department_id = 1\n  OR salary >= 400000;",
            "SELECT name\nFROM employees\nWHERE department_id = 1\n  AND salary >= 400000;",
            "SELECT name\nFROM employees\nWHERE department_id = 1, salary >= 400000;",
            "SELECT name\nFROM employees\nWHERE department_id = 1\n  OR salary => 400000;",
        ],
        "answer_index": 0,
        "explanation": (
            "『どちらか一方を満たせばよい』ときは、条件を `OR` でつなぎます。\n\n"
            "・`department_id = 1` … 営業部\n"
            "・`salary >= 400000` … 月給40万円以上\n\n"
            "この2つを `OR` で結ぶと、『営業部の人』と『40万円以上の人』の両方が残ります。"
        ),
        "points": (
            "・『両方とも満たす』なら `AND`、『どちらか一方でよい』なら `OR` を使います。\n"
            "・条件はカンマ `,` ではつなげません。`AND` か `OR` を使います。"
        ),
    },
    {
        "id": 34,
        "hint": (
            "- 「等しくない」は `<>` で表す（MySQL では `!=` も同じ）\n"
            "- 文字と比べるので値は `' '` で囲む"
        ),
        "topic": "SELECT と WHERE",
        "level": 5,
        "question": "products（商品）テーブルの、カテゴリ（category）が「文具」でない商品の名前（name）とカテゴリ（category）を表示してください。",
        "answer_sql": "SELECT name, category\nFROM products\nWHERE category <> '文具';",
        "choices": [
            "SELECT name, category\nFROM products\nWHERE category <> '文具';",
            "SELECT name, category\nFROM products\nWHERE category = '文具';",
            "SELECT name, category\nFROM products\nWHERE category NOT '文具';",
            "SELECT name, category\nFROM products\nWHERE NOT category = 文具;",
        ],
        "answer_index": 0,
        "explanation": (
            "『◯◯でない（等しくない）』は `<>` で表します。\n\n"
            "・`WHERE category <> '文具'` … カテゴリが『文具』以外の行だけを残します。\n\n"
            "文字と比べるので、値は `' '`（シングルクォート）で囲みます。"
        ),
        "points": (
            "・『等しくない』は `<>` です。MySQL では `!=` も同じ意味で使えます。\n"
            "・`category NOT '文具'` のような書き方はできません。否定は `<>`（または `!=`）です。"
        ),
    },
    {
        "id": 35,
        "hint": (
            "- `BETWEEN A AND B` … 「A以上 B以下」の範囲（A と B も含む）\n"
            "- 範囲のときは `>=` と `<=` を2つ書くかわりに使える"
        ),
        "topic": "SELECT と WHERE",
        "level": 6,
        "question": "products（商品）テーブルの、単価（price）が 1000円以上 30000円以下の商品の名前（name）と単価（price）を表示してください。",
        "answer_sql": (
            "SELECT name, price\n"
            "FROM products\n"
            "WHERE price BETWEEN 1000 AND 30000;"
        ),
        "choices": [
            "SELECT name, price\nFROM products\nWHERE price BETWEEN 1000 AND 30000;",
            "SELECT name, price\nFROM products\nWHERE price BETWEEN 1000 OR 30000;",
            "SELECT name, price\nFROM products\nWHERE price IN (1000, 30000);",
            "SELECT name, price\nFROM products\nWHERE price >= 1000 OR price <= 30000;",
        ],
        "answer_index": 0,
        "explanation": (
            "ある範囲を指定するときは `BETWEEN A AND B` が便利です。"
            "『A以上 B以下』を表し、A と B もその範囲に含みます。\n\n"
            "・`price BETWEEN 1000 AND 30000` … 単価が 1000円〜30000円の商品が残ります。\n\n"
            "これは `price >= 1000 AND price <= 30000` と同じ意味です。"
        ),
        "points": (
            "・`BETWEEN` は必ず `AND` とセット（`OR` ではありません）。\n"
            "・`IN (1000, 30000)` は『1000 か 30000 ちょうど』だけになり、範囲にはなりません。"
        ),
    },

    # =====================================================================
    # 追加: Lv4（データの追加・更新・削除 / INSERT・UPDATE・DELETE）
    # =====================================================================
    {
        "id": 36,
        "hint": (
            "- データの追加は `INSERT INTO 表名 (列...) VALUES (値...);`\n"
            "- 文字は `' '` で囲み、数値はそのまま書く"
        ),
        "topic": "データ操作（INSERT/UPDATE/DELETE）",
        "level": 7,
        "question": "departments（部署）テーブルに、id=5・name「総務」の行を1件追加してください。",
        "answer_sql": "INSERT INTO departments (id, name)\nVALUES (5, '総務');",
        "choices": [
            "INSERT INTO departments (id, name)\nVALUES (5, '総務');",
            "INSERT departments (id, name)\nVALUES (5, '総務');",
            "INSERT INTO departments\nSET (5, '総務');",
            "UPDATE departments\nSET id = 5, name = '総務';",
        ],
        "answer_index": 0,
        "explanation": (
            "データを1件追加するときは `INSERT INTO` を使います。\n\n"
            "・`INSERT INTO departments (id, name)` … どの表の、どの列に入れるか。\n"
            "・`VALUES (5, '総務')` … その列に入れる値。列の順番と値の順番をそろえます。\n\n"
            "id は数値なのでそのまま、name は文字なので `' '` で囲みます。"
        ),
        "points": (
            "・`INSERT` のあとには `INTO` が必要です。\n"
            "・列のならびと VALUES のならびは、同じ順番にそろえます。"
        ),
    },
    {
        "id": 37,
        "hint": (
            "- データの変更は `UPDATE 表名 SET 列 = 値 WHERE 条件;`\n"
            "- `WHERE` を付け忘れると、全部の行が変わってしまう"
        ),
        "topic": "データ操作（INSERT/UPDATE/DELETE）",
        "level": 7,
        "question": "employees（社員）テーブルの id が 3 の人の月給（salary）を 30万円（300000）に変更してください。",
        "answer_sql": "UPDATE employees\nSET salary = 300000\nWHERE id = 3;",
        "choices": [
            "UPDATE employees\nSET salary = 300000\nWHERE id = 3;",
            "UPDATE employees\nSET salary = 300000;",
            "UPDATE employees\nsalary = 300000\nWHERE id = 3;",
            "INSERT INTO employees\nSET salary = 300000\nWHERE id = 3;",
        ],
        "answer_index": 0,
        "explanation": (
            "データを変更するときは `UPDATE` を使います。\n\n"
            "・`UPDATE employees` … どの表を変更するか。\n"
            "・`SET salary = 300000` … どの列をどんな値にするか。\n"
            "・`WHERE id = 3` … どの行を変えるか。ここが大事です。"
        ),
        "points": (
            "・`WHERE` を付け忘れると、表の『全部の行』の月給が書き換わってしまいます。要注意。\n"
            "・変更する値は `SET 列 = 値` の形で書きます。"
        ),
    },
    {
        "id": 38,
        "hint": (
            "- データの削除は `DELETE FROM 表名 WHERE 条件;`\n"
            "- `WHERE` を付け忘れると、全部の行が消えてしまう"
        ),
        "topic": "データ操作（INSERT/UPDATE/DELETE）",
        "level": 7,
        "question": "orders（注文）テーブルの id が 10 の行を1件削除してください。",
        "answer_sql": "DELETE FROM orders\nWHERE id = 10;",
        "choices": [
            "DELETE FROM orders\nWHERE id = 10;",
            "DELETE orders\nWHERE id = 10;",
            "DELETE * FROM orders\nWHERE id = 10;",
            "DELETE FROM orders;",
        ],
        "answer_index": 0,
        "explanation": (
            "データを削除するときは `DELETE FROM` を使います。\n\n"
            "・`DELETE FROM orders` … どの表から消すか。\n"
            "・`WHERE id = 10` … どの行を消すか。\n\n"
            "SELECT と違い、消す列を選ぶ `*` は書きません（行ごとまるごと消えます）。"
        ),
        "points": (
            "・`DELETE` のあとには `FROM` が必要です。\n"
            "・`WHERE` を付け忘れると、表の『全部の行』が消えてしまいます。いちばん危険な書き間違いです。"
        ),
    },
    {
        "id": 39,
        "hint": (
            "- まとめて追加するときは `VALUES (...), (...)` とカンマで並べる\n"
            "- 1件のときと同じ `INSERT INTO` を使う"
        ),
        "topic": "データ操作（INSERT/UPDATE/DELETE）",
        "level": 7,
        "question": "products（商品）テーブルに2件追加してください。(id=7, name='付箋', category='文具', price=200) と (id=8, name='ホチキス', category='文具', price=500)。",
        "answer_sql": (
            "INSERT INTO products (id, name, category, price)\n"
            "VALUES (7, '付箋', '文具', 200),\n"
            "       (8, 'ホチキス', '文具', 500);"
        ),
        "choices": [
            "INSERT INTO products (id, name, category, price)\nVALUES (7, '付箋', '文具', 200),\n       (8, 'ホチキス', '文具', 500);",
            "INSERT INTO products (id, name, category, price)\nVALUES (7, '付箋', '文具', 200)\n       (8, 'ホチキス', '文具', 500);",
            "INSERT INTO products (id, name, category, price)\nVALUES (7, '付箋', '文具', 200) AND (8, 'ホチキス', '文具', 500);",
            "INSERT INTO products (id, name, category, price)\nVALUES (7, '付箋', '文具', 200);\nVALUES (8, 'ホチキス', '文具', 500);",
        ],
        "answer_index": 0,
        "explanation": (
            "複数の行をまとめて追加するときは、`VALUES` のあとに「(値の組)」をカンマ `,` で並べます。\n\n"
            "・`VALUES (7, ...), (8, ...)` … 2件分の値をカンマで区切って書きます。\n\n"
            "1件ずつ INSERT を2回書いてもよいですが、まとめると1文で追加できます。"
        ),
        "points": (
            "・行と行の区切りはカンマ `,`。`AND` や、途中のセミコロン `;` ではありません。\n"
            "・`;` は文の終わりに1回だけ付けます。"
        ),
    },
    {
        "id": 40,
        "hint": (
            "- 今の値をもとに計算するときは `SET 列 = 列 + 値`\n"
            "- `SET 列 = 値` だと、その値で上書きしてしまう"
        ),
        "topic": "データ操作（INSERT/UPDATE/DELETE）",
        "level": 7,
        "question": "employees（社員）テーブルの、開発部（department_id が 2）の社員全員の月給（salary）を 1万円（10000）上げてください。",
        "answer_sql": (
            "UPDATE employees\n"
            "SET salary = salary + 10000\n"
            "WHERE department_id = 2;"
        ),
        "choices": [
            "UPDATE employees\nSET salary = salary + 10000\nWHERE department_id = 2;",
            "UPDATE employees\nSET salary = 10000\nWHERE department_id = 2;",
            "UPDATE employees\nSET salary = salary + 10000;",
            "UPDATE employees\nSET salary + 10000\nWHERE department_id = 2;",
        ],
        "answer_index": 0,
        "explanation": (
            "『今の値に足す』ときは、`SET salary = salary + 10000` と書きます。"
            "右側の `salary` は『今の月給』を表し、それに 10000 を足した値で更新します。\n\n"
            "・`WHERE department_id = 2` … 開発部の社員だけが対象になります。"
        ),
        "points": (
            "・`SET salary = 10000` と書くと、足し算ではなく『10000円に上書き』になってしまいます。\n"
            "・`WHERE` を付けないと、全社員の月給が上がってしまいます。"
        ),
    },

    # =====================================================================
    # 追加: Lv6（集計：SUM・MAX）
    # =====================================================================
    {
        "id": 41,
        "hint": (
            "- 合計は `SUM(列)` で求める\n"
            "- 件数を数える `COUNT` とは役割が違う"
        ),
        "topic": "集計関数と GROUP BY",
        "level": 9,
        "question": "orders（注文）テーブルの数量（quantity）の合計を求めてください。",
        "answer_sql": "SELECT SUM(quantity)\nFROM orders;",
        "choices": [
            "SELECT SUM(quantity)\nFROM orders;",
            "SELECT COUNT(quantity)\nFROM orders;",
            "SELECT TOTAL(quantity)\nFROM orders;",
            "SELECT SUM(*)\nFROM orders;",
        ],
        "answer_index": 0,
        "explanation": (
            "数値の合計を出すときは `SUM(列)` を使います。\n\n"
            "・`SUM(quantity)` … すべての注文の数量を足し合わせます。\n\n"
            "`COUNT` は『件数（何行あるか）』を数える関数なので、合計とは別物です。"
        ),
        "points": (
            "・合計は `SUM`、件数は `COUNT`。目的で使い分けます。\n"
            "・MySQL に `TOTAL` という関数はありません。合計は `SUM` です。"
        ),
    },
    {
        "id": 42,
        "hint": (
            "- 最大値は `MAX(列)`、最小値は `MIN(列)`\n"
            "- どちらも数値や日付の列に使える"
        ),
        "topic": "集計関数と GROUP BY",
        "level": 9,
        "question": "products（商品）テーブルの単価（price）の最大値を求めてください。",
        "answer_sql": "SELECT MAX(price)\nFROM products;",
        "choices": [
            "SELECT MAX(price)\nFROM products;",
            "SELECT MIN(price)\nFROM products;",
            "SELECT MAX(*)\nFROM products;",
            "SELECT LARGEST(price)\nFROM products;",
        ],
        "answer_index": 0,
        "explanation": (
            "いちばん大きい値（最大値）を求めるときは `MAX(列)` を使います。\n\n"
            "・`MAX(price)` … 単価の中でいちばん高い金額を返します。\n\n"
            "反対に、いちばん小さい値（最小値）は `MIN(列)` です。"
        ),
        "points": (
            "・最大は `MAX`、最小は `MIN`。\n"
            "・MySQL に `LARGEST` という関数はありません。最大値は `MAX` です。"
        ),
    },

    # =====================================================================
    # 追加: Lv2（列の別名 AS・計算した列）
    # =====================================================================
    {
        "id": 43,
        "hint": (
            "- `列 AS 別名` … 列に表示用の名前（見出し）を付けられる\n"
            "- 元の列名はそのまま、表示だけ変わる"
        ),
        "topic": "SELECT と WHERE",
        "level": 3,
        "question": "employees（社員）テーブルの名前（name）と月給（salary）を、salary の見出しを「月給」にして表示してください。",
        "answer_sql": "SELECT name, salary AS 月給\nFROM employees;",
        "choices": [
            "SELECT name, salary AS 月給\nFROM employees;",
            "SELECT name, 月給 AS salary\nFROM employees;",
            "SELECT name, salary = 月給\nFROM employees;",
            "SELECT name, salary TO 月給\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "列に表示用の名前（別名）を付けたいときは `列 AS 別名` と書きます。\n\n"
            "・`salary AS 月給` … 中身は salary のまま、見出しだけ『月給』になります。\n\n"
            "結果が読みやすくなり、計算した列に名前を付けるときにも役立ちます。"
        ),
        "points": (
            "・`AS` の『前』が元の列、『後ろ』が新しい見出しです。順番を逆にしないこと。\n"
            "・`AS` は省略もできます（`salary 月給`）が、付けたほうが分かりやすいです。"
        ),
    },
    {
        "id": 44,
        "hint": (
            "- `SELECT` の中で計算ができる（`+ - * /`）\n"
            "- 掛け算は `*`。計算した列には `AS` で名前を付けると分かりやすい"
        ),
        "topic": "SELECT と WHERE",
        "level": 3,
        "question": "employees（社員）テーブルの名前（name）と、年収（月給 × 12）を「年収」という見出しで表示してください。",
        "answer_sql": "SELECT name, salary * 12 AS 年収\nFROM employees;",
        "choices": [
            "SELECT name, salary * 12 AS 年収\nFROM employees;",
            "SELECT name, salary x 12 AS 年収\nFROM employees;",
            "SELECT name, SUM(salary * 12) AS 年収\nFROM employees;",
            "SELECT name, salary * 12\nFROM employees AS 年収;",
        ],
        "answer_index": 0,
        "explanation": (
            "`SELECT` の中では計算ができます。\n\n"
            "・`salary * 12` … 月給を12倍して年収を計算します。\n"
            "・`AS 年収` … 計算した列に見出しを付けます。\n\n"
            "四則演算は `+`（足す）`-`（引く）`*`（掛ける）`/`（割る）を使います。"
        ),
        "points": (
            "・掛け算の記号は `*` です（`x` ではありません）。\n"
            "・`SUM(...)` を付けると全員分を1つに合計してしまいます。1人ずつ計算したいときは付けません。"
        ),
    },

    # =====================================================================
    # 追加: Lv3（NULL でない＝IS NOT NULL）
    # =====================================================================
    {
        "id": 45,
        "hint": (
            "- 空っぽ（NULL）かどうかは `IS NULL` / `IS NOT NULL` で調べる\n"
            "- NULL には `=` や `!=` は使えない"
        ),
        "topic": "SELECT と WHERE",
        "level": 4,
        "question": "employees（社員）テーブルの、上司がいる（manager_id が NULL でない）社員の名前（name）を表示してください。",
        "answer_sql": "SELECT name\nFROM employees\nWHERE manager_id IS NOT NULL;",
        "choices": [
            "SELECT name\nFROM employees\nWHERE manager_id IS NOT NULL;",
            "SELECT name\nFROM employees\nWHERE manager_id != NULL;",
            "SELECT name\nFROM employees\nWHERE manager_id NOT NULL;",
            "SELECT name\nFROM employees\nWHERE manager_id <> '';",
        ],
        "answer_index": 0,
        "explanation": (
            "値が空っぽ（NULL）でないことを調べるときは `IS NOT NULL` を使います。\n\n"
            "・`WHERE manager_id IS NOT NULL` … 上司の社員idが入っている（＝上司がいる）人だけ残します。\n\n"
            "反対に『NULL である』を調べるときは `IS NULL` です。"
        ),
        "points": (
            "・『NULL でない』は `IS NOT NULL`。`!= NULL` や `= NULL` は正しく動きません。\n"
            "・NULL（値がない状態）と、空文字 `''`（長さ0の文字）は別物です。"
        ),
    },

    # =====================================================================
    # 追加: Lv4（IN：複数の値のどれか）
    # =====================================================================
    {
        "id": 46,
        "hint": (
            "- `列 IN (値1, 値2, ...)` … リストの値の『どれかと一致』する行を残す\n"
            "- `= 値1 OR = 値2 OR ...` を短く書ける"
        ),
        "topic": "SELECT と WHERE",
        "level": 5,
        "question": "employees（社員）テーブルの、営業部（department_id が 1）または人事部（department_id が 3）の社員の名前（name）と部署ID（department_id）を表示してください。",
        "answer_sql": (
            "SELECT name, department_id\n"
            "FROM employees\n"
            "WHERE department_id IN (1, 3);"
        ),
        "choices": [
            "SELECT name, department_id\nFROM employees\nWHERE department_id IN (1, 3);",
            "SELECT name, department_id\nFROM employees\nWHERE department_id = 1 OR 3;",
            "SELECT name, department_id\nFROM employees\nWHERE department_id IN (1 OR 3);",
            "SELECT name, department_id\nFROM employees\nWHERE department_id = (1, 3);",
        ],
        "answer_index": 0,
        "explanation": (
            "いくつかの値の『どれかに一致』を調べるときは `IN` が便利です。\n\n"
            "・`department_id IN (1, 3)` … 部署IDが 1 または 3 の社員を残します。\n\n"
            "これは `department_id = 1 OR department_id = 3` と同じ意味で、短く書けます。"
        ),
        "points": (
            "・`IN` のカッコの中はカンマ `,` で区切ります。\n"
            "・`= 1 OR 3` のような書き方はできません。`=` は1つの値としか比べられないからです。"
        ),
    },

    # =====================================================================
    # 追加: Lv7（並び替え：昇順 ASC）
    # =====================================================================
    {
        "id": 47,
        "hint": (
            "- 並び替えは `ORDER BY 列`。`ASC` は昇順（小さい順）\n"
            "- 大きい順にしたいときは `DESC`"
        ),
        "topic": "並び替え・重複除去",
        "level": 8,
        "question": "products（商品）テーブルを単価（price）の安い順に並べ、名前（name）と単価（price）を表示してください。",
        "answer_sql": "SELECT name, price\nFROM products\nORDER BY price ASC;",
        "choices": [
            "SELECT name, price\nFROM products\nORDER BY price ASC;",
            "SELECT name, price\nFROM products\nORDER BY price DESC;",
            "SELECT name, price\nFROM products\nSORT BY price ASC;",
            "SELECT name, price\nFROM products\nORDER price ASC;",
        ],
        "answer_index": 0,
        "explanation": (
            "並び替えは `ORDER BY` を使います。\n\n"
            "・`ORDER BY price ASC` … 単価の小さい順（安い順）に並べます。\n\n"
            "`ASC` は昇順（小→大）。反対に大きい順にしたいときは `DESC`（降順）を使います。"
        ),
        "points": (
            "・昇順（小→大）は `ASC`、降順（大→小）は `DESC`。何も書かないと昇順になります。\n"
            "・並び替えは `ORDER BY`。`SORT BY` ではありません。`BY` の書き忘れにも注意。"
        ),
    },

    # =====================================================================
    # Lv1: SQL はじめの一歩（いちばんやさしい入門）
    # =====================================================================
    {
        "id": 48,
        "hint": (
            "- `SELECT` … データを「取り出す」ことば\n"
            "- `*` は「すべての列」、`FROM 表名` で表を指定する"
        ),
        "topic": "SQL はじめの一歩",
        "level": 1,
        "question": "employees（社員）テーブルの中身を、まるごと全部表示する SQL はどれでしょう？",
        "answer_sql": "SELECT * FROM employees;",
        "choices": [
            "SELECT * FROM employees;",
            "GET * FROM employees;",
            "SHOW employees;",
            "SELECT employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "データを取り出すときは、必ず `SELECT` で始めます。\n\n"
            "・`SELECT *` … `*` は「すべての列」という意味です。\n"
            "・`FROM employees` … どの表から取り出すかを指定します。\n\n"
            "この2つを合わせて『社員の表から、全部の列を取り出す』になります。"
        ),
        "points": (
            "・取り出しは `SELECT` です。`GET` や `SHOW` では取り出せません。\n"
            "・表を指定する `FROM` を書き忘れると動きません。"
        ),
    },
    {
        "id": 49,
        "hint": (
            "- 取り出したい列の名前を `SELECT` の後ろに書く\n"
            "- `FROM` の後ろには「表の名前」を書く"
        ),
        "topic": "SQL はじめの一歩",
        "level": 1,
        "question": "employees（社員）テーブルの名前（name）の列だけを表示する SQL はどれでしょう？",
        "answer_sql": "SELECT name FROM employees;",
        "choices": [
            "SELECT name FROM employees;",
            "SELECT name;",
            "SELECT employees FROM name;",
            "GET name FROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "`*`（すべての列）の代わりに列の名前を書くと、その列だけを取り出せます。\n\n"
            "・`SELECT name` … 名前の列だけ\n"
            "・`FROM employees` … 社員の表から\n\n"
            "『どの列を／どの表から』の順で書くのが基本の形です。"
        ),
        "points": (
            "・`SELECT` の後ろは『列の名前』、`FROM` の後ろは『表の名前』。場所を入れかえないように。\n"
            "・`FROM` を省くと、どの表か分からずエラーになります。"
        ),
    },
    {
        "id": 50,
        "hint": (
            "- `FROM` の後ろに「使いたい表の名前」を書く\n"
            "- すべての列は `*`"
        ),
        "topic": "SQL はじめの一歩",
        "level": 1,
        "question": "departments（部署）テーブルの中身を全部表示する SQL はどれでしょう？",
        "answer_sql": "SELECT * FROM departments;",
        "choices": [
            "SELECT * FROM departments;",
            "SELECT * FROM employees;",
            "SELECT * departments;",
            "SELECT departments;",
        ],
        "answer_index": 0,
        "explanation": (
            "取り出す表は `FROM` の後ろで指定します。今回は部署の表なので `FROM departments` です。\n\n"
            "・`SELECT *` … すべての列\n"
            "・`FROM departments` … 部署の表から\n\n"
            "表の名前をまちがえると、ちがうデータが出てきてしまいます。"
        ),
        "points": (
            "・`FROM` の後ろの表の名前で『どの表を見るか』が決まります。\n"
            "・`FROM` という言葉自体を省くと動きません（`SELECT * departments;` は誤り）。"
        ),
    },
    {
        "id": 51,
        "hint": (
            "- 「すべての列」は記号 `*`（アスタリスク）で表す\n"
            "- `SELECT` のすぐ後ろに `*` を書く"
        ),
        "topic": "SQL はじめの一歩",
        "level": 1,
        "question": "products（商品）テーブルの、すべての列・すべての行を表示する SQL はどれでしょう？",
        "answer_sql": "SELECT * FROM products;",
        "choices": [
            "SELECT * FROM products;",
            "SELECT all FROM products;",
            "SELECT # FROM products;",
            "SELECT FROM products;",
        ],
        "answer_index": 0,
        "explanation": (
            "「すべての列」を表す記号は `*`（アスタリスク）です。\n\n"
            "・`SELECT *` … すべての列を取り出す\n"
            "・`FROM products` … 商品の表から\n\n"
            "`all` や `#` ではなく、`*` を使うのがルールです。"
        ),
        "points": (
            "・「全部の列」は `*` の1文字で表します。\n"
            "・`SELECT` の後ろに何も書かない（`SELECT FROM ...`）のは誤り。必ず列か `*` を書きます。"
        ),
    },
]
