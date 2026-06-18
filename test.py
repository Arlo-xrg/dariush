import sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

from UI.ui import JarvisYellowUI

from features.site_control import run_command
from features.temperature import get_weather
from listening import listen
from speak import speak
from features.Global_price import get_price  
from features.G_S_i import get_SI          
from features.translator import transletor

# ================= ترد اختصاصی پردازش صوتی =================
class JarvisVoiceThread(QThread):
    command_detected = pyqtSignal(str)
    status_updated = pyqtSignal(str)
    prices_updated = pyqtSignal(dict)  
    close_program = pyqtSignal()  
    translation_rendered = pyqtSignal(str) #

    def run(self):
       
        self.status_updated.emit("LISTENING...")
        speak("hi sir")
        while True:
            order = listen()
            if order is not None:
                self.command_detected.emit(order)
                
                # _________________________say_hi________________________
                if "سلام" in order:
                    self.status_updated.emit("SPEAKING...")
                    speak("hi sir how are you what can i do for you")
                    self.status_updated.emit("LISTENING...")
                    
                # _________________________open_SMT_____________________
                elif "باز" in order:
                    self.status_updated.emit("EXECUTING...")
                    run_command(order)
                    self.status_updated.emit("LISTENING...")
                    
                # _________________________Price_________________________
                elif "قیمت" in order:
                    self.status_updated.emit("FETCHING PRICES...")
                    live_prices = get_price() 
                    if live_prices:
                        self.prices_updated.emit(live_prices)
                        speak("prices updated successfully, sir")
                    else:
                        speak("failed to fetch prices")
                    self.status_updated.emit("LISTENING...")
                    
                # _________________________Translate_____________________
                elif "ترجمه" in order:
                    self.status_updated.emit("TRANSLATOR ACTIVE")
                    speak("say your sentence")
                    while True: 
                        order = listen()
                        if order is not None:
                            if order == "خارج شو":
                                break
                            else:
                                # نمایش متن در حال پردازش در UI
                                self.command_detected.emit(order)
                                tr = transletor(order)
                                
                                # پرتاب متن ترجمه شده به لایه گرافیکی
                                self.translation_rendered.emit(tr)
                                break
                    # بعد از اتمام ترجمه، یک مقدار تاخیر یا بازگشت به حالت شنیدن
                    self.status_updated.emit("LISTENING...")
                    
                # ________________________finish_________________________
                elif "پایان" in order:
                    self.status_updated.emit("OFFLINE")
                    speak("thank you sir, shutting down")
                    self.close_program.emit()  
                    break

# ================= کنترلر نهایی برنامه‌ =================
class JarvisController:
    
    def __init__(self):
        self.ui = JarvisYellowUI()
        self.cached_ip = None        
        self.start_voice_assistant()
        self.setup_live_monitoring() 
        
        self.load_weather_once() 
        self.load_prices_once()
        
        self.ui.show()

    def start_voice_assistant(self):
        self.voice_thread = JarvisVoiceThread()
        self.voice_thread.status_updated.connect(self.ui.status_txt.setText)
        self.voice_thread.command_detected.connect(self.ui.command_input.setText)
        self.voice_thread.prices_updated.connect(self.update_prices_on_hud)
        self.voice_thread.close_program.connect(self.ui.close)
        
        # 🔗 متصل کردن سیگنال متنی ترجمه به متد نمایش روی مانیتور
        self.voice_thread.translation_rendered.connect(self.show_translation_on_hud)
        
        self.voice_thread.start()

    def setup_live_monitoring(self):
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_hardware_live)
        self.stats_timer.start(2000) 
        self.update_hardware_live()

    def load_weather_once(self):
        weather_data = get_weather("Babol")
        if weather_data:
            self.ui.lbl_city.setText(f"📍 CITY        : {weather_data['city']}")
            self.ui.lbl_temp.setText(f"🌡️ TEMPERATURE : {weather_data['temp']}")
            self.ui.lbl_humidity.setText(f"💧 HUMIDITY    : {weather_data['humidity']}")
            self.ui.lbl_condition.setText(f"☀️ CONDITION   : {weather_data['condition']}")
        else:
            self.ui.lbl_condition.setText("☀️ CONDITION   : ERROR FETCHING")

    def load_prices_once(self):
        initial_prices = get_price()
        if initial_prices:
            self.update_prices_on_hud(initial_prices)   

    # 🎯 متد جدید برای نوشتن متن ترجمه شده در کادر وضعیت پایین هسته مرکزی
    def show_translation_on_hud(self, text):
        self.ui.status_txt.setText("TRANSLATED:")
        self.ui.command_input.setText(text)

    def update_hardware_live(self):
        sys_dict = get_SI()
        if sys_dict:
            self.ui.bars["CPU USAGE"][0].setText(f"CPU USAGE: {sys_dict['cpu']}%")
            self.ui.bars["CPU USAGE"][1].setValue(int(sys_dict['cpu']))
            
            self.ui.bars["RAM UTILIZATION"][0].setText(f"RAM UTILIZATION: {sys_dict['ram']}%")
            self.ui.bars["RAM UTILIZATION"][1].setValue(int(sys_dict['ram']))
            
            self.ui.bars["DISK STORAGE"][0].setText(f"DISK STORAGE: {sys_dict['disk']}%")
            self.ui.bars["DISK STORAGE"][1].setValue(int(sys_dict['disk']))
            
            self.ui.bars["GPU USAGE"][0].setText(f"GPU USAGE: {sys_dict['gpu']}%")
            self.ui.bars["GPU USAGE"][1].setValue(int(sys_dict['gpu']))
            
            if self.cached_ip is None or self.cached_ip == "CONNECTION ERROR":
                self.cached_ip = sys_dict['ip']
            
            for widget in self.ui.findChildren(QLabel):
                if "NETWORK IP:" in widget.text():
                    widget.setText(f"NETWORK IP: {self.cached_ip}")
                    break

    def update_prices_on_hud(self, price_dict):
        self.ui.lbl_gold.setText(f"🏆 GOLD OUNCE : {price_dict['gold']}")
        self.ui.lbl_coin.setText(f"🪙 CRYPTO COIN: {price_dict['coin']}")
        self.ui.lbl_dollar.setText(f"💵 USD INDEX  : {price_dict['dollar']}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = JarvisController()
    sys.exit(app.exec())