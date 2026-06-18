import re
import requests

def get_price():
    try:
        # درخواست به سایت برای گرفتن قیمت‌های لحظه‌ای
        res = requests.get("https://www.tgju.org/", timeout=5)
        tag1 = re.findall('<span class="info-price">(.*)</span>', res.text)
        
        # ذخیره دیتای تمیز شده در یک دیکشنری
        data = {
            "gold": tag1[3],
            "coin": tag1[4],
            "dollar": tag1[5]
        }
        return data
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None