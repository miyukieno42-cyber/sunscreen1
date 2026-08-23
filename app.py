import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --------------------------------------------------
# 1. ページの設定（タイトルや背景色のデザイン）
# --------------------------------------------------
st.set_page_config(
    page_title="子どもの頃の日焼け止めアンケート",
    page_icon="☀️",
    layout="centered"
)

# 可愛くシンプルなデザインにするためのカスタムCSS
st.markdown("""
<style>
    /* 全体の背景色（優しい薄いパステルイエロー/ベージュ） */
    .stApp {
        background-color: #fffdf5;
    }
    
    /* メインカードのスタイル */
    .main-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(230, 200, 170, 0.3);
        border: 2px solid #ffe8cc;
        margin-bottom: 20px;
    }

    /* ボタンのデザイン */
    .stButton>button {
        background-color: #ffb703;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #fb8500;
        color: white;
    }
</style>
""", unsafe_allow_html=True)  # ←ここを修正しました！

# CSVファイルの保存先
DATA_FILE = "sunscreen_responses.csv"

# --------------------------------------------------
# 2. セッション状態の初期化（ステップ管理）
# --------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --------------------------------------------------
# 3. 質問リストの定義
# --------------------------------------------------
QUESTIONS = [
    {
        "id": "q1",
        "question": "小学生の頃、日常的に日焼け止めを塗っていましたか？",
        "options": ["毎日塗っていた", "時々塗っていた", "イベント（プール等）の時だけ", "ほとんど塗っていなかった"]
    },
    {
        "id": "q2",
        "question": "日焼け止めを塗るよう勧めてくれたのは誰ですか？（複数選択可）",
        "type": "multiselect",
        "options": ["お母さん・お父さん", "学校の先生", "部活・習い事のコーチ", "自分で塗るようになった", "その他/覚えていない"]
    },
    {
        "id": "q3",
        "question": "子どもの頃の日焼け止めで嫌だった思い出はありますか？",
        "options": ["ベタベタ感・白浮きが嫌だった", "塗るのが面倒だった", "目に入って痛かった", "特に嫌な思い出はない"]
    },
    {
        "id": "q4",
        "question": "大人になった現在、日焼け対策に対する意識はどうですか？",
        "options": ["とても意識している", "ある程度意識している", "あまり意識していない", "全く意識していない"]
    }
]

# --------------------------------------------------
# 4. 画面表示の制御
# --------------------------------------------------

# タイトルヘッダー
st.markdown("<h1 style='text-align: center; color: #fb8500;'>☀️ 子どもの頃の日焼け止めアンケート</h1>", unsafe_allow_html=True) # ←ここも修正！
st.markdown("<p style='text-align: center; color: #666;'>昔の思い出や体験について教えてください♪</p>", unsafe_allow_html=True)
st.write("---")

total_q = len(QUESTIONS)
current_step = st.session_state.step

# 【A. 回答中画面】
if current_step < total_q:
    q = QUESTIONS[current_step]
    
    # プログレスバー（進捗率）
    progress = (current_step) / total_q
    st.progress(progress)
    st.caption(f"質問 {current_step + 1} / {total_q}")

    # 質問カード
    st.markdown(f"""
    <div class="main-card">
        <h3 style="color: #333; margin-top:0;">Q{current_step + 1}. {q['question']}</h3>
    </div>
    """, unsafe_allow_html=True)

    # 回答の入力フィールド
    is_multi = q.get("type") == "multiselect"
    
    if is_multi:
        user_choice = st.multiselect("該当するものを全て選んでください", q["options"], key=f"select_{q['id']}")
    else:
        user_choice = st.radio("以下から1つ選んでください", q["options"], key=f"radio_{q['id']}", index=None)

    col1, col2 = st.columns([1, 1])
    
    # 次へボタン
    with col2:
        if st.button("次へ ➔", use_container_width=True):
            if not user_choice:
                st.warning("選択肢を選んでから「次へ」を押してください。")
            else:
                if isinstance(user_choice, list):
                    st.session_state.answers[q["id"]] = ", ".join(user_choice)
                else:
                    st.session_state.answers[q["id"]] = user_choice
                
                st.session_state.step += 1
                st.rerun()

    # 戻るボタン
    with col1:
        if current_step > 0:
            if st.button("⬅ 戻る", use_container_width=True):
                st.session_state.step -= 1
                st.rerun()

# 【B. 回答完了画面】
else:
    st.progress(1.0)
    st.markdown("""
    <div class="main-card" style="text-align: center;">
        <h2 style="color: #2a9d8f;">🎉 ご回答ありがとうございました！</h2>
        <p style="color: #555;">アンケートへのご協力感謝いたします。</p>
    </div>
    """, unsafe_allow_html=True)

    # データの保存処理（初回のみ実行）
    if "saved" not in st.session_state:
        new_data = st.session_state.answers.copy()
        new_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        df_new = pd.DataFrame([new_data])

        if os.path.exists(DATA_FILE):
            df_existing = pd.read_csv(DATA_FILE)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
        else:
            df_new.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

        st.session_state.saved = True

    # データダウンロードボタン（管理者用）
    st.write("---")
    st.write("### 📊 回答結果の確認（管理者向け）")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            st.download_button(
                label="📥 集計データ（CSV）をダウンロード",
                data=f,
                file_name="日焼け止めアンケート結果.csv",
                mime="text/csv",
            )
