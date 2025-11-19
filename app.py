import streamlit as st
import pandas as pd

# --- 1. ページ設定 ---
st.set_page_config(page_title="康煕字典体コンバーター", page_icon="u5b57")

# --- 2. デザインの変更（CSSハック） ---
# ここで「Zenオールド明朝」というWebフォントを読み込んでいます
st.markdown("""
    <style>
    /* Google Fontsからフォントを読み込む */
    @import url('https://fonts.googleapis.com/css2?family=Zen+Old+Mincho&display=swap');

    /* アプリ全体のフォントを変更 */
    html, body, [class*="css"] {
        font-family: 'Zen Old Mincho', serif;
    }
    
    /* 入力欄と出力欄の文字を少し大きくする */
    .stTextArea textarea, .stCode {
        font-size: 1.2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- タイトル ---
st.title("康煕字典体コンバーター")
st.write("現代の文章を、古風な康煕字典体（旧字体）へ変換します。")

# --- 3. データの読み込み ---
@st.cache_data
def load_kanji_data():
    try:
        df = pd.read_csv("kanji_data.csv")
        return dict(zip(df['新字体'], df['旧字体']))
    except FileNotFoundError:
        return {}

kanji_map = load_kanji_data()

# --- 4. 画面レイアウト ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("現代文（入力）")
    input_text = st.text_area(
        "ここに文章を入力", 
        height=250, 
        value="旧帝国大学で、円満な対話を行い、気迫を持って実践する。",
        label_visibility="collapsed" # ラベルを隠してスッキリさせる
    )

# --- 変換処理 ---
output_text = ""
if kanji_map:
    for char in input_text:
        output_text += kanji_map.get(char, char)
else:
    st.error("データファイル（kanji_data.csv）が見つかりません。")

with col2:
    st.subheader("康煕字典体（結果）")
    # --- 5. 結果表示の工夫 ---
    # st.codeを使うと、右上に自動的に「コピーボタン」が表示されます
    # language=None にすることで、プログラムの色分けを無効化してただの文字として表示します
    st.code(output_text, language=None)
    
    # 注意書き
    st.caption("※右上のアイコンをクリックするとコピーできます")

# --- データ情報 ---
if kanji_map:
    with st.expander("現在の登録文字数を確認する"):
        st.write(f"登録数: {len(kanji_map)}文字")
        st.dataframe(pd.DataFrame(list(kanji_map.items()), columns=["新字体", "旧字体"]))
