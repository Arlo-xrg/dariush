from features.site_control import run_command
from features.temperature import get_weather
from listening import listen
from speak import speak
from features.Global_price import get_price
from features.G_S_i import get_SI
from features.translator import transletor
speak("hi sir")
while True :
    order = listen()
    if order != None:
        #_________________________say_hi________________________
        if "سلام" in order :
            speak("hi sir how are you what can i do for you")
        #_________________________open_SMT_____________________
        if "باز" in order:
            run_command(order)
        #_________________________Price_________________________
        elif "قیمت" in order :
            print("قیمت ها")
            get_price()
        #_________________________system_information____________
        elif "پردازش" in order :
            get_SI()
        #_________________________Translate_____________________
        if "ترجمه" in order :
            print("say your sentence :")
            while True : 
                order = listen()
                if order != None :
                    if order =="خارج شو":
                        print("break trasnlator")
                        break
                    else:
                        tr =transletor(order)
                        print(tr)
                        break
                
        #________________________finish_________________________
        elif order == "پایان":
            break
        

        
   
speak("thank you sir")
