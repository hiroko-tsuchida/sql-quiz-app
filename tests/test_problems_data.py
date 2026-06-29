"""問題データ（problems.py）の整合性テスト。

問題は47問あり手で書いているため、追加・編集のたびにケアレスミスが
起きやすい。ここでまとめて検査し、壊れたデータをアプリ表示前に弾く。
"""

import pytest

from problems import LEVELS, PROBLEMS

REQUIRED_KEYS = {
    "id",
    "topic",
    "level",
    "question",
    "choices",
    "answer_index",
    "answer_sql",
    "explanation",
}
LEVEL_NUMBERS = {info["level"] for info in LEVELS}


def test_ids_are_unique():
    """id の重複が無い（重複すると _BY_ID で問題が消える）。"""
    ids = [p["id"] for p in PROBLEMS]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_required_keys_present(problem):
    """各問題に必須キーがそろっている。"""
    missing = REQUIRED_KEYS - problem.keys()
    assert not missing, f"id={problem['id']} に不足キー: {missing}"


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_four_choices(problem):
    """選択肢はちょうど4つ（出題時に3択へ縮める前提）。"""
    assert len(problem["choices"]) == 4


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_answer_index_in_range(problem):
    """answer_index が choices の範囲内。"""
    assert 0 <= problem["answer_index"] < len(problem["choices"])


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_answer_sql_matches_choice(problem):
    """answer_sql が choices[answer_index] と一致する（解説と正解の食い違い防止）。"""
    assert problem["answer_sql"] == problem["choices"][problem["answer_index"]]


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_level_is_known(problem):
    """level が LEVELS に定義された番号のいずれか。"""
    assert problem["level"] in LEVEL_NUMBERS


def test_every_level_has_problems():
    """全レベルに最低1問ある（空レベルだとスタートしても出題できない）。"""
    used = {p["level"] for p in PROBLEMS}
    assert LEVEL_NUMBERS <= used, f"問題が無いレベル: {LEVEL_NUMBERS - used}"
