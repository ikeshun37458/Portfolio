import pandas as pd
import streamlit as st

st.title("家計簿")

uploader = st.empty()
uploaded_file = uploader.file_uploader("Zaimの入力データをアップロードしてください。", type=["csv"])

# フラグ
# 夏と冬
season_list = ["06", "07", "08", "12", "01", "02"]
season_cate = ["水道・光熱"]
# イベント月(年末年始、GW、お盆)
event_list = ["01", "05", "08", "12"]
event_cate = ["交通費", "エンタメ", "交際費"]

# 初期化
if "df1" not in st.session_state:
    st.session_state.df1 = None 

if uploaded_file:
    uploader.empty()

    df_org = pd.read_csv(uploaded_file, encoding="utf-8")
    st.success("データがアップロードされました！")

    # データの前処理
    df_org["日付"] = df_org["日付"].apply(lambda x: x[:7])
    df_org[["year", "month"]] = df_org["日付"].str.split("-", expand=True)
    df_org = df_org.rename(columns={
        "日付": "year-month",
        "カテゴリ": "category",
        "カテゴリの内訳": "sub_category",
        "支出": "expenses"
    })
    df_org = df_org[[
        "year-month",
        "year",
        "month",
        "category",
        "sub_category",
        "expenses"
    ]]
    df_org = df_org[df_org["expenses"] > 0]

    # 年月のリスト
    date_list = df_org["year-month"].unique()

    # カテゴリ別に集計したのDataFrameを作成→保持
    df_all_cate = pd.DataFrame()
    for date in date_list:
        df_filtered = df_org[df_org["year-month"] == date]
        df_total_cate = df_filtered.copy()
        
        df_total_cate["expen_cate"] = df_filtered.groupby("category")["expenses"].transform("sum")
        df_total_cate = df_total_cate.drop_duplicates(subset=["category"])
        
        df_total_cate = df_total_cate.sort_values(by=["category"])
        df_total_cate = df_total_cate.drop(["expenses", "sub_category"], axis=1)
        df_all_cate = pd.concat([df_all_cate, df_total_cate], ignore_index=True)

    # フラグを追加
    df_all_cate["season"] = df_all_cate["month"].isin(season_list).astype(int)
    df_all_cate["event"] = df_all_cate["month"].isin(event_list).astype(int)
    
    st.session_state.df1 = df_all_cate
    
if st.session_state.df1 is not None:
    uploader.empty()
    st.write("データがアップロードされています。\n実績または予測にお進みください！")
