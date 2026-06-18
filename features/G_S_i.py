import psutil
import GPUtil
import requests

# تعریف آی‌پی بیرون از تابع به عنوان حافظه موقت (Cache)
_saved_ip = None

def get_SI():    
    global _saved_ip
    try:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        
        gpu = 0
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = int(gpus[0].load * 100)
        except Exception:
            gpu = 0
            
        # فقط اگر آی‌پی را نداشتیم درخواست وب بفرست
        if _saved_ip is None or _saved_ip == "CONNECTION ERROR":
            try:
                _saved_ip = requests.get("https://api.ipify.org", timeout=2).text
            except Exception:
                _saved_ip = "CONNECTION ERROR"
            
        system_data = {
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "gpu": gpu,
            "ip": _saved_ip
        }
        return system_data
        
    except Exception as e:
        print(f"Error in get_SI: {e}")
        return None