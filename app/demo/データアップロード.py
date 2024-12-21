import os
import re
import glob
from io import StringIO
import chardet
import pandas as pd
import requests
import streamlit as st

st.title("家計簿")

if "df1" not in st.session_state:
    st.session_state.df1 = None 
if "df2" not in st.session_state:
    st.session_state.df2 = None 

# files = glob.glob(f"Zaim*.csv")
# response = requests.get(url)
# for file_path in files:
#     # エンコーディングを確認
#     with open(file_path, "rb") as f:
#         result = chardet.detect(f.read())
#         encoding = result["encoding"]
#     df_org = pd.read_csv(file_path, encoding=encoding)

# url = "https://github.com/ikeshun37458/Portfolio/blob/main/app/demo/Zaim.20241209210307.csv"
url = "https://github.com/ikeshun37458/Portfolio/blob/92a400f909b3b108e66a4d0d0776b57114db33b8/app/demo/Zaim.20241209210307.csv"
response = requests.get(url)

st.write(response.text[:100000])

# df_org = pd.read_csv(StringIO(response.text), encoding='utf-8')

if df_org:
    st.success("データがアップロードされました！")

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

# 予測データのDataFrameを作成→保持
file_path = "df_all_pred.csv"
with open(file_path, "rb") as f:
    result = chardet.detect(f.read())
    encoding = result["encoding"]
df_all_pred = pd.read_csv(file_path, encoding=encoding)

st.session_state.df2 = df_all_pred
    
    
if (st.session_state.df1 is not None) and (st.session_state.df2 is not None):
    st.write("データがアップロードされています。\n実績または予測にお進みください！")
