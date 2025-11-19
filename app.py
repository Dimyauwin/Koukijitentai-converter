import streamlit as st
import pandas as pd # データを扱うための道具

# ページ設定
st.set_page_config(page_title="康煕字典体コンバーター", page_icon="u5b57")

st.title("康煕字典体コンバーター")
st.write("CSVファイルからデータを読み込み、旧字体（康煕字典体に近い文字）へ変換します。")

# --- データの読み込み ---
# 毎回ファイルを読み込むと遅くなるので、キャッシュ（一時保存）を使います
@st.cache_data
def load_kanji_data():
    try:
        # CSVファイルを読み込む
        df = pd.read_csv("kanji_data.csv")
        # 辞書形式 {'沢': '澤', '浜': '濱'...} に変換して返す
        return dict(zip(df['新字体'], df['旧字体']))
    except FileNotFoundError:
        return {} # ファイルがない場合は空の辞書を返す

# 辞書を作成
kanji_map = load_kanji_data()

# --- 画面レイアウト ---
col1, col2 = st.columns(2)

with col1:
    input_text = st.text_area(
        "変換したい文章（新字体）", 
        height=200, 
        value="旧帝国大学で、円満な対話を行い、気迫を持って実践する。"
    )

# 変換処理
output_text = ""
if kanji_map: # データが読み込めていれば
    for char in input_text:
        output_text += kanji_map.get(char, char)
else:
    st.error("データファイル（kanji_data.csv）が見つかりません。")

with col2:
    st.text_area("変換結果（旧字体）", value=output_text, height=200)

# データの情報表示
if kanji_map:
    st.caption(f"現在の登録文字数: {len(kanji_map)}文字")
    # どんなデータが入っているか確認したい場合、下のチェックを入れると表が見れます
    if st.checkbox("登録データを確認する"):
        st.dataframe(pd.DataFrame(list(kanji_map.items()), columns=["新字体", "旧字体"]))
