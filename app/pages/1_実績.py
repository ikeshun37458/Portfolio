import japanize_matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.title("実績")

if "df1" not in st.session_state:
    st.session_state.df1 = None 

if st.session_state.df1 is None:
    st.write("データがアップロードされていません。データアップロードに戻りアップロードしてください！")
else:
    df_all_cate = st.session_state.df1
    
    date_list = df_all_cate["year-month"].unique()
    target_month = st.selectbox(
        "何月の実績を確認しますか？",
        date_list,
        index=None,
        placeholder="選択してください"
    )

    if target_month != None:
        df_month = df_all_cate[df_all_cate["year-month"] == target_month]
        
        df_month = df_month.sort_values(by=["expen_cate"], ascending=False)
        month_sum = df_month["expen_cate"].sum()
        
        plt.pie(
            list(df_month["expen_cate"]),
            labels=None,
            startangle=90,
            wedgeprops={"edgecolor":"black", "width": 0.3},
            counterclock=False
        )
        plt.legend(labels=df_month["category"], loc="upper right", fontsize=8.5, frameon=False, bbox_to_anchor=(1.1, 1))
        plt.text(0, 0, f"¥{month_sum:,}", ha="center", va="center", fontsize=20, fontweight="bold", color="white")
        plt.style.use("dark_background")
        
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.pyplot(plt)
        with col2:
            df_month = df_month[["category", "expen_cate"]].reset_index(drop=True)
            df_month = df_month.rename(columns={
                "category": "カテゴリ",
                "expen_cate": "支出"
            })
            st.write(df_month)
