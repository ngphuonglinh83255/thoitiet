import streamlit as st
import pandas as pd
import json
import altair as alt

st.set_page_config(page_title="Giám sát thời tiết", layout="wide")
st.title("🌦️ Dashboard Giám sát Thời tiết - Hanoi")

def load_data():
    with open('weather_log.json') as f:
        lines = f.readlines()
        records = [json.loads(line) for line in lines if line.strip()]
        return pd.DataFrame(records)

df = load_data()

# Xử lý thời gian
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Cảnh báo
    st.subheader("🚨 Cảnh báo thời tiết hiện tại")
    latest = df.iloc[-1]
    temp = latest["temperature"]
    humidity = latest["humidity"]

    alerts = []

    if temp > 35:
        alerts.append("🌡️ Cảnh báo: Nhiệt độ quá cao!")
    elif temp < 10:
        alerts.append("❄️ Cảnh báo: Nhiệt độ quá thấp!")

    if humidity > 90:
        alerts.append("💧 Cảnh báo: Độ ẩm quá cao!")
    elif humidity < 30:
        alerts.append("🔥 Cảnh báo: Độ ẩm quá thấp!")

    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("✅ Nhiệt độ và độ ẩm đang ổn định.")

    # Biểu đồ thời gian thực bằng Altair
    st.subheader("📈 Biểu đồ đường theo thời gian")

    # Vẽ nhiệt độ
    chart_temp = alt.Chart(df).mark_line(color="red").encode(
        x=alt.X('timestamp:T', title='Thời gian'),
        y=alt.Y('temperature:Q', title='Nhiệt độ (°C)'),
        tooltip=['timestamp:T', 'temperature']
    ).properties(
        title="Biến động nhiệt độ theo thời gian",
        width=800,
        height=300
    )

    st.altair_chart(chart_temp, use_container_width=True)

    # Vẽ độ ẩm
    chart_humid = alt.Chart(df).mark_line(color="blue").encode(
        x=alt.X('timestamp:T', title='Thời gian'),
        y=alt.Y('humidity:Q', title='Độ ẩm (%)'),
        tooltip=['timestamp:T', 'humidity']
    ).properties(
        title="Biến động độ ẩm theo thời gian",
        width=800,
        height=300
    )

    st.altair_chart(chart_humid, use_container_width=True)

else:
    st.error("❌ Không tìm thấy cột 'timestamp' trong dữ liệu!")

# Bảng dữ liệu
st.subheader("📄 Dữ liệu ghi nhận gần đây")
st.dataframe(df[::-1])
