import streamlit as st
import pandas as pd
import requests

# URL backend Flask
BASE_URL = "http://127.0.0.1:5000"

st.title("Dashboard Nhà Hàng")

# 1. Top 5 nhà hàng
st.header("Top 5 Nhà Hàng Theo Đánh Giá Trung Bình")
try:
    top5 = requests.get(f"{BASE_URL}/api/top5").json()
    df_top5 = pd.DataFrame(top5)
    st.table(df_top5)
except Exception as e:
    st.error(f"Lỗi khi lấy dữ liệu Top 5: {e}")

# 2. Biểu đồ sentiment
st.header("Biểu Đồ Phân Bố Sentiment")
try:
    sentiment = requests.get(f"{BASE_URL}/api/sentiment").json()
    df_sentiment = pd.DataFrame(list(sentiment.items()), columns=["Sentiment", "Count"])
    st.bar_chart(df_sentiment.set_index("Sentiment"))
except Exception as e:
    st.error(f"Lỗi khi lấy dữ liệu Sentiment: {e}")

# 3. Dữ liệu raw (tùy chọn)
st.header("Dữ Liệu 100 Review Đầu Tiên")
try:
    raw = requests.get(f"{BASE_URL}/api/raw").json()
    df_raw = pd.DataFrame(raw)
    st.dataframe(df_raw)
except Exception as e:
    st.error(f"Lỗi khi lấy dữ liệu raw: {e}")
