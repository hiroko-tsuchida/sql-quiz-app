"""アプリの「純粋ロジック」（画面に依存しない計算）をまとめたモジュール。

ここに置く関数は Streamlit（画面）に依存しないので、そのまま単体テスト
できます。app.py からはここを import して使い、UI 側のコードを薄く保ちます。

含まれるもの:
  - problems_for_level … あるレベルの問題を取り出す
  - three_choices      … 4択データを3択へ縮める（出題用・並びをシャッフル）
  - serialize_progress / deserialize_progress … 進捗の保存・復元
"""

import random

from problems import PROBLEMS


def problems_for_level(level: int):
    """その level の問題を、データに並んでいる順（= id 順）で返す。"""
    return [p for p in PROBLEMS if p["level"] == level]


def three_choices(problem: dict, seed=None):
    """4つの選択肢から誤答を1つ減らして「3択」にし、並びをシャッフルして返す。

    データ（problems.py）は正解1つ＋誤答3つの4択のまま保持し、
    出題時にここで3択へ縮める（最後の誤答を1つ落とす）。

    seed を渡すと、その値に応じて「落とす誤答」と「3択の並び」の両方を決める。
    同じ seed なら必ず同じ結果になる（＝再実行されても変わらない）ので、
    出題画面と採点（check_answer）で seed をそろえれば判定がズレない。
    seed を変えると、落ちる誤答も並びも変わるため出題に変化が出る。
    seed=None のときは最後の誤答を落とし、シャッフルもせず元の順序のまま返す。

    戻り値: (3つの選択肢リスト, その中での正解の位置)
    """
    choices = problem["choices"]
    correct = problem["answer_index"]
    wrong_indices = [i for i in range(len(choices)) if i != correct]
    rng = random.Random(seed) if seed is not None else None
    if rng is not None:
        drop = rng.choice(wrong_indices)  # 落とす誤答も seed で選ぶ
    else:
        drop = wrong_indices[-1]  # seed なしは最後の誤答を落とす（従来どおり）
    kept = [i for i in range(len(choices)) if i != drop]
    if rng is not None:
        rng.shuffle(kept)
    return [choices[i] for i in kept], kept.index(correct)


# --- 進捗の保存／復元用（純関数なので単体テストしやすい）-----------------------
def serialize_progress(s: dict) -> dict:
    """session_state のスナップショット(dict)を JSON 化できる形にする。"""
    return {
        "unlocked": int(s["unlocked"]),
        "passed": sorted(int(x) for x in s["passed"]),
        "level_score": {str(k): list(v) for k, v in s["level_score"].items()},
        "selected_level": int(s["selected_level"]),
        "active": bool(s["active"]),
        "finished": bool(s["finished"]),
        "round_level": int(s["round_level"]),
        "queue": [int(x) for x in s["queue"]],
        "pos": int(s["pos"]),
        "wrong": sorted(int(x) for x in s["wrong"]),
        "answered": bool(s["answered"]),
        "last_correct": bool(s["last_correct"]),
        "is_first_round": bool(s["is_first_round"]),
        "first_correct": int(s["first_correct"]),
        "round_id": int(s["round_id"]),
    }


def deserialize_progress(d: dict) -> dict:
    """保存された dict を session_state に入れられる形(型)に復元する。"""
    return {
        "unlocked": int(d.get("unlocked", 1)),
        "passed": set(int(x) for x in d.get("passed", [])),
        "level_score": {int(k): tuple(v) for k, v in d.get("level_score", {}).items()},
        "selected_level": int(d.get("selected_level", 1)),
        "active": bool(d.get("active", False)),
        "finished": bool(d.get("finished", False)),
        "round_level": int(d.get("round_level", 1)),
        "queue": [int(x) for x in d.get("queue", [])],
        "pos": int(d.get("pos", 0)),
        "wrong": set(int(x) for x in d.get("wrong", [])),
        "answered": bool(d.get("answered", False)),
        "last_correct": bool(d.get("last_correct", False)),
        "is_first_round": bool(d.get("is_first_round", True)),
        "first_correct": int(d.get("first_correct", 0)),
        "round_id": int(d.get("round_id", 0)),
    }
