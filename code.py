import speech_recognition as sr
import pyttsx3
import time


engine = pyttsx3.init()
#engine.setProperty('rate', 150)
engine.setProperty('voice', 'english+f1')

# Speech to Text conversion using google API
engine.say("Welcome to the Navigation assistant. Say help me to activate")
engine.runAndWait()


# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)  
    print("Say something!")
    audio = r.listen(source)
    input = r.recognize_google(audio, language = 'pt')
    if input == "help me":
        print (input)
        engine.say("activated")
        engine.runAndWait()
        time.sleep(1)
        engine.say("What do you want to find?")
        engine.runAndWait()
        query = r.listen(source)
        queryout = r.recognize_google(query)
        print(queryout)
        l = queryout.split()
        print(l[0][1])
        if l[0] == "find":
            print(l[1])
        else:
            print("exit")
                
        
    else:
        print("try again")
        print(input)
    
    
# try:
#     print(r.recognize_google(audio))
# except sr.UnknownValueError:
#     engine.say("Repeat")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))
