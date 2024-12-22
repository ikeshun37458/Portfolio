import pandas as pd
import streamlit as st

# タイトル
st.title("家計簿")

uploader = st.empty()
uploaded_file = uploader.file_uploader("Zaimの入力データをアップロードしてください。", type=["csv"])

# 初期化
if "df1" not in st.session_state:
    st.session_state.df1 = None 

if uploaded_file:
    uploader.empty()

    df_org = pd.read_csv(uploaded_file, encoding="utf-8")
    st.success("データがアップロードされました！")

    # データの前処理
    df_org["日付"] = df_org["日付"].apply(lambda x: x[:7])
    df_org = df_org.rename(columns={
        "日付": "year-month",
        "カテゴリ": "category",
        "カテゴリの内訳": "sub_category",
        "支出": "expenses"
    })
    df_org = df_org[[
        "year-month",
        "category",
        "sub_category",
        "expenses"
    ]]
    df_org = df_org[df_org["expenses"] > 0]

    # 年月のリスト
    date_list = df_org["year-month"].unique()

    # 大カテゴリのDataFrameを作成→保持
    df_all_cate = pd.DataFrame()
    for date in date_list:
        df_filtered = df_org[df_org["year-month"] == date]
        df_total_cate = df_filtered.copy()
        
        df_total_cate["expen_cate"] = df_filtered.groupby("category")["expenses"].transform("sum")
        df_total_cate = df_total_cate.drop_duplicates(subset=["category"])
        
        df_total_cate = df_total_cate.sort_values(by=["category"])
        df_total_cate = df_total_cate.drop(["expenses", "sub_category"], axis=1)
        df_all_cate = pd.concat([df_all_cate, df_total_cate], ignore_index=True)
    
    st.session_state.df1 = df_all_cate
    
if st.session_state.df1 is not None:
    uploader.empty()
    st.write("データがアップロードされています。\n実績または予測にお進みください！")
