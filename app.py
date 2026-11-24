import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="太古城每日成交與地產新聞", page_icon="🏢", layout="wide"
)

st.title("🏢 太古城住宅每日成交、呎價及新聞追蹤")
st.caption(
    "數據來源：中原地產、美聯物業、香港經濟日報、星島日報 | 每日自動更新"
)


@st.cache_data(ttl=1800)
def load_all_data():
  if os.path.exists("taikoo_data.csv"):
    df_tx = pd.read_csv("taikoo_data.csv")
  else:
    df_tx = pd.DataFrame(
        columns=[
            "成交日期",
            "來源",
            "交易類型",
            "單位資料",
            "實用面積",
            "成交價",
            "實用呎價",
        ]
    )

  if os.path.exists("taikoo_news.csv"):
    df_news = pd.read_csv("taikoo_news.csv")
  else:
    df_news = pd.DataFrame(columns=["發布時間", "媒體來源", "新聞標題", "連結"])

  return df_tx, df_news


df_tx, df_news = load_all_data()

# 建立三大手機友善分頁
tab1, tab2, tab3 = st.tabs(["💰 買賣成交呎價", "🔑 出租成交呎價", "📰 太古城地產新聞"])

# --- 分頁 1：買賣成交 ---
with tab1:
  sale_df = df_tx[df_tx["交易類型"] == "買賣"].copy()
  if not sale_df.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("平均實用呎價", f"${round(sale_df['實用呎價'].mean()):,} / 呎")
    c2.metric("最新一宗呎價", f"${int(sale_df.iloc['實用呎價']):,} / 呎")
    c3.metric("累計紀錄宗數", f"{len(sale_df)} 宗")

    fig = px.line(
        sale_df.sort_values("成交日期"),
        x="成交日期",
        y="實用呎價",
        markers=True,
        title="太古城買賣實用呎價走勢 (HKD/呎)",
    )
    st.plotly_chart(fig, use_container_width=True)

    sale_df["成交價(萬)"] = (sale_df["成交價"] / 10000).round(1).astype(
        str
    ) + "萬"
    sale_df["實用呎價"] = sale_df["實用呎價"].apply(lambda x: f"${int(x):,}")
    st.dataframe(
        sale_df[
            ["成交日期", "來源", "單位資料", "實用面積", "成交價(萬)", "實用呎價"]
        ],
        use_container_width=True,
        hide_index=True,
    )
  else:
    st.info("系統正在收集最新買賣數據，請稍後刷新。")

# --- 分頁 2：出租成交 ---
with tab2:
  rent_df = df_tx[df_tx["交易類型"] == "出租"].copy()
  if not rent_df.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("平均租務呎價", f"${round(rent_df['實用呎價'].mean(), 1)} / 呎")
    c2.metric("最新一宗租務呎價", f"${rent_df.iloc['實用呎價']} / 呎")
    c3.metric("累計租務宗數", f"{len(rent_df)} 宗")

    fig_r = px.line(
        rent_df.sort_values("成交日期"),
        x="成交日期",
        y="實用呎價",
        markers=True,
        title="太古城出租實用呎價走勢 (HKD/呎)",
    )
    st.plotly_chart(fig_r, use_container_width=True)

    rent_df["月租"] = rent_df["成交價"].apply(lambda x: f"${int(x):,}")
    rent_df["實用呎價"] = rent_df["實用呎價"].apply(lambda x: f"${x}")
    st.dataframe(
        rent_df[
            ["成交日期", "來源", "單位資料", "實用面積", "月租", "實用呎價"]
        ],
        use_container_width=True,
        hide_index=True,
    )
  else:
    st.info("系統正在收集最新租務數據，請稍後刷新。")

# --- 分頁 3：地產新聞（經濟日報 & 星島日報） ---
with tab3:
  st.subheader("最新太古城地產報導")
  if not df_news.empty:
    for _, row in df_news.iterrows():
      st.markdown(f"**[{row['媒體來源']}]** [{row['新聞標題']}]({row['連結']})")
      st.caption(f"發布時間：{row['發布時間']}")
      st.divider()
  else:
    st.info("暫無最新新聞，系統將於每日自動更新。")
