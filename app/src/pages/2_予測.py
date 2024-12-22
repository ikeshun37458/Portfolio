import japanize_matplotlib
import matplotlib.pyplot as plt
import requests
import pandas as pd
import streamlit as st

st.title("予測")

# 初期化
if "df1" not in st.session_state:
    st.session_state.df1 = None

if st.session_state.df1 is None:
    st.write("データがアップロードされていません。データアップロードに戻りアップロードしてください！")
else:
    df_all_cate = st.session_state.df1
    cate_list = df_all_cate["category"].unique()
    target_cate = st.selectbox(
        "どのカテゴリを確認しますか？",
        cate_list,
        index=None,
        placeholder="選択してください"
    )

    if target_cate != None:
        # データ準備
        data = df_all_cate[df_all_cate["category"].str.contains(target_cate)].iloc[-12:].copy()
        expen_cate = data["expen_cate"].tolist()

        model_status = st.empty()
        model_status.write("モデルを学習中...")
        # サーバーにデータを送信
        response = requests.post("http://127.0.0.1:8000/train/", json={"data": expen_cate, "step": 3})
    
        if response.status_code == 200:
            model_status.empty()
            prediction = response.json()["prediction"]
            st.write(f"予測された来月の支出額：¥{prediction:,.0f}")

            # 直近1年の年月リストを取得
            date = data["year-month"].tolist()
            last_month = date[-1]
            year, month = int(last_month[:4]), int(last_month[5:7])

            # 来月の年月を取得
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            next_month = f"{year}-{month:02d}"

            plt.plot(
                date,
                expen_cate,
                marker=".",
                color="lightseagreen",
                linewidth=2
            )
            plt.plot(
                [date[-1], next_month],
                [expen_cate[-1], prediction],
                marker=".",
                linestyle="--",
                color="yellow",
                linewidth=2
            )
            
            plt.xticks(rotation=45, fontsize=10)
            plt.xlabel("支出の月別推移", fontsize=10)
            plt.ylabel("支出", rotation=0, fontsize=10, labelpad=15)
            plt.tight_layout()
            plt.style.use("dark_background")
            st.pyplot(plt)
        else:
            model_status.empty()
            st.write("データ数が十分にありません。他のカテゴリを選択してください！")
