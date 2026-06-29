"""正解 SQL を実際に実行して、結果の表を作るモジュール。

schema.py のサンプルデータを「インメモリの SQLite」に読み込み、その上で
SQL を実行します。SQLite は MySQL とほぼ同じ SQL が動き、ウィンドウ関数
（RANK など）や CONCAT にも対応しているため、本アプリの問題はそのまま実行
できます。データはメモリ上だけに作るので、ファイルやネットワークは不要です。

注意: INSERT / UPDATE / DELETE もここで実行できますが、毎回まっさらな
サンプルデータから作り直すため、本物のデータが書き換わることはありません。
"""

import math
import re
import sqlite3

import numpy as np
import pandas as pd

import schema

# SQLite 用のテーブル定義。型を明示して、id などが「1.0」のような小数で
# 表示されないようにする（INTEGER と指定しておく）。
_CREATE = {
    "departments": "CREATE TABLE departments (id INTEGER, name TEXT)",
    "employees": (
        "CREATE TABLE employees ("
        "id INTEGER, name TEXT, department_id INTEGER, "
        "salary INTEGER, hire_date TEXT, manager_id INTEGER)"
    ),
    "products": (
        "CREATE TABLE products (id INTEGER, name TEXT, category TEXT, price INTEGER)"
    ),
    "orders": (
        "CREATE TABLE orders ("
        "id INTEGER, employee_id INTEGER, product_id INTEGER, "
        "quantity INTEGER, order_date TEXT)"
    ),
}

# テーブル名 → 元データ（schema.py の DataFrame）
_FRAMES = {
    "departments": schema.departments,
    "employees": schema.employees,
    "products": schema.products,
    "orders": schema.orders,
}

# INSERT/UPDATE/DELETE から「対象のテーブル名」を取り出すための正規表現
_TARGET_TABLE_RE = re.compile(
    r"\b(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM)\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.IGNORECASE,
)


def _clean(value):
    """DataFrame の1セルを、sqlite3 が受け取れる素の Python の値に直す。

    pandas は欠損を NaN（小数）で持つので、それは NULL（None）に変換する。
    numpy の整数はそのままだと sqlite3 が受け取れないので int に直す。
    """
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def build_connection() -> sqlite3.Connection:
    """サンプルデータを読み込んだ、新しいインメモリ SQLite 接続を作って返す。"""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    for name, ddl in _CREATE.items():
        cur.execute(ddl)
        df = _FRAMES[name]
        cols = list(df.columns)
        placeholders = ", ".join("?" * len(cols))
        rows = [[_clean(v) for v in row] for row in df.itertuples(index=False)]
        cur.executemany(
            f"INSERT INTO {name} ({', '.join(cols)}) VALUES ({placeholders})", rows
        )
    conn.commit()
    return conn


def _prettify(df: pd.DataFrame) -> pd.DataFrame:
    """表示用に整える。中身が全部整数の小数列（1.0 など）は整数に直す。"""
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_float_dtype(s):
            non_null = s.dropna()
            if not non_null.empty and (non_null % 1 == 0).all():
                df[col] = s.astype("Int64")
    return df


def run_sql(sql: str) -> dict:
    """SQL を実行して結果を返す。

    戻り値（dict）:
      SELECT のとき … {"kind": "select", "df": 結果の DataFrame}
      INSERT/UPDATE/DELETE のとき …
        {"kind": "dml", "table": 対象テーブル名, "rowcount": 変更行数,
         "df": 実行後のそのテーブルの中身}
    """
    conn = build_connection()
    try:
        first_word = sql.lstrip().split(None, 1)[0].upper()
        if first_word == "SELECT":
            df = pd.read_sql_query(sql, conn)
            return {"kind": "select", "df": _prettify(df)}

        cur = conn.execute(sql)
        conn.commit()
        match = _TARGET_TABLE_RE.search(sql)
        table = match.group(1) if match else None
        after = pd.read_sql_query(f"SELECT * FROM {table}", conn) if table else None
        return {
            "kind": "dml",
            "table": table,
            "rowcount": cur.rowcount,
            "df": _prettify(after) if after is not None else None,
        }
    finally:
        conn.close()
