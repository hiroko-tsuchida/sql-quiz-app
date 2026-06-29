"""テーブル定義とサンプルデータ。

「こういうテーブルとデータがある」という前提を学習者に見せるために使います。
さらに、このサンプルデータは runner.py でインメモリ SQLite に読み込まれ、
正解 SQL を実際に実行して『実行結果』を表示するのにも使われます。
SQL の方言（書き方のルール）は MySQL を想定しています。
"""

import pandas as pd

# --- テーブルの作成文（MySQL の CREATE TABLE 文）-------------------------------
# 学習者がカラム名や型を確認できるように、画面にそのまま表示します。
CREATE_STATEMENTS = """\
-- 部署
CREATE TABLE departments (
    id   INT PRIMARY KEY,
    name VARCHAR(50)        -- 部署名
);

-- 社員
CREATE TABLE employees (
    id            INT PRIMARY KEY,
    name          VARCHAR(50),   -- 氏名
    department_id INT,           -- 所属部署（departments.id を参照）
    salary        INT,           -- 月給（円）
    hire_date     DATE,          -- 入社日
    manager_id    INT            -- 上司の社員id（いない場合は NULL）
);

-- 商品
CREATE TABLE products (
    id       INT PRIMARY KEY,
    name     VARCHAR(50),   -- 商品名
    category VARCHAR(50),   -- カテゴリ
    price    INT            -- 単価（円）
);

-- 注文（どの社員がどの商品を何個売ったか）
CREATE TABLE orders (
    id          INT PRIMARY KEY,
    employee_id INT,        -- 担当社員（employees.id を参照）
    product_id  INT,        -- 商品（products.id を参照）
    quantity    INT,        -- 数量
    order_date  DATE        -- 注文日
);
"""

# --- サンプルデータ -----------------------------------------------------------
# pandas の DataFrame で持ち、画面に表として表示します。

departments = pd.DataFrame(
    [
        {"id": 1, "name": "営業"},
        {"id": 2, "name": "開発"},
        {"id": 3, "name": "人事"},
        {"id": 4, "name": "マーケティング"},
    ]
)

employees = pd.DataFrame(
    [
        # id, name, department_id, salary, hire_date, manager_id
        {
            "id": 1,
            "name": "佐藤",
            "department_id": 1,
            "salary": 450000,
            "hire_date": "2015-04-01",
            "manager_id": None,
        },
        {
            "id": 2,
            "name": "鈴木",
            "department_id": 1,
            "salary": 320000,
            "hire_date": "2019-04-01",
            "manager_id": 1,
        },
        {
            "id": 3,
            "name": "高橋",
            "department_id": 1,
            "salary": 280000,
            "hire_date": "2022-10-01",
            "manager_id": 1,
        },
        {
            "id": 4,
            "name": "田中",
            "department_id": 2,
            "salary": 500000,
            "hire_date": "2014-07-01",
            "manager_id": None,
        },
        {
            "id": 5,
            "name": "伊藤",
            "department_id": 2,
            "salary": 380000,
            "hire_date": "2020-04-01",
            "manager_id": 4,
        },
        {
            "id": 6,
            "name": "渡辺",
            "department_id": 2,
            "salary": 350000,
            "hire_date": "2021-04-01",
            "manager_id": 4,
        },
        {
            "id": 7,
            "name": "山本",
            "department_id": 3,
            "salary": 300000,
            "hire_date": "2018-04-01",
            "manager_id": None,
        },
        {
            "id": 8,
            "name": "中村",
            "department_id": 3,
            "salary": 260000,
            "hire_date": "2023-04-01",
            "manager_id": 7,
        },
        # department_id = 4（マーケティング）には、まだ社員がいない
        {
            "id": 9,
            "name": "小林",
            "department_id": None,
            "salary": 240000,
            "hire_date": "2023-09-01",
            "manager_id": None,
        },
    ]
)

products = pd.DataFrame(
    [
        {"id": 1, "name": "ノートPC", "category": "電子機器", "price": 120000},
        {"id": 2, "name": "マウス", "category": "電子機器", "price": 2500},
        {"id": 3, "name": "デスク", "category": "家具", "price": 30000},
        {"id": 4, "name": "チェア", "category": "家具", "price": 18000},
        {"id": 5, "name": "ノート", "category": "文具", "price": 300},
        {"id": 6, "name": "ボールペン", "category": "文具", "price": 150},
    ]
)

orders = pd.DataFrame(
    [
        # id, employee_id, product_id, quantity, order_date
        {
            "id": 1,
            "employee_id": 2,
            "product_id": 1,
            "quantity": 2,
            "order_date": "2024-01-15",
        },
        {
            "id": 2,
            "employee_id": 2,
            "product_id": 2,
            "quantity": 10,
            "order_date": "2024-01-20",
        },
        {
            "id": 3,
            "employee_id": 3,
            "product_id": 5,
            "quantity": 50,
            "order_date": "2024-02-05",
        },
        {
            "id": 4,
            "employee_id": 3,
            "product_id": 6,
            "quantity": 30,
            "order_date": "2024-02-05",
        },
        {
            "id": 5,
            "employee_id": 5,
            "product_id": 1,
            "quantity": 1,
            "order_date": "2024-02-10",
        },
        {
            "id": 6,
            "employee_id": 5,
            "product_id": 3,
            "quantity": 3,
            "order_date": "2024-03-01",
        },
        {
            "id": 7,
            "employee_id": 6,
            "product_id": 4,
            "quantity": 5,
            "order_date": "2024-03-12",
        },
        {
            "id": 8,
            "employee_id": 2,
            "product_id": 1,
            "quantity": 1,
            "order_date": "2024-03-20",
        },
        {
            "id": 9,
            "employee_id": 8,
            "product_id": 5,
            "quantity": 20,
            "order_date": "2024-04-02",
        },
        {
            "id": 10,
            "employee_id": 5,
            "product_id": 2,
            "quantity": 4,
            "order_date": "2024-04-18",
        },
    ]
)

# 画面で「テーブル一覧」として回すための辞書
TABLES = {
    "departments（部署）": departments,
    "employees（社員）": employees,
    "products（商品）": products,
    "orders（注文）": orders,
}
