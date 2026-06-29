"""SQL 問題集アプリ（Streamlit / MySQL 構文）— レベル攻略モード。

使い方:
    streamlit run app.py

遊び方:
    - レベルは全部で13。どのレベルからでも自由に選んで挑戦できる。
    - 各問題は3択。正しい SQL を選んで「答え合わせ」する。
    - レベルの問題を最後まで解くと、点数と間違えた問題が出る。
    - 間違えた問題は「もう一度」で再挑戦。全問正解すると【合格】。
"""

import json
import os
import random

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import runner
import schema
from problems import LEVELS, PROBLEMS
from quiz_logic import (
    deserialize_progress,
    problems_for_level,
    serialize_progress,
    three_choices,
)

st.set_page_config(page_title="SQL 問題集（MySQL）", page_icon="🗃️", layout="wide")

MAX_LEVEL = len(LEVELS)  # レベル総数（現在は 13）
_BY_ID = {p["id"]: p for p in PROBLEMS}  # id から問題を引く辞書
_LEVEL_INFO = {d["level"]: d for d in LEVELS}  # level から {title, desc} を引く

# 進捗の自動保存はブラウザの localStorage に行う（ユーザーごとに保存される）。
# ブラウザが無い自動テスト時は SQLQUIZ_NO_STORAGE=1 で無効化して使う。
STORAGE_ENABLED = os.environ.get("SQLQUIZ_NO_STORAGE") != "1"
PROGRESS_KEY = "sqlquiz_progress"


# 進捗として保存する session_state のキー。
# メタ進捗（解放/合格/点数）に加えて「途中の攻略状態」も保存することで、
# 1問ごとにチェックポイント保存し、次回は途中の問題から再開できる。
PERSIST_KEYS = [
    "unlocked",
    "passed",
    "level_score",
    "selected_level",
    "active",
    "finished",
    "round_level",
    "queue",
    "pos",
    "wrong",
    "answered",
    "last_correct",
    "is_first_round",
    "first_correct",
    "round_id",
]


# =============================================================================
# セッション状態（アプリが覚えておく値）の初期化
# =============================================================================
DEFAULTS = {
    "unlocked": 1,  # 解放済みの最高レベル
    "selected_level": 1,  # いま画面で見ているレベル
    "passed": set(),  # 合格したレベルの集合
    "level_score": {},  # {level: (初回正解数, 問題数)}
    # --- 1ラウンド分の攻略状態 ---
    "active": False,  # 攻略中（問題を解いている最中）か
    "finished": False,  # ラウンドを解き終えて結果画面を表示中か
    "queue": [],  # このラウンドで解く問題 id のリスト
    "pos": 0,  # いまラウンド内の何問目か
    "wrong": set(),  # このラウンドで間違えた id
    "answered": False,  # 今の問題を答え合わせ済みか
    "last_correct": False,  # 今の問題が正解だったか
    "round_level": 1,  # このラウンドが属するレベル
    "is_first_round": True,  # 初回ラウンド（点数を記録する）か
    "first_correct": 0,  # 初回ラウンドの正解数
    "round_id": 0,  # ラジオの key を毎ラウンド変えるための通し番号
    "ended": False,  # 「今日はここまで」で終了画面を表示中か
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


def choice_seed(problem: dict) -> str:
    """選択肢シャッフル用のシード。ラウンドと問題で固定し、再実行でも並びを保つ。

    出題画面（render_question）と採点（check_answer）でこの同じシードを使うことで、
    両者の3択の並びが必ず一致し、判定がズレない。round_id はラウンドごとに
    増えるので、同じ問題でも再挑戦すると別の並びになる。
    """
    return f"{ss.round_id}:{problem['id']}"


def check_answer(problem: dict, radio_key: str):
    """『答え合わせ』ボタン。選んだ選択肢を採点する（3択）。"""
    _, correct_index = three_choices(problem, seed=choice_seed(problem))
    chosen_label = ss[radio_key]
    chosen_index = ord(chosen_label) - ord("A")
    is_correct = chosen_index == correct_index
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
    ss.scroll_to_top = True  # 次の画面ではページ先頭へスクロールする
    if ss.pos >= len(ss.queue):
        ss.active = False
        ss.finished = True
        # 初回ラウンドの結果を、このレベルの点数として記録する
        if ss.is_first_round:
            ss.level_score[ss.round_level] = (ss.first_correct, len(ss.queue))
        # 間違いを直し切って全問正解（＝合格）したら、点数を満点に更新する。
        # 「間違えた問題をもう一度」での再挑戦でもここで反映される。
        if not ss.wrong:
            full = len(problems_for_level(ss.round_level))
            ss.level_score[ss.round_level] = (full, full)


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
                scale=alt.Scale(
                    domain=["合格", "未合格"], range=["#2E7D32", "#E0E0E0"]
                ),
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
st.sidebar.caption("MySQL の書き方で学ぶ・Lv1〜Lv13")

st.sidebar.subheader("レベルを選ぶ")
# レベルボタンのラベルを左寄せにする（Streamlit の既定は中央寄せ）。
# ボタン本体・内側のラッパー・テキスト(p)すべてに効かせて確実に左寄せする。
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] .stButton button {
        justify-content: flex-start !important;
        text-align: left !important;
    }
    [data-testid="stSidebar"] .stButton button > div,
    [data-testid="stSidebar"] .stButton button [data-testid="stMarkdownContainer"] {
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stButton button p {
        text-align: left !important;
        width: 100% !important;
        margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
for info in LEVELS:
    lv = info["level"]
    n = len(problems_for_level(lv))
    # どのレベルもいつでも選べる（ロックなし）。合格済みは ✅ で示す。
    mark = "✅" if lv in ss.passed else "▶️"

    # 「Lv＋数字＋ピリオド」を太字にする（ボタンのラベルは Markdown が使える）。
    label = f"{mark} **Lv{lv}.** {info['title']}（{n}問）"
    st.sidebar.button(
        label,
        key=f"lv_{lv}",
        type="primary" if lv == ss.selected_level else "secondary",
        use_container_width=True,
        on_click=select_level,
        args=(lv,),
    )

# 進捗状況
st.sidebar.divider()
st.sidebar.subheader("進捗状況")
for info in LEVELS:
    lv = info["level"]
    score = ss.level_score.get(lv)
    if score is None:
        # まだ一度も解いていないレベル
        status = "未挑戦"
    else:
        # 一度でも解いたレベルは「正解数／問題数」と状態を出す
        correct, total = score
        mark = "✅合格" if lv in ss.passed else "🔄挑戦中"
        status = f"{correct}/{total}問 {mark}"
    st.sidebar.write(f"Lv{lv}：{status}")

st.sidebar.divider()
st.sidebar.subheader("合格したレベル")
render_progress_donut(st.sidebar)
st.sidebar.button("進捗をリセット", on_click=reset_progress)


# =============================================================================
# メイン画面
# =============================================================================
# 見出し。通常の st.title（約2.75rem）の半分くらいの大きさにする。
st.markdown(
    "<h1 style='font-size: 1.375rem; font-weight: 700; margin: 0 0 0.5rem 0;'>"
    "SQL 問題集（MySQL）</h1>",
    unsafe_allow_html=True,
)

# --- テーブル定義とサンプルデータ（折りたたみ）-------------------------------
with st.expander(
    "📋 テーブル（departments, employees, products, orders）定義とサンプルデータを見る",
    expanded=False,
):
    st.caption("問題はこのデータベースを題材にしています。いつでもここで確認できます。")
    st.code(schema.CREATE_STATEMENTS, language="sql")
    for table_name, df in schema.TABLES.items():
        st.markdown(f"**{table_name}**")
        st.dataframe(df, hide_index=True, use_container_width=True)

st.divider()

level = ss.selected_level
info = _LEVEL_INFO[level]


def render_answer_result(problem: dict):
    """正解 SQL を実際に実行して、その出力結果（表）を表示する。

    SELECT は結果の表をそのまま、INSERT/UPDATE/DELETE は『実行後のテーブル』を
    表示する。実行に失敗しても画面が止まらないよう、失敗時は注意書きだけ出す。
    """
    try:
        result = runner.run_sql(problem["answer_sql"])
    except Exception:
        st.caption("（この SQL の実行結果は表示できませんでした）")
        return

    # 実行結果の表は最大 3 行まで表示する（多いときは先頭だけ見せる）。
    max_rows = 3
    if result["kind"] == "select":
        df = result["df"]
        if df.empty:
            st.caption("条件にあう行はありません（0 件）。")
        else:
            st.dataframe(df.head(max_rows), hide_index=True, use_container_width=True)
            if len(df) > max_rows:
                st.caption(f"{len(df)} 件中 先頭 {max_rows} 件を表示")
            else:
                st.caption(f"{len(df)} 件")
    else:
        # INSERT / UPDATE / DELETE：実行後のテーブルの中身を見せる
        table = result["table"]
        st.caption(
            f"この SQL は {table} テーブルを変更します（{result['rowcount']} 行）。"
            f"実行後の {table} テーブルは次のとおりです。"
        )
        if result["df"] is not None:
            df = result["df"]
            st.dataframe(df.head(max_rows), hide_index=True, use_container_width=True)
            if len(df) > max_rows:
                st.caption(f"{len(df)} 件中 先頭 {max_rows} 件を表示")


def render_question(problem: dict):
    """1問分の出題・答え合わせ・解説を表示する（3択）。"""
    total = len(ss.queue)
    st.caption(
        f"このラウンド：問題 {ss.pos + 1} / {total}　｜　項目: {problem['topic']}"
    )
    st.subheader(f"問題 {ss.pos + 1}")
    # 問題文は本文より一段大きめ（約1rem → 1.2rem）にして読みやすくする。
    st.markdown(
        f"<p style='font-size: 1.2rem; line-height: 1.7; margin: 0 0 0.5rem 0;'>"
        f"{problem['question']}</p>",
        unsafe_allow_html=True,
    )

    # 実行結果はヒントの上に、折りたたみで表示する（答えを選ぶ前から見られる）
    with st.expander("▶️ 実行結果を見る"):
        render_answer_result(problem)

    # ヒント（構文の意味）。見なくても解けるよう、たたんで表示する。
    if problem.get("hint"):
        with st.expander("💡 ヒントを見る（構文の意味）"):
            st.markdown(problem["hint"])

    choices, correct_index = three_choices(problem, seed=choice_seed(problem))
    labels = [chr(ord("A") + i) for i in range(len(choices))]

    st.markdown("#### 選択肢")
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
        correct_label = labels[correct_index]
        if ss.last_correct:
            st.success(f"正解！　答えは {correct_label} です。")
        else:
            st.error(f"不正解…　正解は {correct_label} です。")

        st.markdown("#### ✅ 正解の SQL（MySQL）")
        st.code(problem["answer_sql"], language="sql")

        # 「次の問題」「今日はここまで」は解説の上に置く
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

        st.markdown("#### 📖 解説")
        st.write(problem["explanation"])
        if problem.get("points"):
            st.markdown("#### 💡 ポイント / よくある間違い")
            st.info(problem["points"])


def render_result():
    """ラウンド終了後の結果画面。"""
    lv = ss.round_level
    total = len(problems_for_level(lv))
    wrong = ss.wrong

    st.header(f"Lv{lv} {_LEVEL_INFO[lv]['title']}　結果")

    score = ss.level_score.get(lv)
    if score is not None:
        correct, score_total = score
        st.metric("このレベルの正解数", f"{correct} / {score_total} 問")

    if not wrong:
        # --- 合格 ---
        ss.passed.add(lv)
        if lv < MAX_LEVEL:
            ss.unlocked = max(ss.unlocked, lv + 1)

        st.success(f"🎉 全問正解！ Lv{lv} は【合格】です。")
        # お祝い演出：カラフルな花がひらひら降ってくるアニメ（CSS のみ）。
        # たくさんの花の絵文字を、横位置・大きさ・落ちる速さ・開始時間を
        # ばらばらにして降らせる。
        _flowers = ["🌸", "🌺", "🌻", "🌷", "🌹", "💐", "🏵️", "🌼", "🌸", "🏵️"]
        _petals = "".join(
            f"<span class='flower' style='"
            f"left:{random.uniform(0, 100):.1f}%;"
            f"font-size:{random.uniform(3.6, 7.8):.2f}rem;"
            f"animation-delay:{random.uniform(0, 1.2):.2f}s;"
            f"animation-duration:{random.uniform(2.6, 4.6):.2f}s;'>"
            f"{random.choice(_flowers)}</span>"
            for _ in range(135)
        )
        st.markdown(
            "<style>"
            "@keyframes flowerfall{"
            "0%{transform:translateY(-12vh) rotate(0deg);opacity:1;}"
            "100%{transform:translateY(112vh) rotate(540deg);opacity:.9;}}"
            ".flower{position:fixed;top:0;z-index:9999;pointer-events:none;"
            "animation-name:flowerfall;animation-timing-function:linear;"
            "animation-iteration-count:1;will-change:transform;}"
            "</style>"
            f"<div aria-hidden='true'>{_petals}</div>",
            unsafe_allow_html=True,
        )

        if lv < MAX_LEVEL:
            next_info = _LEVEL_INFO[lv + 1]
            st.write(
                f"次は **Lv{lv + 1}（{next_info['title']}）** に挑戦してみましょう。"
            )
            st.button(
                f"Lv{lv + 1} へ進む →",
                type="primary",
                on_click=select_level,
                args=(lv + 1,),
            )
        else:
            st.success("🏆 全12レベルを制覇しました！おめでとうございます！")
    else:
        # --- まだ間違いが残っている ---
        st.warning(
            f"あと {len(wrong)} 問。間違えた問題をもう一度解いて、全問正解を目指しましょう。"
        )
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


def scroll_to_top():
    """親ページ（Streamlit 本体）をいちばん上までスクロールする。

    コンポーネントは iframe の中で動くので、window.parent 側のスクロール要素を
    たどってトップへ戻す。再実行直後の描画タイミングのブレに備えて数回試す。
    """
    components.html(
        """
        <script>
        const toTop = () => {
            const doc = window.parent.document;
            const targets = [
                doc.querySelector('section.main'),
                doc.querySelector('[data-testid="stMain"]'),
                doc.querySelector('.stMainBlockContainer'),
                doc.scrollingElement, doc.documentElement, doc.body,
            ];
            for (const el of targets) {
                if (el) { try { el.scrollTo(0, 0); } catch (e) {} }
            }
            try { window.parent.scrollTo(0, 0); } catch (e) {}
        };
        toTop();
        setTimeout(toTop, 50);
        setTimeout(toTop, 150);
        </script>
        """,
        height=0,
    )


# 「次の問題」などで進んだ直後は、ページ先頭へスクロールする
if ss.get("scroll_to_top"):
    scroll_to_top()
    ss.scroll_to_top = False


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
    st.button(
        "▶️ スタート",
        type="primary",
        on_click=start_round,
        args=(level, [p["id"] for p in problems_for_level(level)], True),
    )


# --- 進捗の自動保存（この実行で進捗が変わっていればブラウザに保存）-------------
save_progress()
