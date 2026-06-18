import requests

API_KEY = "809d645cd50c43a4b0c101505240611"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(city_name="Tehran"):
    url = f"{BASE_URL}?key={API_KEY}&q={city_name}&aqi=no"
    try:
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            data = response.json()
            location = data['location']
            current = data['current']
            
            # بازگرداندن داده‌ها در قالب دیکشنری تمیز
            return {
                "city": f"{location['name']}, {location['country']}",
                "temp": f"{current['temp_c']}°C",
                "humidity": f"{current['humidity']}%",
                "condition": current['condition']['text'].upper()
            }
        else:
            return None
    except Exception:
        return None