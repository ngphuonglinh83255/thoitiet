import requests, json, os
from datetime import datetime

API_KEY = "b23631c8788d754ca739ac72ec55aa9c"

# Danh sách các tỉnh/thành phố cần theo dõi
CITIES = ["Ha Noi", "Ho Chi Minh", "Da Nang", "Hai Phong", "Can Tho"]

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},VN&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"⚠️ Không lấy được dữ liệu cho {city}")
        return None

    weather = res.json()
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": city,
        "temperature": weather["main"]["temp"],
        "humidity": weather["main"]["humidity"]
    }

if __name__ == "__main__":
    records = []
    for city in CITIES:
        data = fetch_weather(city)
        if data:
            records.append(data)

    if records:
        with open("weather_log.json", "a", encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record) + "\n")

        print("✅ Dữ liệu thời tiết đã được cập nhật cho các tỉnh.")
