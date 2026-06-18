import sys
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
                             QLabel, QLineEdit, QProgressBar)
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QRadialGradient, QFont

# ================= ویجت پیشرفته و متحرک هسته مرکزی =================
class JarvisAnimatedCore(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 320)
        
        self.angle_layer1 = 0.0
        self.angle_layer2 = 0.0
        self.angle_layer3 = 0.0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16) 
        
    def update_animation(self):
        self.angle_layer1 += 0.8  
        self.angle_layer2 -= 1.4  
        self.angle_layer3 += 2.0  
        
        if self.angle_layer1 >= 360: self.angle_layer1 -= 360
        if self.angle_layer2 <= -360: self.angle_layer2 += 360
        if self.angle_layer3 >= 360: self.angle_layer3 -= 360
        
        self.update() 
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        base_radius = 110 
        
        glow_grad = QRadialGradient(center_x, center_y, base_radius + 30)
        glow_grad.setColorAt(0.0, QColor(241, 196, 15, 45))  
        glow_grad.setColorAt(0.5, QColor(212, 175, 55, 15)) 
        glow_grad.setColorAt(1.0, QColor(0, 0, 0, 0))        
        painter.setBrush(glow_grad)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(center_x - (base_radius+30)), int(center_y - (base_radius+30)), 
                            int((base_radius+30)*2), int((base_radius+30)*2))
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen_static = QPen(QColor(241, 196, 15, 80), 1)
        painter.setPen(pen_static)
        
        painter.drawLine(int(center_x), int(center_y - base_radius - 25), int(center_x), int(center_y - base_radius - 5))
        painter.drawLine(int(center_x), int(center_y + base_radius + 5), int(center_x), int(center_y + base_radius + 25))
        painter.drawLine(int(center_x - base_radius - 25), int(center_y), int(center_x - base_radius - 5), int(center_y))
        painter.drawLine(int(center_x + base_radius + 5), int(center_y), int(center_x + base_radius + 25), int(center_y))
        
        offset = base_radius + 15
        painter.drawArc(QRectF(center_x - offset, center_y - offset, offset*2, offset*2), 45*16, 10*16)
        painter.drawArc(QRectF(center_x - offset, center_y - offset, offset*2, offset*2), 135*16, 10*16)
        painter.drawArc(QRectF(center_x - offset, center_y - offset, offset*2, offset*2), 225*16, 10*16)
        painter.drawArc(QRectF(center_x - offset, center_y - offset, offset*2, offset*2), 315*16, 10*16)

        # لایه متحرک ۱
        painter.save() 
        painter.translate(center_x, center_y)
        painter.rotate(self.angle_layer1)
        pen_l1 = QPen(QColor("#f1c40f"), 2)
        pen_l1.setDashPattern([15, 10, 5, 10]) 
        painter.setPen(pen_l1)
        painter.drawEllipse(QRectF(-base_radius, -base_radius, base_radius*2, base_radius*2))
        painter.setBrush(QColor("#ffcc00"))
        painter.drawEllipse(int(-4), int(-base_radius-2), 8, 4)
        painter.drawEllipse(int(-4), int(base_radius-2), 8, 4)
        painter.restore() 

        # لایه متحرک ۲
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle_layer2)
        r_mid = base_radius * 0.75
        pen_l2 = QPen(QColor("#ffcc00"), 1, Qt.PenStyle.DashLine)
        painter.setPen(pen_l2)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QRectF(-r_mid, -r_mid, r_mid*2, r_mid*2))
        pen_arc = QPen(QColor("#f1c40f"), 3)
        painter.setPen(pen_arc)
        painter.drawArc(QRectF(-r_mid, -r_mid, r_mid*2, r_mid*2), 0, 60*16)
        painter.drawArc(QRectF(-r_mid, -r_mid, r_mid*2, r_mid*2), 180*16, 60*16)
        painter.restore()

        # لایه متحرک ۳
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle_layer3)
        r_core = base_radius * 0.4
        pen_l3 = QPen(QColor("#ffffff"), 1.5)
        pen_l3.setDashPattern([4, 4])
        painter.setPen(pen_l3)
        painter.drawEllipse(QRectF(-r_core, -r_core, r_core*2, r_core*2))
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(-5, -5, 10, 10)
        painter.restore()
        
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        painter.drawText(QRectF(0, 0, width, height), Qt.AlignmentFlag.AlignCenter, "CORE\nON")


# ================= پنجره اصلی ظاهری UI =================
class JarvisYellowUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('𝙅𝘼𝙍𝙑𝙅𝙎 𝙊𝙎 : 𝘼𝙉𝙅𝙈𝘼𝙏𝙀𝘿 𝘾𝙊𝙍执行')
        self.resize(1250, 780) 
        self.setStyleSheet("background-color: #050508;")
        
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        main_box_style = "QFrame { background-color: #16161c; border: 2px solid #f1c40f; border-radius: 14px; }"
        inner_box_style = "QFrame { background-color: #0d0d12; border: 1px solid #ffcc00; border-radius: 10px; } QLabel { border: none; background: transparent; }"
        header_style = "color: #f1c40f; font-family: 'Consolas'; font-weight: bold; font-size: 14px; letter-spacing: 2px; border: none;"
        data_text_style = "color: #e0e0e6; font-family: 'Consolas'; font-size: 12px; border: none;"
        
        # ================= ۱. ستون سمت چپ =================
        left_main_box = QFrame()
        left_main_box.setStyleSheet(main_box_style)
        left_layout = QVBoxLayout(left_main_box)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(15, 20, 15, 20)
        
        left_inner1 = QFrame()
        left_inner1.setStyleSheet(inner_box_style)
        left_inner1_layout = QVBoxLayout(left_inner1)
        left_inner1_layout.setSpacing(12)
        left_inner1_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_env = QLabel("┌── SYSTEM CORE ──┐")
        lbl_env.setStyleSheet(header_style)
        lbl_env.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_inner1_layout.addWidget(lbl_env)
        
        self.bars = {}
        for name, val in [("CPU USAGE", 24), ("GPU USAGE", 18), ("RAM UTILIZATION", 45), ("DISK STORAGE", 62)]:
            lay = QVBoxLayout()
            lbl = QLabel(f"{name}: {val}%")
            lbl.setStyleSheet(data_text_style)
            bar = QProgressBar()
            bar.setValue(val)
            bar.setTextVisible(False)
            bar.setFixedHeight(5)
            bar.setStyleSheet("QProgressBar { background-color: #050508; border: none; } QProgressBar::chunk { background-color: #f1c40f; }")
            lay.addWidget(lbl)
            lay.addWidget(bar)
            left_inner1_layout.addLayout(lay)
            self.bars[name] = (lbl, bar)
            
        lbl_ip = QLabel("NETWORK IP: 192.168.1.5")
        lbl_ip.setStyleSheet("color: #ffcc00; font-family: 'Consolas'; font-size: 12px; margin-top: 5px;")
        left_inner1_layout.addWidget(lbl_ip)
        
        left_inner2 = QFrame()
        left_inner2.setStyleSheet(inner_box_style)
        left_inner2_layout = QVBoxLayout(left_inner2)
        left_inner2_layout.setSpacing(12)
        left_inner2_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_market = QLabel("┌── ASSETS INDEX ──┐")
        lbl_market.setStyleSheet(header_style)
        lbl_market.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_inner2_layout.addWidget(lbl_market)
        
        self.lbl_gold = QLabel("🏆 GOLD OUNCE : 0")
        self.lbl_gold.setStyleSheet("color: #ffcc00; font-family: 'Consolas'; font-size: 12px; font-weight: bold;")
        self.lbl_coin = QLabel("🪙 CRYPTO COIN: 0")
        self.lbl_coin.setStyleSheet(data_text_style)
        self.lbl_dollar = QLabel("💵 USD INDEX  : 0")
        self.lbl_dollar.setStyleSheet(data_text_style)
        
        left_inner2_layout.addWidget(self.lbl_gold)
        left_inner2_layout.addWidget(self.lbl_coin)
        left_inner2_layout.addWidget(self.lbl_dollar)
        
        left_layout.addWidget(left_inner1, stretch=5) 
        left_layout.addWidget(left_inner2, stretch=3)
        
        # ================= ۲. ستون وسط =================
        center_main_box = QFrame()
        center_main_box.setStyleSheet(main_box_style)
        center_layout = QVBoxLayout(center_main_box)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(15)
        
        self.jarvis_core = JarvisAnimatedCore()
        
        center_bottom_inner_box = QFrame()
        center_bottom_inner_box.setStyleSheet(inner_box_style)
        bottom_layout = QHBoxLayout(center_bottom_inner_box)
        bottom_layout.setContentsMargins(20, 12, 20, 12)
        bottom_layout.setSpacing(15)
        
        self.status_txt = QLabel("AWAITING:")
        self.status_txt.setStyleSheet("color: #555566; font-family: 'Consolas'; font-size: 11px; font-weight: bold;")
        
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter neural command here...")
        self.command_input.setStyleSheet("background-color: #050508; color: #ffcc00; border: 1px solid #f1c40f; padding: 6px; font-family: 'Consolas';")
        
        bottom_layout.addWidget(self.status_txt)
        bottom_layout.addWidget(self.command_input, stretch=1)
        
        center_layout.addWidget(self.jarvis_core, stretch=6) 
        center_layout.addWidget(center_bottom_inner_box, stretch=1)
        
       # ================= ۳. ستون سمت راست (جایگزین این بخش در jarvis_ui.py) =================
        right_main_box = QFrame()
        right_main_box.setStyleSheet(main_box_style)
        right_layout = QVBoxLayout(right_main_box)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(15, 20, 15, 20)
        
        right_inner1 = QFrame()
        right_inner1.setStyleSheet(inner_box_style)
        right_inner1_layout = QVBoxLayout(right_inner1)
        right_inner1_layout.setSpacing(12)
        right_inner1_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_weather_hd = QLabel("┌── WEATHER HUD ──┐")
        lbl_weather_hd.setStyleSheet(header_style)
        lbl_weather_hd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_inner1_layout.addWidget(lbl_weather_hd)
        
        # تعریف متغیر برای لیبل‌ها جهت تغییر داینامیک
        self.lbl_city = QLabel("📍 CITY: Babol")
        self.lbl_city.setStyleSheet("color: #ffcc00; font-family: 'Consolas'; font-size: 12px; font-weight: bold;")
        self.lbl_temp = QLabel("🌡️ TEMPERATURE : --°C")
        self.lbl_temp.setStyleSheet(data_text_style)
        self.lbl_humidity = QLabel("💧 HUMIDITY    : --%")
        self.lbl_humidity.setStyleSheet(data_text_style)
        self.lbl_condition = QLabel("☀️ CONDITION   : LOADING...")
        self.lbl_condition.setStyleSheet(data_text_style)
        
        right_inner1_layout.addWidget(self.lbl_city)
        right_inner1_layout.addWidget(self.lbl_temp)
        right_inner1_layout.addWidget(self.lbl_humidity)
        right_inner1_layout.addWidget(self.lbl_condition)
        
        right_inner2 = QFrame()
        right_inner2.setStyleSheet(inner_box_style)
        right_inner2_layout = QVBoxLayout(right_inner2)
        right_inner2_layout.setContentsMargins(10, 10, 10, 10)
        
        lbl_music_hd = QLabel("🎵 NOW PLAYING")
        lbl_music_hd.setStyleSheet("color: #555566; font-family: 'Consolas'; font-size: 11px; font-weight: bold;")
        lbl_music_hd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_track = QLabel("Synthwave Mix.mp3\n ◀  𝚰𝚰  ▶ ")
        lbl_track.setStyleSheet("color: #ffcc00; font-family: 'Consolas'; font-size: 12px; font-weight: bold;")
        lbl_track.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        right_inner2_layout.addWidget(lbl_music_hd)
        right_inner2_layout.addWidget(lbl_track)
        
        right_layout.addWidget(right_inner1, stretch=4)
        right_layout.addWidget(right_inner2, stretch=2)
        
        lbl_music_hd = QLabel("🎵 NOW PLAYING")
        lbl_music_hd.setStyleSheet("color: #555566; font-family: 'Consolas'; font-size: 11px; font-weight: bold;")
        lbl_music_hd.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_track = QLabel("Synthwave Mix.mp3\n ◀  𝚰𝚰  ▶ ")
        lbl_track.setStyleSheet("color: #ffcc00; font-family: 'Consolas'; font-size: 12px; font-weight: bold;")
        lbl_track.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        right_inner2_layout.addWidget(lbl_music_hd)
        right_inner2_layout.addWidget(lbl_track)
        
        right_layout.addWidget(right_inner1, stretch=4)
        right_layout.addWidget(right_inner2, stretch=2)
        
        main_layout.addWidget(left_main_box, stretch=1)
        main_layout.addWidget(center_main_box, stretch=4)
        main_layout.addWidget(right_main_box, stretch=1)