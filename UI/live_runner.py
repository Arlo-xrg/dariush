# live_runner.py
import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# اگر کتابخانه watchdog را نداری، در ترمینال بزن: pip install watchdog
# این کتابخانه تغییرات فایل‌ها را حس می‌کند

class UIChangeHandler(FileSystemEventHandler):
    def __init__(self, script_to_run):
        self.script_to_run = script_to_run
        self.process = None
        self.start_process()

    def start_process(self):
        """اجرای فایل UI"""
        if self.process:
            self.process.terminate() # بستن پنجره قبلی
        print("⚡ [LIVE] Reloading UI with new modifications...")
        # اجرای فایل ui.py
        self.process = subprocess.Popen([sys.executable, self.script_to_run])

    def on_modified(self, event):
        # اگر خود فایل ui.py تغییر کرد، پروسه را ریستارت کن
        if event.src_path.endswith("ui.py"):
            # یک تاخیر کوچک برای اینکه فایل کاملا ذخیره شود
            time.sleep(0.2)
            self.start_process()

if __name__ == "__main__":
    TARGET_SCRIPT = "ui.py" # اسمی فایلی که می‌خواهی زنده تغییرش دهی
    
    if not os.path.exists(TARGET_SCRIPT):
        # ساخت یک فایل ui اولیه اگر وجود نداشته باشد
        with open(TARGET_SCRIPT, "w", encoding="utf-8") as f:
            f.write("# بدنه اولیه فایل ui")

    event_handler = UIChangeHandler(TARGET_SCRIPT)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    print(f"👀 Live Reloading active. Modify '{TARGET_SCRIPT}' and save to see changes live!")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()