import threading
import time
import webview

# وارد کردن توابع اختصاصی خودت
from features.G_S_i import get_SI
from features.Global_price import get_price
from features.site_control import run_command
from features.temperature import get_weather
from features.translator import transletor
from listening import listen
from speak import speak as original_speak

jarvis_window = None


def ui_add_message(text, sender):

    global jarvis_window
    if jarvis_window:
        
        safe_text = text.replace("'", "\\'").replace("\n", " ")
        jarvis_window.evaluate_js(f"addUserMessage('{safe_text}', '{sender}');")


def speak(text):
    
    global jarvis_window
    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(true);")
        ui_add_message(text, 'jarvis')
    original_speak(text)

    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(false);")


def jarvis_core_logic():
    global jarvis_window

    time.sleep(3)
    speak("hi sir")

    while True:
        order = listen()
        if order is not None:
            print(order)
            ui_add_message(order, 'user')
            
            # _________________________say_hi________________________
            if "سلام" in order:
                speak("hi sir how are you what can i do for you")

            # _________________________open_SMT_____________________
            elif "باز" in order:
                run_command(order)

            # _________________________Price_________________________
            elif "قیمت" in order:
                print("قیمت ها")
                get_price()

            # _________________________system_information____________
            elif "پردازش" in order:
                get_SI()

            # _________________________Translate_____________________
            elif "ترجمه" in order:
                print("say your sentence :")
                while True:
                    order = listen()
                    if order is not None:
                        ui_add_message(order, 'user') 
                        if order == "خارج شو":
                            print("break translator")
                            break
                        else:
                            tr = transletor(order)
                            print(tr)
                            if tr: ui_add_message(f"Translation: {tr}", 'jarvis')
                            break

            # ________________________finish_________________________
            elif order == "پایان":
                break

    speak("thank you sir")
    if jarvis_window:
        jarvis_window.destroy()  


if __name__ == "__main__":
    jarvis_window = webview.create_window(
        title="JARVIS AI Core",
        url="UI/UI_v2/ui2.html",  
        width=1500,
        height=900,
        resizable=True,
        background_color="#000000",
    )

    threading.Thread(target=jarvis_core_logic, daemon=True).start()

    webview.start()
