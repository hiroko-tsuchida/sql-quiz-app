"""SQL 問題集アプリ（Streamlit / MySQL 構文）— レベル攻略モード。

使い方:
    streamlit run app.py

遊び方:
    - Lv1（やさしい）から順に挑戦する。レベルは全部で5つ。
    - 各問題は4択。正しい SQL を選んで「答え合わせ」する。
    - レベルの問題を最後まで解くと、点数と間違えた問題が出る。
    - 間違えた問題は「もう一度」で再挑戦。全問正解すると【合格】。
    - 合格すると次のレベルが解放される（まだ解いていない先のレベルはロック）。
"""

import json
import os

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import schema
from problems import LEVELS, PROBLEMS

st.set_page_config(page_title="SQL 問題集（MySQL）", page_icon="🗃️", layout="wide")

MAX_LEVEL = len(LEVELS)                        # 5
_BY_ID = {p["id"]: p for p in PROBLEMS}        # id から問題を引く辞書
_LEVEL_INFO = {d["level"]: d for d in LEVELS}  # level から {title, desc} を引く

# 進捗の自動保存はブラウザの localStorage に行う（ユーザーごとに保存される）。
# ブラウザが無い自動テスト時は SQLQUIZ_NO_STORAGE=1 で無効化して使う。
STORAGE_ENABLED = os.environ.get("SQLQUIZ_NO_STORAGE") != "1"
PROGRESS_KEY = "sqlquiz_progress"

# レベルのスタート画面に出す「早見表」。キーは level 番号。
CHEATSHEET = {
    2: (
        "**基本文法の早見表**\n\n"
        "- `SELECT 列 FROM 表` … どの列を・どの表から\n"
        "- `WHERE 条件` … 条件にあう行だけ\n"
        "- `列 AS 別名` … 列に見出しを付ける\n"
        "- `BETWEEN A AND B` … A以上B以下（両端を含む）\n"
        "- `IN (値1, 値2)` … どれかに一致\n"
        "- `ORDER BY 列 [DESC]` … 並び替え（`DESC`で大きい順）\n"
        "- `DISTINCT` … 重複を除く\n"
        "- `LIMIT n` … 先頭 n 件だけ\n\n"
        "句を書く順番： `SELECT → FROM → WHERE → ORDER BY → LIMIT`"
    ),
}


def problems_for_level(level: int):
    """その level の問題を id 順で返す。"""
    return [p for p in PROBLEMS if p["level"] == level]


# 進捗として保存する session_state のキー。
# メタ進捗（解放/合格/点数）に加えて「途中の攻略状態」も保存することで、
# 1問ごとにチェックポイント保存し、次回は途中の問題から再開できる。
PERSIST_KEYS = [
    "unlocked", "passed", "level_score", "selected_level",
    "active", "finished", "round_level", "queue", "pos", "wrong",
    "answered", "last_correct", "is_first_round", "first_correct", "round_id",
]


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


# =============================================================================
# セッション状態（アプリが覚えておく値）の初期化
# =============================================================================
DEFAULTS = {
    "unlocked": 1,        # 解放済みの最高レベル
    "selected_level": 1,  # いま画面で見ているレベル
    "passed": set(),      # 合格したレベルの集合
    "level_score": {},    # {level: (初回正解数, 問題数)}
    # --- 1ラウンド分の攻略状態 ---
    "active": False,      # 攻略中（問題を解いている最中）か
    "finished": False,    # ラウンドを解き終えて結果画面を表示中か
    "queue": [],          # このラウンドで解く問題 id のリスト
    "pos": 0,             # いまラウンド内の何問目か
    "wrong": set(),       # このラウンドで間違えた id
    "answered": False,    # 今の問題を答え合わせ済みか
    "last_correct": False,  # 今の問題が正解だったか
    "round_level": 1,     # このラウンドが属するレベル
    "is_first_round": True,  # 初回ラウンド（点数を記録する）か
    "first_correct": 0,   # 初回ラウンドの正解数
    "round_id": 0,        # ラジオの key を毎ラウンド変えるための通し番号
    "ended": False,       # 「今日はここまで」で終了画面を表示中か
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

ss = st.session_state

# --- ブラウザに保存した進捗を読み込む（セッションで1回だけ）-------------------
localS = None
if STORAGE_ENABLED:
    from streamlit_local_storage import LocalStorage

    localS = LocalStorage()
    if not ss.get("_loaded_from_storage"):
        raw = localS.getItem(PROGRESS_KEY)
        if raw:
            try:
                data = raw if isinstance(raw, dict) else json.loads(raw)
                for k, v in deserialize_progress(data).items():
                    ss[k] = v
            except Exception:
                pass  # 壊れたデータは無視して最初から
        # 直後の無駄な再保存を防ぐため、現在値を「保存済み」として記録
        ss["_saved_payload"] = json.dumps(
            serialize_progress({k: ss[k] for k in PERSIST_KEYS}), ensure_ascii=False
        )
        ss["_loaded_from_storage"] = True


def save_progress():
    """進捗（途中の攻略状態を含む）が変わっていればブラウザに保存する。"""
    if not (STORAGE_ENABLED and localS is not None):
        return
    payload = json.dumps(
        serialize_progress({k: ss[k] for k in PERSIST_KEYS}), ensure_ascii=False
    )
    if ss.get("_saved_payload") != payload:
        localS.setItem(PROGRESS_KEY, payload, key="sqlquiz_save")
        ss["_saved_payload"] = payload


# =============================================================================
# 状態を変える関数（ボタンの on_click から呼ぶ。手動 st.rerun は使わない）
# =============================================================================
def select_level(level: int):
    """サイドバーでレベルを選んだとき。攻略状態をリセットしてスタート画面へ。"""
    ss.selected_level = level
    ss.active = False
    ss.finished = False


def start_round(level: int, ids: list, is_first: bool):
    """1ラウンドを開始する。"""
    ss.round_level = level
    ss.queue = list(ids)
    ss.pos = 0
    ss.wrong = set()
    ss.answered = False
    ss.last_correct = False
    ss.is_first_round = is_first
    ss.first_correct = 0
    ss.active = True
    ss.finished = False
    ss.round_id += 1


def check_answer(problem: dict, radio_key: str):
    """『答え合わせ』ボタン。選んだ選択肢を採点する。"""
    chosen_label = ss[radio_key]
    chosen_index = ord(chosen_label) - ord("A")
    is_correct = chosen_index == problem["answer_index"]
    ss.answered = True
    ss.last_correct = is_correct
    if is_correct:
        if ss.is_first_round:
            ss.first_correct += 1
    else:
        ss.wrong.add(problem["id"])


def go_next():
    """次の問題へ。最後まで解いたら結果画面へ。"""
    ss.pos += 1
    ss.answered = False
    ss.last_correct = False
    if ss.pos >= len(ss.queue):
        ss.active = False
        ss.finished = True
        # 初回ラウンドの結果を、このレベルの点数として記録する
        if ss.is_first_round:
            ss.level_score[ss.round_level] = (ss.first_correct, len(ss.queue))


def reset_progress():
    """進捗をすべて初期化する。"""
    for key, value in DEFAULTS.items():
        # set/list/dict は新しい空オブジェクトに（参照の共有を避ける）
        ss[key] = type(value)() if isinstance(value, (set, list, dict)) else value


def end_session():
    """「今日はここまで」ボタン。いまの問題を確定して次へ進めてから終了画面へ。

    これにより、次に再開したときは「次の問題」から始まる。
    （保存は本体側で行う）
    """
    if ss.active and ss.answered:
        go_next()  # 答え済みの問題を確定し、次の問題へ進めておく
    ss.ended = True


def resume_session():
    """終了画面から戻る。"""
    ss.ended = False


def render_progress_donut(container):
    """合格したレベルを輪（ドーナツ）グラフで表示する。"""
    passed_n = len(ss.passed)
    df = pd.DataFrame(
        {
            "区分": ["合格", "未合格"],
            "レベル数": [passed_n, MAX_LEVEL - passed_n],
        }
    )
    ring = (
        alt.Chart(df)
        .mark_arc(innerRadius=45, outerRadius=70)
        .encode(
            theta=alt.Theta("レベル数:Q", stack=True),
            color=alt.Color(
                "区分:N",
                scale=alt.Scale(domain=["合格", "未合格"], range=["#2E7D32", "#E0E0E0"]),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
            order=alt.Order("区分:N"),
            tooltip=["区分:N", "レベル数:Q"],
        )
    )
    center = (
        alt.Chart(pd.DataFrame({"label": [f"{passed_n}/{MAX_LEVEL}"]}))
        .mark_text(size=24, fontWeight="bold", color="#2E7D32")
        .encode(text="label:N")
    )
    container.altair_chart(ring + center, use_container_width=True)


# =============================================================================
# 「今日はここまで」終了画面（保存してタブを閉じる）
# =============================================================================
if ss.ended:
    save_progress()  # ここまでの進捗を確実に保存
    st.title("👋 今日はここまで")
    st.success("進捗を保存しました。続きはまたいつでも、途中の問題から再開できます。")
    st.caption("このタブを自動で閉じようとします。閉じない場合は手動で閉じてください。")
    # ブラウザによっては window.close() が無視されます（その場合は上の案内のとおり手動で）。
    components.html(
        "<script>setTimeout(function(){window.open('','_self');window.close();}, 400);</script>",
        height=0,
    )
    st.button("◀ 戻って続ける", on_click=resume_session)
    st.stop()


# =============================================================================
# サイドバー：レベル選択と進捗
# =============================================================================
st.sidebar.title("🗃️ SQL 問題集")
st.sidebar.caption("MySQL の書き方で学ぶ・Lv1〜Lv5")

st.sidebar.subheader("レベルを選ぶ")
for info in LEVELS:
    lv = info["level"]
    n = len(problems_for_level(lv))
    if lv in ss.passed:
        mark, locked = "✅", False
    elif lv <= ss.unlocked:
        mark, locked = "▶️", False
    else:
        mark, locked = "🔒", True

    label = f"{mark} Lv{lv} {info['title']}（{n}問）"
    if locked:
        st.sidebar.button(label, key=f"lv_{lv}", disabled=True, use_container_width=True)
    else:
        st.sidebar.button(
            label,
            key=f"lv_{lv}",
            type="primary" if lv == ss.selected_level else "secondary",
            use_container_width=True,
            on_click=select_level,
            args=(lv,),
        )

# レベルごとの点数
st.sidebar.divider()
st.sidebar.subheader("レベルごとの点数")
for info in LEVELS:
    lv = info["level"]
    score = ss.level_score.get(lv)
    status = "（未挑戦）"
    if score is not None:
        correct, total = score
        status = f"{correct} / {total} 点"
    if lv in ss.passed:
        status += "　🎉合格"
    st.sidebar.write(f"Lv{lv}：{status}")

st.sidebar.divider()
st.sidebar.subheader("合格したレベル")
render_progress_donut(st.sidebar)
st.sidebar.button("進捗をリセット", on_click=reset_progress)


# =============================================================================
# メイン画面
# =============================================================================
st.title("SQL 問題集（MySQL）")

# --- テーブル定義とサンプルデータ（折りたたみ）-------------------------------
with st.expander("📋 テーブル定義とサンプルデータを見る", expanded=False):
    st.caption("問題はこのデータベースを題材にしています。いつでもここで確認できます。")
    st.code(schema.CREATE_STATEMENTS, language="sql")
    for table_name, df in schema.TABLES.items():
        st.markdown(f"**{table_name}**")
        st.dataframe(df, hide_index=True, use_container_width=True)

st.divider()

level = ss.selected_level
info = _LEVEL_INFO[level]


def render_question(problem: dict):
    """1問分の出題・答え合わせ・解説を表示する（4択）。"""
    total = len(ss.queue)
    st.caption(
        f"このラウンド：問題 {ss.pos + 1} / {total}　｜　項目: {problem['topic']}"
    )
    st.subheader("問題")
    st.write(problem["question"])

    # ヒント（構文の意味）。見なくても解けるよう、たたんで表示する。
    if problem.get("hint"):
        with st.expander("💡 ヒントを見る（構文の意味）"):
            st.markdown(problem["hint"])

    choices = problem["choices"]
    labels = [chr(ord("A") + i) for i in range(len(choices))]

    st.markdown("#### 選択肢（正しい SQL を1つ選んでください）")
    for label, sql in zip(labels, choices):
        st.markdown(f"**{label}**")
        st.code(sql, language="sql")

    # key にラウンド番号を含め、毎ラウンド・各問題でラジオを独立させる
    radio_key = f"choice_{problem['id']}_{ss.round_id}"
    st.radio("あなたの答え", labels, key=radio_key, horizontal=True)

    if not ss.answered:
        # まだ答え合わせ前：答え合わせボタンだけ出す
        st.button(
            "✅ 答え合わせ",
            type="primary",
            on_click=check_answer,
            args=(problem, radio_key),
        )
    else:
        # 答え合わせ後：結果と解説、次へボタン
        correct_label = labels[problem["answer_index"]]
        if ss.last_correct:
            st.success(f"正解！　答えは {correct_label} です。")
        else:
            st.error(f"不正解…　正解は {correct_label} です。")

        st.markdown("#### ✅ 正解の SQL（MySQL）")
        st.code(problem["answer_sql"], language="sql")
        st.markdown("#### 📖 解説")
        st.write(problem["explanation"])
        if problem.get("points"):
            st.markdown("#### 💡 ポイント / よくある間違い")
            st.info(problem["points"])

        is_last = ss.pos >= len(ss.queue) - 1
        col_next, col_end = st.columns(2)
        with col_next:
            st.button(
                "結果を見る" if is_last else "次の問題",
                type="primary",
                on_click=go_next,
                use_container_width=True,
            )
        with col_end:
            st.button(
                "🌙 今日はここまで",
                on_click=end_session,
                use_container_width=True,
            )


def render_result():
    """ラウンド終了後の結果画面。"""
    lv = ss.round_level
    total = len(problems_for_level(lv))
    wrong = ss.wrong

    st.header(f"Lv{lv} {_LEVEL_INFO[lv]['title']}　結果")

    score = ss.level_score.get(lv)
    if score is not None:
        correct, score_total = score
        st.metric("このレベルの点数（初回）", f"{correct} / {score_total} 点")

    if not wrong:
        # --- 合格 ---
        ss.passed.add(lv)
        if lv < MAX_LEVEL:
            ss.unlocked = max(ss.unlocked, lv + 1)

        st.success(f"🎉 全問正解！ Lv{lv} は【合格】です。")
        # 風船の上昇アニメを半分の速さに（標準は 750ms → 1500ms に上書き）。
        # Streamlit の風船は data-testid="stBalloons" の中の img をインラインで
        # animationDuration:750ms にしているため、!important で上書きする。
        st.markdown(
            "<style>"
            '[data-testid="stBalloons"] img { animation-duration: 1500ms !important; }'
            "</style>",
            unsafe_allow_html=True,
        )
        st.balloons()

        if lv < MAX_LEVEL:
            next_info = _LEVEL_INFO[lv + 1]
            st.write(f"次は **Lv{lv + 1}（{next_info['title']}）** が解放されました。")
            st.button(
                f"Lv{lv + 1} へ進む →",
                type="primary",
                on_click=select_level,
                args=(lv + 1,),
            )
        else:
            st.success("🏆 全5レベルを制覇しました！おめでとうございます！")
    else:
        # --- まだ間違いが残っている ---
        st.warning(f"あと {len(wrong)} 問。間違えた問題をもう一度解いて、全問正解を目指しましょう。")
        st.markdown("#### ❌ 間違えた問題")
        for pid in sorted(wrong):
            st.write(f"・{_BY_ID[pid]['question']}")

        st.button(
            "間違えた問題をもう一度 🔁",
            type="primary",
            on_click=start_round,
            args=(lv, sorted(wrong), False),
        )

    st.divider()
    st.button(
        "このレベルを最初からやり直す",
        on_click=select_level,
        args=(lv,),
    )


# --- 画面の出し分け ----------------------------------------------------------
if ss.active and ss.queue and 0 <= ss.pos < len(ss.queue):
    # 攻略中：いまの問題を出す（途中保存からの再開もここに入る）
    render_question(_BY_ID[ss.queue[ss.pos]])
elif ss.finished:
    # 結果画面
    render_result()
else:
    # スタート画面
    n = len(problems_for_level(level))
    st.header(f"Lv{level}　{info['title']}")
    st.write(info["desc"])
    st.caption(f"問題数：{n} 問　／　全問正解で合格です。")
    if level in ss.passed:
        st.success("このレベルは合格済みです。もう一度挑戦することもできます。")
    # このレベルに早見表があれば表示（Lv2＝基本文法など）
    if level in CHEATSHEET:
        with st.expander("📘 基本文法の早見表（クリックで開く）", expanded=False):
            st.markdown(CHEATSHEET[level])
    st.button(
        "▶️ スタート",
        type="primary",
        on_click=start_round,
        args=(level, [p["id"] for p in problems_for_level(level)], True),
    )


# --- 進捗の自動保存（この実行で進捗が変わっていればブラウザに保存）-------------
save_progress()
