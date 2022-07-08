import keyboard 
import time
import win32gui
import win32api
import gd
import win32.lib.win32con as win32con
import os
import mouse
import json

mem = gd.memory.get_memory()
win = win32gui.FindWindow(None, 'Geometry Dash')

def click():
    win32api.SendMessage(win, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

def unclick():
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

accurate = 0
recording = 1
delay = 0.01
speedhack = 1
    
while True:
    if keyboard.is_pressed('P') and recording != 0:
        recording = 0
        print("In playing mode")
    if keyboard.is_pressed('R') and recording != 1:
        recording = 1
        print("In record mode")
    if mem.level_length != 0 and recording == 1:
        try:
            os.remove("macro.cobot")
        except:
            print("You did not record a macro before...")
        print('Starting to record!')
        f = open("macro.cobot","a")
        f.write("{\"macro\":[")
        cli = 0
        while not(mem.level_length == 0):
            list = {"click":cli,"x": str(mem.get_x_pos()),"y": str(mem.get_y_pos())}
            if win32api.GetKeyState(0x01) < 0:
                cli = 1
                print (1)
            else:
                cli = 0
                print (0)
            string = json.dumps(list)
            f.write(string + ",")
            time.sleep(delay / speedhack)
        f.seek(f.tell() - 1, os.SEEK_SET)
        f.truncate()
        f.write("]}")
        f.close()
        print ("Finished recording!")
    elif mem.level_length != 0 and recording == 0:
        frame = 0
        #macro = input("Enter macro name: ")
        # TODO add speedhack support 
        # p = open(macro + ".cobot")
        print("Playing back")
        json_file = open("macro.cobot")
        data = json.load(json_file)
        # print(data)
        while not(mem.level_length == 0):
            try:
                if not(mem.is_dead()):
                    print("Frame: " + str(frame))
                    mem.set_x_pos(float(data['macro'][frame]['x']))
                    mem.set_y_pos(float(data['macro'][frame]['y']))
                    if data['macro'][frame]['click'] == 1:
                        print("Clicking: 1")
                        click()
                    else:
                        print("Clicking: 0")
                        unclick()
                    time.sleep(delay)
                    frame = frame + 1
                if mem.is_dead() and not(mem.is_practice_mode()):
                    frame = 0

            except:
                print("Playback ended!")
                break

        json_file.close()
        unclick()
        

