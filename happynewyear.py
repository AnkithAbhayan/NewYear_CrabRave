from tkinter import *
import sys
import pytz
import time
from datetime import datetime
from random import randint,shuffle
import threading
import pygame

pygame.mixer.init()
pygame.mixer.music.load(
    "Noisestorm - Crab Rave (Official Music Video) (320 kbps).mp3"
)

def hex_from_rgb(rgb):
    return "#%02x%02x%02x" % rgb   
alarms = {
    "11:58:45":"Let the music start!",
    "12:00:00":"Happy New year!"
    
}
default = hex_from_rgb((255,255,255))

def ringalarmwhenitstime(Gui):
    def hex_from_rgb(rgb):
        return "#%02x%02x%02x" % rgb   
    def dismiss_alarm():
        global stop
        stop = True

        #Gui.alarm_info.destroy()
        #Gui.alarm_notice.destroy()
        Gui.dismiss_button.destroy()
        Gui.all_alarm_info = Label(Gui.root, text=get_alarm_list(), font=extremely_small_font, fg=default, bg=hex_from_rgb((20,20,20)) )
        Gui.all_alarm_info.grid(row=2, column=0, columnspan=2)
    

    def playringtone(alarm_name):
        stop = False
        Gui.info["text"] = "Happy New Year 2023!"

        Gui.all_alarm_info.destroy()
        #Gui.alarm_notice = Label(Gui.root, font=small_font, text="Alarm is ringing!", fg=hex_from_rgb((0,0,0)), bg=hex_from_rgb((0,255,0)))
        #Gui.alarm_notice.grid(row=2, column=0, pady=7, columnspan=2)
        #Gui.alarm_info = Label(Gui.root, font=small_font, text=f"Alarm info: {alarm_name}", fg=default, bg=hex_from_rgb((20,20,20)))
        #Gui.alarm_info.grid(row=3, column=0, columnspan=2)

        Gui.dismiss_button = Button(Gui.root,bg=hex_from_rgb((20,20,20)), font=small_font, text="Dismiss", command=lambda:dismiss_alarm())
        Gui.dismiss_button.grid(row=4, column=0, pady=12, columnspan=2)

        rgbs = [
            (255,255,0),
            (125,125,50),
            (255,0,255),
            (125,50,125),
            (0,255,255),
            (50,125,125),
            (255,0,0),
            (125,50,50),
            (0,255,0),
            (50,125,50),
            (0,0,255),
            (50,50,125)
        ]
        while True:
            shuffle(rgbs)
            for item in rgbs:
                r,g,b = item[0],item[1],item[2]
                
                """while r!=Gui.current_rgb[0] or g!=Gui.current_rgb[1] or b!=Gui.current_rgb[2]:
                    if r > Gui.current_rgb[0]:
                        Gui.current_rgb[0] += 5
                    elif r < Gui.current_rgb[0]:
                        Gui.current_rgb[0] -= 5

                    if g > Gui.current_rgb[1]:
                        Gui.current_rgb[1] += 5
                    elif g < Gui.current_rgb[1]:
                        Gui.current_rgb[1] -= 5

                    if b > Gui.current_rgb[2]:
                        Gui.current_rgb[2] += 5
                    elif b < Gui.current_rgb[2]:
                        Gui.current_rgb[2] -= 5
                """
                rev = hex_from_rgb(item)
                Gui.root["bg"] = rev
                Gui.info["fg"] = rev
                Gui.am_or_pm["fg"] = rev
                Gui.dismiss_button["fg"] = rev
                Gui.timestamp["fg"] = rev
                time.sleep(0.1)
            if stop == True:
                print("YESSSS")
                print("Dismiss button pressed.")
                Gui.root["bg"] = hex_from_rgb((0,0,0))
                Gui.info["fg"] = hex_from_rgb((255,255,255))
                sys.exit()

    for item, value in alarms.items():
        temp = getcurrenttime()[0]
        if item == temp:
            if alarms[item] == "Happy New year!":
                dewit = threading.Thread(target=lambda: playringtone(value))
                dewit.start()
            else:
                pygame.mixer.music.play()
                Gui.info["text"] = "Now Playing: Crab Rave (Beat drop at midnight!)"

            break

def getcurrenttime():
    test = datetime.now(tz=pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S")
    temp = time.strptime(str(test), "%H:%M:%S")
    return [time.strftime("%I:%M:%S", temp), time.strftime("%p", temp)]

def get_alarm_list():
    list_of_alarms = "All Alarms:"
    checking_lenghtiest = []
    for key, value in alarms.items():
        checking_lenghtiest.append(value)
    length = len(max(checking_lenghtiest, key=len))

    for key, value in alarms.items():
        list_of_alarms += f"\n{key} AM-  {value}{' '*(length-len(value))}"
    return list_of_alarms

def updaterealtime(Gui):
    current_time = getcurrenttime()
    Gui.timestamp["text"] = current_time[0]
    Gui.am_or_pm["text"] = current_time[1]

    while True:
        temp_var = getcurrenttime()
        if temp_var[0] != current_time[0]:
            current_time=temp_var
            Gui.timestamp["text"] = current_time[0]
            Gui.am_or_pm["text"] = current_time[1]
            ringalarmwhenitstime(Gui)

def togglewindowstate(Gui):
    if Gui.root.attributes('-fullscreen'):
        Gui.root.attributes('-fullscreen', False)
    else:
        Gui.root.attributes('-fullscreen', True)

large_font = ("Fira Code", 150)
medium_font = ("Fira Code", 100)
small_font = ("Fira Code", 25)
extremely_small_font = ("Fira Code", 12)


class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.bind("<F11>", lambda event: togglewindowstate(self))

        self.root["bg"] = hex_from_rgb((0,0,0))
        
        self.current_rgb = [255,0,0]
        self.clrcutoff = 15
        
        self.info = Label(self.root, text="Get ready for 2023!", font=small_font, fg=default, bg=hex_from_rgb((20,20,20)))
        self.timestamp = Label(self.root, text="00:00:00", font=large_font, fg=default, bg=hex_from_rgb((20,20,20)))
        self.am_or_pm = Label(self.root, text="NN", font=medium_font, fg=default, bg=hex_from_rgb((20,20,20)))
        self.all_alarm_info = Label(self.root, text=get_alarm_list(), font=extremely_small_font, fg=default, bg=hex_from_rgb((20,20,20)) )

        self.info.grid(row=0, column=0, pady=50, columnspan=2)
        self.timestamp.grid(row=1, column=0, pady=70, padx=80)
        self.am_or_pm.grid(row=1, column=1)
        self.all_alarm_info.grid(row=2, column=0, columnspan=2)

        self.timeupdate = threading.Thread(target=lambda: updaterealtime(self))
        self.timeupdate.start()


        self.root.mainloop()

Gui = Gui()
