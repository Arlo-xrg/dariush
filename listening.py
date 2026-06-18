import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print("Listen...")

def listen():
    try :
        with mic as source:
            audio = r.listen(source)

        text = r.recognize_google(audio, language="fa-IR")#fa-IR   en-US
        print( text)
        return text
    except:pass
