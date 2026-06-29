"""純粋ロジック（quiz_logic.py）のテスト。

画面（Streamlit）に依存しない関数だけを対象にしているので、
ここでは普通の Python の値を渡して結果を確かめるだけで済みます。
"""

from quiz_logic import (
    deserialize_progress,
    problems_for_level,
    serialize_progress,
    three_choices,
)


# --- three_choices ----------------------------------------------------------
def _sample_problem(answer_index: int) -> dict:
    """4択のダミー問題を作る。choices の中身で位置が分かるようにしておく。"""
    return {
        "choices": ["A0", "A1", "A2", "A3"],
        "answer_index": answer_index,
    }


def test_three_choices_returns_three():
    """4択 → 必ず3択に縮む。"""
    choices, _ = three_choices(_sample_problem(0))
    assert len(choices) == 3


def test_three_choices_keeps_correct_answer():
    """どの位置が正解でも、正解の選択肢は3択の中に残り、
    返り値の正解位置が本当にその選択肢を指している（シャッフル有無の両方で）。"""
    for ans in range(4):
        problem = _sample_problem(ans)
        for seed in (None, "1:1", "2:5"):
            choices, correct_index = three_choices(problem, seed=seed)
            # 返ってきた correct_index が、元の正解の文言を指している
            assert choices[correct_index] == problem["choices"][ans]
            # 正解は必ず残っている
            assert problem["choices"][ans] in choices


def test_three_choices_shuffle_is_stable_per_seed():
    """同じ seed なら毎回まったく同じ並びになる（再実行で並びがブレない）。"""
    problem = _sample_problem(0)
    first = three_choices(problem, seed="3:7")
    second = three_choices(problem, seed="3:7")
    assert first == second


def test_three_choices_seed_changes_order():
    """seed を変えると並びが変わりうる。複数 seed のどれかは
    シャッフルなし（seed=None）と異なる並びになる。"""
    problem = _sample_problem(0)
    base, _ = three_choices(problem, seed=None)
    orders = {tuple(three_choices(problem, seed=f"r:{i}")[0]) for i in range(20)}
    assert any(order != tuple(base) for order in orders)


# --- problems_for_level -----------------------------------------------------
def test_problems_for_level_filters_by_level():
    """指定レベルの問題だけが返り、すべてその level を持つ。"""
    for lv in range(1, 13):
        result = problems_for_level(lv)
        assert all(p["level"] == lv for p in result)


# --- serialize / deserialize（往復しても壊れない）---------------------------
def test_progress_round_trip():
    """session_state 相当の値 → 保存形式 → 復元 で、中身が保たれる。"""
    state = {
        "unlocked": 3,
        "passed": {1, 2},
        "level_score": {1: (3, 3), 2: (2, 4)},
        "selected_level": 2,
        "active": True,
        "finished": False,
        "round_level": 2,
        "queue": [5, 6, 7],
        "pos": 1,
        "wrong": {6},
        "answered": True,
        "last_correct": False,
        "is_first_round": True,
        "first_correct": 1,
        "round_id": 4,
    }
    restored = deserialize_progress(serialize_progress(state))

    assert restored["unlocked"] == 3
    assert restored["passed"] == {1, 2}
    assert restored["level_score"] == {1: (3, 3), 2: (2, 4)}
    assert restored["queue"] == [5, 6, 7]
    assert restored["wrong"] == {6}
    assert restored["active"] is True
    assert restored["last_correct"] is False


def test_deserialize_uses_defaults_for_empty():
    """空の dict からでも、欠けたキーは既定値で安全に復元される。"""
    restored = deserialize_progress({})
    assert restored["unlocked"] == 1
    assert restored["selected_level"] == 1
    assert restored["passed"] == set()
    assert restored["queue"] == []
    assert restored["is_first_round"] is True
