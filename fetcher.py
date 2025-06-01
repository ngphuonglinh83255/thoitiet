import requests
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

API_KEY = "b23631c8788d754ca739ac72ec55aa9c"

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
        # 🔐 Kết nối Google Sheets
        creds = Credentials.from_service_account_file("weather-creds.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
        client = gspread.authorize(creds)

        # 📄 Mở sheet
        sheet = client.open("weather-data").sheet1

        # 📤 Ghi dữ liệu
        for record in records:
            row = [record["timestamp"], record["city"], record["temperature"], record["humidity"]]
            sheet.append_row(row)

        print("✅ Dữ liệu thời tiết đã được cập nhật lên Google Sheets.")
