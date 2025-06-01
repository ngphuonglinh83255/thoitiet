import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

API_KEY = "b23631c8788d754ca739ac72ec55aa9c"
CITIES = ["Ha Noi", "Ho Chi Minh", "Da Nang", "Haiphong", "Can Tho"]

@st.cache_data(ttl=900)  # cache dữ liệu 15 phút để hạn chế gọi API quá nhiều
def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},VN&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize(),
        "time": datetime.now()
    }

def main():
    st.title("🌦️ Dashboard Giám sát Thời tiết Việt Nam")

    # Tự động refresh trang sau mỗi 15 phút (900000 ms)
    st_autorefresh(interval=900_000, key="refresh")

    selected_cities = st.multiselect("Chọn thành phố để xem thông tin thời tiết:", CITIES, default=CITIES)

    if not selected_cities:
        st.warning("Vui lòng chọn ít nhất 1 thành phố.")
        return

    # Lấy dữ liệu mới cho các thành phố đã chọn
    new_data = []
    for city in selected_cities:
        weather = fetch_weather(city)
        if weather:
            new_data.append(weather)
        else:
            st.error(f"Không lấy được dữ liệu cho thành phố: {city}")

    if not new_data:
        st.error("Không có dữ liệu thời tiết để hiển thị.")
        return

    # Đọc dữ liệu lịch sử từ file csv (nếu có)
    try:
        df_history = pd.read_csv("weather_history.csv", parse_dates=["time"])
    except FileNotFoundError:
        df_history = pd.DataFrame(columns=["city", "temperature", "humidity", "description", "time"])

    # Thêm dữ liệu mới vào lịch sử
    df_new = pd.DataFrame(new_data)
    df_history = pd.concat([df_history, df_new], ignore_index=True)

    # Giữ lại dữ liệu lịch sử trong khoảng 24 giờ
    cutoff_time = datetime.now() - pd.Timedelta(hours=24)
    df_history = df_history[df_history["time"] >= cutoff_time]

    # Lưu lại dữ liệu lịch sử
    df_history.to_csv("weather_history.csv", index=False)

    # Hiển thị bảng dữ liệu thời tiết hiện tại
    st.subheader("Bảng dữ liệu thời tiết hiện tại")
    df_display = df_new[["city", "temperature", "humidity", "description", "time"]].copy()
    df_display["time"] = df_display["time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    st.dataframe(df_display.set_index("city"))

    # Lọc dữ liệu lịch sử theo các thành phố được chọn
    df_filtered = df_history[df_history["city"].isin(selected_cities)].copy()
    df_filtered.sort_values(by="time", inplace=True)

    # Vẽ biểu đồ đường Nhiệt độ theo thời gian với đường cong spline
    fig_temp = px.line(
        df_filtered,
        x="time",
        y="temperature",
        color="city",
        title="Biểu đồ đường Nhiệt độ theo thời gian",
        labels={"time": "Thời gian", "temperature": "Nhiệt độ (°C)", "city": "Thành phố"},
        markers=True,
        line_shape='spline'
    )
    fig_temp.update_layout(xaxis=dict(tickformat="%H:%M:%S\n%b %d"))
    st.plotly_chart(fig_temp, use_container_width=True)

    # Vẽ biểu đồ đường Độ ẩm theo thời gian với đường cong spline
    fig_humidity = px.line(
        df_filtered,
        x="time",
        y="humidity",
        color="city",
        title="Biểu đồ đường Độ ẩm theo thời gian",
        labels={"time": "Thời gian", "humidity": "Độ ẩm (%)", "city": "Thành phố"},
        markers=True,
        line_shape='spline'
    )
    fig_humidity.update_layout(xaxis=dict(tickformat="%H:%M:%S\n%b %d"))
    st.plotly_chart(fig_humidity, use_container_width=True)

if __name__ == "__main__":
    main()
