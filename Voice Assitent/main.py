import os
import time
import pyttsx3 as x3
import speech_recognition as sr
from Commands import *
import random
import re
import webbrowser
import wikipedia
import json
import request
from datetime import datetime
#Settings of Voice
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
engine = x3.init()
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)



#All Assistent'opportunities
class Time():
    def __init__(self):
        self.engine = x3.init()
        self.now = datetime.now()
        self.engine.say(random.choice(Phrases_after_Actions))
        self.time_now = self.now.strftime("%d %B, %A, %H Hours %M Minutes,  %Y ")
        print(self.time_now)
        self.engine.say(self.time_now)
        self.engine.runAndWait() 


class System():
    def __init__(self):
        self.Chrome = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        self.cmd = 'C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/System Tools/cmd.exe'
        self.Telegram = "C:/Users/LENOVO/AppData/Roaming/Telegram Desktop/Telegram.exe"
        self.HoneyPot = 'C:/Users/LENOVO/Desktop/Win_Locker/dist/main.exe'
        self.Desktop = 'C:/Users/LENOVO/Desktop'
        self.Vs = "C:/Program Files/Microsoft VS Code/Code.exe"
    def AppMannager(self):
        self.engine = x3.init()
        self.ask = Answer
        print(self.ask)
        self.engine.say(random.choice(Phrases_after_Actions))
        time.sleep(1)
        if self.ask == "open telegram":
            os.startfile(self.Telegram)
        elif self.ask == "open browser":
            os.startfile(self.Chrome)
        elif self.ask == "open cmd":
            os.startfile(self.cmd)
        elif self.ask == "open honeypot":
            os.startfile(self.HoneyPot)
        elif self.ask == "open visual studio":
            os.startfile(self.Vs)
  
        
class Web():
    def __init__(self):
        self.url = Answer
        self.new_list = ''
    def OpenUrl(self):
        self.url = list(str(self.url))
        self.engine = x3.init()
        for i in self.url:
            if i == ' ':
                self.new_list = ''
            self.new_list+=i
        self.url = self.new_list.strip()
        print(self.url)
        self.engine.say(random.choice(Phrases_after_Actions))
        time.sleep(1)
        if re.search(r'\.', self.url):
            webbrowser.open_new_tab('https://' + self.url)  
        elif re.search(r'\ ', self.url):
            webbrowser.open_new_tab('https://www.google.com/search?=&ei=&q=bu'+ self.url +'&oq=')
        else:
            webbrowser.open_new_tab('https://www.google.com/search?=&ei=&q='+ self.url +'&oq=')



class WikiPedia():
    def __init__(self):
        self.Question = Answer
        self.Wiki_Request =  wikipedia.summary(self.Question, sentences=random.randint(2,4))
        self.New_list = list(str(self.Wiki_Request))
        self.count = 0
        
    def Wiki_Search(self):
        self.engine = x3.init()
        for i in self.New_list:
            if i == '.':
                self.count += 1
        self.engine.say(random.choice(Phrases_after_Actions))
        self.Wiki_Request = self.Wiki_Request.replace('.','\n',self.count)
        print(self.Wiki_Request)
        self.engine.say(self.Wiki_Request)
    

class BoringStuff():
    def __init__(self):
        self.music_directory = 'C:/Users/LENOVO/Downloads/MUSIC/'
        self.random_music_id = random.randint(1,14) 
        self.command = Answer
    def Joke(self):
        self.engine = x3.init()
        self.engine.say(random.choice(Phrases_after_Actions))
        for i in Commands_Boring_Stuff:
            if self.command.startswith('tell me a joke'):
                self.joke = random.choice(Jokes)  
                self.engine.say(self.joke)
                self.command = ''
                
            if self.command.startswith(i):
                self.music_directory = self.music_directory + str(self.random_music_id) + '.mp3'
                os.startfile(self.music_directory)


        
                
#First request

def Greeting():
    engine = x3.init()
    engine.say('Hello, how can I help you, Sir?')
    engine.runAndWait()
    
Greeting()
Answer = 'a'

#Launch 
if __name__ == "__main__":
    while Answer != 'stop':
        with mic as source:
            r.adjust_for_ambient_noise(source)
            engine = x3.init()
            print('Command Please')
            engine.say("Command Please")
            engine.runAndWait()
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            Answer = query.lower()
            print(Answer)
        except sr.UnknownValueError:
            print("The voice wasn't recognized!")
            Answer = ''
            engine.say("The voice wasn't recognized!")
        except sr.RequestError as e:
            engine.say("[log] Undefined Error,Please check your Internet connection!")
        #Check the meaning in Massives from Commands.py
        def check_Meanings():
            for i in Commands_Time:
                if Answer == i:
                    Time()
            for i in Commands_System:
                if Answer == i:
                    system_1 = System()
                    system_1.AppMannager()
            for i in Commands_Wikipedia:
                if Answer.startswith(i):
                    print(Answer)
                    wiki_1 = WikiPedia()
                    wiki_1.Wiki_Search()
            for i in Commands_Boring_Stuff:
                if Answer.startswith(i):
                    bore_1 = BoringStuff()
                    bore_1.Joke()
            for i in Commands_Detection_System:
                if Answer.startswith(i):
                    os.startfile("/Detec/l.py")     
            if Answer.startswith('search'):
                web_1 = Web()
                web_1.OpenUrl()
             
        check_Meanings() 
    