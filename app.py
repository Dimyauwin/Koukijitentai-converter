import streamlit as st

# ページ設定
st.set_page_config(page_title="康煕字典体コンバーター", page_icon="u5b57")

st.title("康煕字典体コンバーター")
st.write("文章を入力すると、登録された文字だけを康煕字典体（旧字体）に変換します。")

# --- 辞書データ ---
# ここを増やせば変換できる文字が増えます
kanji_map = {
    "沢": "澤",
    "浜": "濱",
    "学": "學",
    "対": "對",
    "弁": "瓣",
    "恵": "惠",
    "鉄": "鐵",
    "亜": "亞",
    "仏": "佛",
    "声": "聲",
    "医": "醫"
}

# --- 画面レイアウト ---
col1, col2 = st.columns(2)

with col1:
    input_text = st.text_area("変換したい文章（新字体）", height=200, value="沢辺で学ぶ、亜細亜の対策と仏の恵み。")

# 変換処理
output_text = ""
for char in input_text:
    output_text += kanji_map.get(char, char) # 辞書にあれば変換、なければそのまま

with col2:
    st.text_area("変換結果（旧字体）", value=output_text, height=200)

st.caption(f"現在の登録文字数: {len(kanji_map)}文字")
