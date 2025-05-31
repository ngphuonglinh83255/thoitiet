import requests, json, os
from datetime import datetime

API_KEY = "b23631c8788d754ca739ac72ec55aa9c"
CITY = "Hanoi"

def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        print("⚠️ Không lấy được dữ liệu")
        return

    weather = res.json()
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": weather["main"]["temp"],
        "humidity": weather["main"]["humidity"]
    }

    with open("weather_log.json", "a") as f:  # mở file ở chế độ thêm
        f.write(json.dumps(record) + "\n")     # ghi mỗi dòng là 1 object

if __name__ == "__main__":
    fetch_weather()
