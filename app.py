import streamlit as st
import pandas as pd

# --- 1. ページ設定 ---
st.set_page_config(page_title="正字化コンバーター", page_icon="u5b57")

# --- 2. デザイン設定 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Zen+Old+Mincho&display=swap');
    html, body, [class*="css"] {
        font-family: 'Zen Old Mincho', serif;
    }
    .stTextArea textarea, .stCode {
        font-size: 1.2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. サイドバー設定 ---
st.sidebar.header("設定")
use_ivs = st.sidebar.checkbox("IVS（異体字セレクタ）を使う", value=True, help="厳密な字形を出したい場合はオン推奨。")

# --- ★ここが新機能：注意すべき文字のリスト ---
# これらは文脈によって旧字が変わるため、あえて変換せずに警告を出します
attention_chars = ["弁", "余", "予"]

# --- 4. データ読み込み ---
@st.cache_data
def load_kanji_data():
    try:
        df = pd.read_csv("kanji_data.csv")
        return dict(zip(df['新字体'], df['旧字体']))
    except FileNotFoundError:
        return {}

raw_map = load_kanji_data()

# --- 辞書の構築（モード切替） ---
kanji_map = {}
if raw_map:
    for k, v in raw_map.items():
        # 1. まず「注意すべき文字」は辞書から除外する（プログラム側で処理するため）
        if k in attention_chars:
            continue
            
        # 2. IVSモードの判定
        if len(v) == 1: # 互換漢字なら常に使う
            kanji_map[k] = v
        elif len(v) > 1: # IVS付きならチェックボックス次第
            if use_ivs:
                kanji_map[k] = v

# --- 5. メイン画面 ---
st.title("正字化コンバーター")

# モード案内
if use_ivs:
    st.info("現在のモード：**フル変換**")
else:
    st.success("現在のモード：**互換漢字のみ**")

col1, col2 = st.columns(2)

with col1:
    st.subheader("入力")
    input_text = st.text_area(
        "変換したい文章", 
        height=250, 
        value="安全弁を確認し、余力を残して、予定を組む。", # テスト用例文
        label_visibility="collapsed"
    )

# --- 6. 変換処理（ロジック変更） ---
output_text = ""
has_attention = False # 注意文字が含まれているかチェック用

if raw_map:
    for char in input_text:
        # ★ A. 注意すべき文字が来た場合
        if char in attention_chars:
            output_text += f"【{char}】" # 記号で囲んでそのまま出す
            has_attention = True
            
        # ★ B. 辞書にある場合
        elif char in kanji_map:
            output_text += kanji_map[char]
            
        # ★ C. それ以外（変換なし）
        else:
            output_text += char
else:
    st.error("データファイルが見つかりません。")

with col2:
    st.subheader("結果")
    st.code(output_text, language=None)
    st.caption("※右上のアイコンでコピー")
    
    # ★ 注意書きを表示
    if has_attention:
        st.warning("""
        **⚠️ 確認が必要な文字があります**
        
        以下の文字は文脈によって旧字体が異なるため、あえて変換していません。
        文脈に合わせて手動で修正してください。
        
        * **【弁】** → 花瓣(花びら)、辨明、辯論、弁(冠) など
        * **【余】** → 餘(あまり)、余(われ)
        * **【予】** → 豫(あらかじめ)、予(われ)
        """)

# --- データ情報 ---
with st.expander("現在の登録状況"):
    st.write(f"変換対象: {len(kanji_map)}文字")
