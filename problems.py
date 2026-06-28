"""SQL 問題集のデータ（MySQL 構文）。

1 問は辞書（dict）で表します。キーの意味:
  id          … 通し番号
  topic       … 項目（トピック）。学習の区分け
  level       … 難易度 1〜3（1=初級, 2=中級, 3=上級）
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
    "基本文法",
    "並び替え・重複除去",
    "集計関数と GROUP BY",
    "テーブル結合（JOIN）",
    "サブクエリ",
    "文字列・日付の関数",
    "CASE 式と条件分岐",
    "ウィンドウ関数",
]

# レベル（攻略の段階）。やさしい順に Lv1〜Lv5。
# 各問題の "level" がこの番号に対応します。アプリは Lv1 から順に攻略します。
LEVELS = [
    {"level": 1, "title": "はじめの一歩", "desc": "SELECT と WHERE の基本（まずはここから）"},
    {"level": 2, "title": "並び替え・絞り込み", "desc": "ORDER BY・DISTINCT・LIMIT・複数条件"},
    {"level": 3, "title": "集計（GROUP BY）", "desc": "COUNT/AVG・GROUP BY・HAVING・CASE 入門"},
    {"level": 4, "title": "結合と条件分岐", "desc": "JOIN・複数テーブル・CASE の応用"},
    {"level": 5, "title": "サブクエリとウィンドウ関数", "desc": "上級。サブクエリ・RANK などの総仕上げ"},
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
        "level": 1,
        "question": "社員（employees）の中から、月給（salary）が 30万円以上の人の "
                    "名前（name）と月給（salary）を取り出してください。",
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
        "level": 2,
        "question": "営業部（department_id が 1）に所属し、かつ月給が 30万円以上の社員の "
                    "名前と月給を取り出してください。",
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
        "level": 1,
        "question": "上司がいない社員（manager_id が空っぽ＝NULL の人）の名前を取り出してください。",
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
        "level": 2,
        "question": "社員を月給の高い順に並べて、名前と月給を表示してください。",
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
        "level": 2,
        "question": "商品（products）にどんなカテゴリ（category）があるか、"
                    "重複をなくして一覧で取り出してください。",
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
        "level": 2,
        "question": "月給が高い人トップ3の、名前と月給を表示してください。",
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
        "level": 3,
        "question": "社員が全部で何人いるか、人数を数えてください。",
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
        "level": 3,
        "question": "部署（department_id）ごとに、平均の月給を求めてください。",
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
        "level": 3,
        "question": "社員が 2人以上いる部署について、部署IDとその人数を表示してください。",
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
        "id": 10,
        "hint": (
            "- `JOIN` … 2つの表をつなげる\n"
            "- `ON A = B` でどの列どうしを一致させるか指定"
        ),
        "topic": "テーブル結合（JOIN）",
        "level": 4,
        "question": "社員の名前と、その人が所属する部署の名前を、いっしょに表示してください。",
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
        "level": 4,
        "question": "すべての部署について、部署名とその部署の社員数を表示してください。"
                    "社員が1人もいない部署も、0人として表示してください。",
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
        "level": 4,
        "question": "注文（orders）について、『担当した社員の名前』『商品名』『数量』を"
                    "一覧で表示してください。",
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
        "id": 13,
        "hint": (
            "- `( SELECT ... )` … カッコの中を先に計算（サブクエリ）\n"
            "- 1つの値を返すサブクエリは `>` などで比較できる"
        ),
        "topic": "サブクエリ",
        "level": 5,
        "question": "全社員の平均月給よりも高い月給をもらっている社員の、名前と月給を表示してください。",
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
        "level": 5,
        "question": "一度も注文（orders）を担当していない社員の名前を表示してください。",
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
        "level": 5,
        "question": "各部署で最も月給が高い社員について、部署ID・名前・月給を表示してください。",
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
        "level": 2,
        "question": "名前に『藤』という文字が含まれる社員を、すべて表示してください。",
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
        "level": 3,
        "question": "2020年以降に入社した（hire_date が 2020年1月1日以降の）社員の、"
                    "名前と入社日を表示してください。",
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
        "level": 4,
        "question": "社員一覧を『佐藤（営業）』のように『名前（部署名）』の形にまとめた1つの列で"
                    "表示してください。",
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
        "level": 3,
        "question": "社員の名前と月給に加えて、月給が40万円以上なら『高い』、"
                    "そうでなければ『普通』と表示する列を作ってください。",
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
        "level": 4,
        "question": "社員の名前と月給に加えて、月給を『40万以上=A』『30万以上=B』"
                    "『それ未満=C』の3段階で表示する列を作ってください。",
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
        "level": 5,
        "question": "部署ごとに、『月給が40万円以上の社員が何人いるか』を数えて、"
                    "部署IDと人数を表示してください。",
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
        "level": 5,
        "question": "全社員に、月給の高い順の順位（1位・2位…）を付けて、"
                    "名前・月給・順位を表示してください。",
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
        "level": 5,
        "question": "部署ごとに、月給の高い順の順位を付けてください。"
                    "部署ID・名前・月給・部署内順位を表示してください。",
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
        "level": 5,
        "question": "各部署で月給が最も高い社員（部署内1位）だけを取り出して、"
                    "部署ID・名前・月給を表示してください。",
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
        "level": 1,
        "question": "社員（employees）の名前（name）を、全員分すべて表示してください。",
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
        "level": 1,
        "question": "商品（products）の表について、すべての列・すべての行を表示してください。",
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
        "level": 1,
        "question": "営業部（department_id が 1）に所属する社員の名前（name）を表示してください。",
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
    # 追加: Lv2 用の「基本文法」（AS 別名・BETWEEN・IN）
    # =====================================================================
    {
        "id": 28,
        "hint": (
            "- `列 AS 別名` … 列に表示用の名前（見出し）をつける\n"
            "- 見た目が変わるだけで、データそのものは変わらない"
        ),
        "topic": "基本文法",
        "level": 2,
        "question": "社員の名前と月給を表示してください。"
                    "ただし、月給（salary）の列の見出しを『給料』にしてください。",
        "answer_sql": "SELECT name, salary AS 給料\nFROM employees;",
        "choices": [
            "SELECT name, salary AS 給料\nFROM employees;",
            "SELECT name, 給料 AS salary\nFROM employees;",
            "SELECT name, salary = 給料\nFROM employees;",
            "SELECT name, salary TO 給料\nFROM employees;",
        ],
        "answer_index": 0,
        "explanation": (
            "列に別の見出し（別名）を付けるには `AS` を使います。\n\n"
            "・`salary AS 給料` … salary 列を『給料』という見出しで表示します。\n"
            "・順番は『元の列 AS 新しい見出し』です。逆にしてはいけません。\n\n"
            "見出しが変わるだけで、中身のデータは変わりません。"
        ),
        "points": (
            "・`AS` の後ろが新しい見出しです。『元の列 AS 別名』の順番に注意。\n"
            "・MySQL では `AS` を省いて `salary 給料` とも書けますが、付けた方が読みやすいです。"
        ),
    },
    {
        "id": 29,
        "hint": (
            "- `列 BETWEEN A AND B` … A以上B以下（両端を含む）\n"
            "- 小さい方 AND 大きい方 の順で書く"
        ),
        "topic": "基本文法",
        "level": 2,
        "question": "月給が 30万円以上 40万円以下 の社員の、名前と月給を表示してください。",
        "answer_sql": (
            "SELECT name, salary\n"
            "FROM employees\n"
            "WHERE salary BETWEEN 300000 AND 400000;"
        ),
        "choices": [
            "SELECT name, salary\nFROM employees\nWHERE salary BETWEEN 300000 AND 400000;",
            "SELECT name, salary\nFROM employees\nWHERE salary BETWEEN 400000 AND 300000;",
            "SELECT name, salary\nFROM employees\nWHERE salary IN 300000 AND 400000;",
            "SELECT name, salary\nFROM employees\nWHERE salary >= 300000 OR salary <= 400000;",
        ],
        "answer_index": 0,
        "explanation": (
            "『◯◯以上△△以下』のような範囲は `BETWEEN A AND B` で書けます。\n\n"
            "・`salary BETWEEN 300000 AND 400000` … 30万以上40万以下（両端を含む）。\n"
            "・これは `salary >= 300000 AND salary <= 400000` と同じ意味です。\n\n"
            "書く順番は『小さい方 AND 大きい方』です。"
        ),
        "points": (
            "・`BETWEEN` は両端（30万と40万ちょうど）も含みます。\n"
            "・小さい方→大きい方の順で書くこと。逆にすると1件も取れません。"
        ),
    },
    {
        "id": 30,
        "hint": (
            "- `列 IN (値1, 値2, ...)` … どれかに一致\n"
            "- `OR` をいくつも書く代わりに短く書ける"
        ),
        "topic": "基本文法",
        "level": 2,
        "question": "部署ID（department_id）が 1 または 3 の社員の、名前と部署IDを表示してください。",
        "answer_sql": (
            "SELECT name, department_id\n"
            "FROM employees\n"
            "WHERE department_id IN (1, 3);"
        ),
        "choices": [
            "SELECT name, department_id\nFROM employees\nWHERE department_id IN (1, 3);",
            "SELECT name, department_id\nFROM employees\nWHERE department_id = 1 OR 3;",
            "SELECT name, department_id\nFROM employees\nWHERE department_id IN (1 AND 3);",
            "SELECT name, department_id\nFROM employees\nWHERE department_id = (1, 3);",
        ],
        "answer_index": 0,
        "explanation": (
            "『どれかに一致』を調べるときは `IN (値の一覧)` が便利です。\n\n"
            "・`department_id IN (1, 3)` … 部署IDが 1 か 3 の人を残します。\n"
            "・これは `department_id = 1 OR department_id = 3` と同じ意味で、短く書けます。"
        ),
        "points": (
            "・`= 1 OR 3` は誤りです（『3』が常に真のように扱われ、正しく絞れません）。\n"
            "・候補は `IN (1, 3)` のようにカンマで並べます。"
        ),
    },
]
