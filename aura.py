# Imports   
import subprocess
import time
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import pyautogui
from googlesearch import search
from openai import OpenAI
import os
import winreg
 
client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        print("Good Morning!")
        

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
        print("Good Afternoon!")  
    else:
        speak("Good Evening!")  
        print("Good Evening!")  
    speak("I am Aura Sir. Please tell me how may I help you")         
    print("I am Aura Sir. Please tell me how may I help you")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User Input: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def open_calculator():
    try:
        # Assuming the calculator is in the default Windows location
        subprocess.run("calc.exe", check=True)
        speak("Opening the calculator.")
    except Exception as e:
        speak(f"Sorry, there was an error: {e}")


def evaluate_math_expression(expression):
    try:
        result = eval(expression)
        print(result)
        return result
    except Exception as e:
        print(e)
        return None

def get_installed_software():
    software_list = []
    uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    reg_key = winreg.HKEY_LOCAL_MACHINE
    try:
        with winreg.OpenKey(reg_key, uninstall_key) as key:
            for i in range(1024):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey_path = os.path.join(uninstall_key, subkey_name)
                    with winreg.OpenKey(reg_key, subkey_path) as subkey:
                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        install_location, _ = winreg.QueryValueEx(subkey, "InstallLocation")
                        if display_name and install_location:
                            software_list.append((display_name, install_location))
                except WindowsError:
                    pass
    except Exception as e:
        print(f"Error: {e}")
    return software_list


if __name__ == "__main__":
    wishMe()
    installed_software = get_installed_software()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'open' in query or 'run' in query:
            open_command(query)

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'chatgpt' in query or "chat gpt" in query:
            while True: 
                message = query.replace("chatgpt", "")
                chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=message ) 
                reply = chat.choices[0].message.content 
                print(f"AURA: {reply}") 
        
        elif 'open google' in query:
            webbrowser.open("google.com")
        
        elif 'google' in query:
            query = query.replace("google", "")
            query = query.replace("search about", "")
            query = query.replace("on", "")
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
            print(f"Searching Google for: {query}")

        elif 'open stackoverflow' in query or "open stack overflow" in query:
            webbrowser.open("stackoverflow.com")  

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")  

        elif 'list music' in query:
            music_dir = 'C:\\Users\\wadhi\\Music'
            songs = os.listdir(music_dir)
            for s in songs:
                print(s)      

        elif 'current time' in query or 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  
            print(f"Sir, the time is {strTime}")  
            speak(f"Sir, the time is {strTime}")

        elif 'open vscode' in query or 'vs code' in query:
            codePath = "C:\\Users\\wadhi\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to me' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "wadhiabhavesh@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")      
        
        elif 'open calculator' in query:
            try:
                # Assuming the calculator is in the default Windows location
                subprocess.run("calc.exe", check=True)
                speak("Opening the calculator.")
                time.sleep(2)
                """-
                pyautogui.write()
                pyautogui.press('enter')
                time.sleep(1)
                result = pyautogui.getClipboardData()
                speak(f"The result is {result}")
                """
            except Exception as e:
                print(e)
                speak(f"Sorry, there was an error")
        
        
        elif 'calculate' in query or 'evaluate' in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Sure, please tell me the mathematical expression.")
                speak("Sure, please tell me the mathematical expression.")
                r.pause_threshold = 1
                audio = r.listen(source)
            try:
                print("Recognizing...")    
                expression = r.recognize_google(audio, language='en-in')
                print(f"User Expression: {expression}\n")
                result = evaluate_math_expression(expression)
            except:
                if result is not None:
                    speak(f"The result is {result}")
                    print(f"The result is {result}")
                else:
                    speak("Sorry, I couldn't evaluate the expression.")

        """elif 'open chatgpt' in query or "open chat gpt":
            print("Opening Chat GPT")
            webbrowser.open("chat.openai.com")
        """
