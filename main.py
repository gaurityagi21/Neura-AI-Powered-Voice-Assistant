import os
import eel

from engine.features import *
from engine.command import *

def start():
    
    eel.init("www")

    playAssistantSound()


    # Open Microsoft Edge in app mode
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # eel.start() function
    eel.start('index.html', mode=None, host='localhost', block=True)
