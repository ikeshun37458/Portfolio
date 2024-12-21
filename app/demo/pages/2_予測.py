import japanize_matplotlib
import matplotlib.pyplot as plt
import requests
import pandas as pd
import streamlit as st
import time

st.title("予測")

if "df2" not in st.session_state:
    st.session_state.df2 = None

if st.session_state.df2 is None:
    st.write("データがアップロードされていません。データアップロードに戻りアップロードしてください！")
else:
    df_all_pred = st.session_state.df2

    
    cate_list = df_all_pred["category"].unique()
    target_cate = st.selectbox(
        "どのカテゴリを確認しますか？",
        cate_list,
        index=None,
        placeholder="選択してください"
    )

    if target_cate != None:
        # データ準備
        data = df_all_pred[df_all_pred["category"].str.contains(target_cate)].iloc[-13:].copy()
        date = data["year-month"].tolist()
        expen_cate = data["expen_cate"].tolist()
        expen_pred = expen_cate[-1]
        
        model_status = st.empty()
        
        if len(date) < 13:
            model_status.write("データ数が十分にありません。他のカテゴリを選択してください！")
        else:
            model_status.write("モデルを学習中...")
            time.sleep(3)
            model_status.write(f"予測された来月の支出額：¥{expen_pred:,.0f}")
    
            plt.plot(
                date[:-1],
                expen_cate[:-1],
                marker=".",
                color="lightseagreen",
                linewidth=2
            )
            plt.plot(
                date[-2:],
                expen_cate[-2:],
                marker=".",
                linestyle="--",
                color="yellow"
            )
            
            plt.xticks(rotation=45, fontsize=10)
            plt.xlabel("支出の月別推移", fontsize=10)
            plt.ylabel("支出", rotation=0, fontsize=10, labelpad=15)
            plt.tight_layout()
            plt.style.use("dark_background")
            st.pyplot(plt)
