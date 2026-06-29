"""SQL 実行（runner.py）のテスト。

サンプルデータをインメモリ SQLite に読み込み、SQL を実行して結果を返す
部分を検証する。全47問の正解 SQL がエラーなく実行できることも確かめる。
"""

import pytest

from problems import PROBLEMS
from runner import run_sql


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_every_answer_sql_runs(problem):
    """全問の正解 SQL がエラーなく実行できる。"""
    result = run_sql(problem["answer_sql"])
    assert result["kind"] in ("select", "dml")


def test_select_returns_rows():
    """単純な SELECT が、サンプルデータの件数どおりの表を返す。"""
    result = run_sql("SELECT * FROM departments;")
    assert result["kind"] == "select"
    assert len(result["df"]) == 4  # 部署は4件


def test_ids_are_integers_not_floats():
    """欠損のある列があっても、id は 1.0 ではなく整数として表示される。"""
    result = run_sql("SELECT id, department_id FROM employees;")
    df = result["df"]
    # 1.0 のような小数表記にならないこと（Int64 か通常の整数）
    assert "Int" in str(df["id"].dtype) or "int" in str(df["id"].dtype)


def test_window_function_rank():
    """ウィンドウ関数 RANK が動き、最高給に1位が付く。"""
    result = run_sql(
        "SELECT name, salary, RANK() OVER (ORDER BY salary DESC) AS r FROM employees;"
    )
    df = result["df"]
    assert int(df.iloc[0]["r"]) == 1
    assert df.iloc[0]["salary"] == df["salary"].max()


def test_update_is_isolated_per_call():
    """UPDATE しても、次の実行ではサンプルデータが元に戻っている
    （毎回まっさらな DB を作るので本物のデータは壊れない）。"""
    upd = run_sql("UPDATE employees SET salary = 0 WHERE id = 1;")
    assert upd["kind"] == "dml"
    assert upd["table"] == "employees"
    assert upd["rowcount"] == 1

    again = run_sql("SELECT salary FROM employees WHERE id = 1;")
    assert again["df"].iloc[0]["salary"] != 0  # 元の値に戻っている


def test_empty_result():
    """条件にあう行が無いときは空の表が返る。"""
    result = run_sql("SELECT * FROM employees WHERE salary > 99999999;")
    assert result["kind"] == "select"
    assert result["df"].empty
