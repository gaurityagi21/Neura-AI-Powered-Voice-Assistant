import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') #getting details of current voice
    engine.setProperty('voice', voices[1].id) #changing index, changes voices. 1 for female & changing index, changes voices. o for male
    engine.setProperty('rate', 174)     # setting up new voice rate
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer() #variable initialised using recognizer 
    
    with sr.Microphone() as source:   # mic is used as a source to detect speech
        print('Listening...')
        eel.DisplayMessage('listening...')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source, duration=1)

        audio=r.listen(source, timeout=5, phrase_time_limit=8) 
    try:
        print('recognizing')
        eel.DisplayMessage('recognizing...')
        query= r.recognize_google(audio, language='en-in') #recognize_google is standard engine of recognize
        print(f"user said:{query}")  
        eel.DisplayMessage(query) 
        time.sleep(2)

    except Exception as e: 
        print(f"Error: {e}")
        eel.DisplayMessage("Sorry, I didn't catch that. Please try again.")  # Handle errors 
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    try:

        query = takecommand()
        print(query)


        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
            
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)
                
        else:
            from engine.features import chatBot 
            chatBot(query)
    except:
        print("error")
        
    eel.ShowHood()      
