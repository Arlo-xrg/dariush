import webbrowser
import subprocess
import os

# مسیر کروم
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "commands.txt")

command = {}

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        line = line.replace(",", "")

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().replace('"', '')
        value = value.strip().replace('"', '')

        command[key] = value


def clean_url(url):
    url = url.lower()

    for prefix in ["https://", "http://", "www."]:
        url = url.replace(prefix, "")

    url = url.split("/")[0]
    parts = url.split(".")

    return parts[0]


def open_in_chrome(url):
    try:
        if os.path.exists(CHROME_PATH):
            subprocess.Popen([CHROME_PATH, url])
        else:
            print("Chrome not found! Opening with default browser...")
            webbrowser.open(url)
    except Exception as e:
        print(f"Error opening URL: {e}")


def run_command(text):
    try:
        text = text.lower()

        for key, value in command.items():

            if key.lower() in text:

                # سایت
                if value.startswith(("http://", "https://")):
                    open_in_chrome(value)
                    return None

                # برنامه
                elif value.lower().endswith(".exe"):
                    subprocess.Popen(value, shell=True)
                    return None

                # دستور داخلی
                elif value.lower().endswith(".ord"):
                    return value

        return text

    except Exception as e:
        print(f"Error: {e}")
        return text
