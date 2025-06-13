import re 
from shlex import quote
import struct
import subprocess
import time
import webbrowser
from playsound import playsound  
import eel
import os
import sqlite3

import pyaudio
import pyautogui

from engine.command import speak
from engine.config import ASSISTANT_NAME

import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, remove_words 
from hugchat import hugchat
# Playing assistant sound function

con = sqlite3.connect("neura.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"  # Path to your sound file
    playsound(music_dir)  # Call the playsound function

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")    
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip() #remove spaces from start and end of query

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening"+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening"+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening"+query)
                    try:
                        os.system('start '+query) #start brave
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term +" on YouTube")
    kit.playonyt(search_term) 

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
            
# Find Contacts
def findContact(query):
     
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    try:
        if flag == 'message':
            target_tab = 11
            neura_message = f"Message sent successfully to {name}"
        elif flag == 'call':
            target_tab = 6
            message = ''
            neura_message = f"Calling {name}"
        else:
            target_tab = 5
            message = ''
            neura_message = f"Starting video call with {name}"

        # Clean phone number (remove spaces and special chars)
        clean_number = ''.join(filter(str.isdigit, mobile_no))

        # Construct URL with cleaned number and encoded message
        whatsapp_url = f"whatsapp://send?phone={clean_number}&text={quote(message)}"

        # Open WhatsApp link
        subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
        time.sleep(3)  # Wait for WhatsApp to open

        # Focus search and navigate tabs
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)

        for _ in range(target_tab):
            pyautogui.press('tab')
            time.sleep(0.2)

        time.sleep(0.5)
        pyautogui.press('enter')

        speak(neura_message)
        return True

    except Exception as e:
        print(f"Error: {e}")
        speak(f"Failed to complete {flag} with {name}")
        return False

#Chat Bot
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
