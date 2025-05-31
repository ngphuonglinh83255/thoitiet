import streamlit as st
import pandas as pd
import json
import altair as alt
import os

st.set_page_config(page_title="Giám sát thời tiết", layout="wide")
st.title("🌦️ Dashboard Giám sát Thời tiết Việt Nam")

# 🟨 Load dữ liệu từ file JSON
def load_data():
    if not os.path.exists("weather_log.json"):
        # Trả về DataFrame rỗng nếu file chưa có
        return pd.DataFrame()
    with open("weather_log.json", encoding="utf-8") as f:
        lines = f.readlines()
        records = [json.loads(line) for line in lines if line.strip()]
        return pd.DataFrame(records)


df = load_data()

# ✅ Chuẩn hóa tên thành phố
city_mapping = {
    "Hanoi": "Ha Noi",
    "Ha Noi": "Ha Noi",
    "Ho Chi Minh City": "Ho Chi Minh",
    "TP. Ho Chi Minh": "Ho Chi Minh",
    "HoChiMinh": "Ho Chi Minh"
}
df["city"] = df["city"].replace(city_mapping)

# ⏱️ Xử lý thời gian
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

# 🗺️ Chọn tỉnh/thành phố để phân tích
if not df.empty:
    selected_city = st.selectbox("🗺️ Chọn tỉnh/thành phố", sorted(df['city'].dropna().unique()))

    city_data = df[df['city'] == selected_city]

    # 🚨 Cảnh báo nhiệt độ/độ ẩm
    st.subheader(f"🚨 Cảnh báo thời tiết hiện tại tại {selected_city}")
    latest = city_data.iloc[-1]
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

    # 📈 Biểu đồ thời gian mượt
    st.subheader("📊 Biểu đồ thời tiết theo thời gian")

    line_temp = alt.Chart(city_data).mark_line(interpolate='monotone', color='red').encode(
        x=alt.X('timestamp:T', title='Thời gian'),
        y=alt.Y('temperature:Q', title='Nhiệt độ (°C)'),
        tooltip=['timestamp:T', 'temperature']
    ).properties(
        title=f"Biến động nhiệt độ tại {selected_city}",
        width=800,
        height=300
    )

    line_humidity = alt.Chart(city_data).mark_line(interpolate='monotone', color='blue').encode(
        x=alt.X('timestamp:T', title='Thời gian'),
        y=alt.Y('humidity:Q', title='Độ ẩm (%)'),
        tooltip=['timestamp:T', 'humidity']
    ).properties(
        title=f"Biến động độ ẩm tại {selected_city}",
        width=800,
        height=300
    )

    st.altair_chart(line_temp, use_container_width=True)
    st.altair_chart(line_humidity, use_container_width=True)

    # 📄 Bảng dữ liệu
    st.subheader("📋 Dữ liệu ghi nhận")
    st.dataframe(city_data[::-1])
else:
    st.warning("⚠️ Không có dữ liệu để hiển thị.")
