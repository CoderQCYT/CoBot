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
    keyboard.press("space")
def unclick():
    keyboard.release("space")

def clicktwo():
    keyboard.press("up_arrow")
def unclicktwo():
    keyboard.release("up_arrow")
    

recording = 1
delay = 0.01
speedhack = 1
physics = 1
step = 0
step_setup = False
frame = 1
playback_ended = False
    
while True:
    if keyboard.is_pressed('P') and recording != 0:
        recording = 0
        print("In playing mode")
    if keyboard.is_pressed('F') and physics == 1:
        print ("Physics is off")
        physics = 0
    if keyboard.is_pressed('R') and recording != 1:
        recording = 1
        print("In record mode")
    if keyboard.is_pressed('E') and physics == 0:
        print ("Physics is on")
        physics = 1

    if mem.get_x_pos() > 0 and recording == 1:
        try:
            os.remove("macro.cobot")
        except:
            print("You did not record a macro before...")
        print('Starting to record!')
        f = open("macro.cobot","w")
        frame = 1
        # speedhack = float(input("Speedhack: "))
        macro = {"speedhack":speedhack,"macro":[]}
        cli = 0
        twopcli = 0
        while mem.get_x_pos() > 0.1:
            if not(mem.is_dead()):
                if step_setup == True:
                    mem.set_x_pos(step_x)
                    mem.set_y_pos(step_y)
                    step_setup = False
                list = {"click":cli,"arrow":twopcli,"x": str(mem.get_x_pos()),"y": str(mem.get_y_pos()),"frame":frame}
                if win32api.GetKeyState(0x01) < 0 or win32api.GetKeyState(0x20) < 0:
                    cli = 1
                else:
                    cli = 0
                if win32api.GetKeyState(0x26):
                    twopcli = 1
                else:
                    twopcli = 0
                macro["macro"].append(list)
                time.sleep(delay / speedhack)
                frame = frame + 1
                if keyboard.is_pressed('Z'):
                    step = frame
                    step_x = mem.get_x_pos()
                    step_y = mem.get_y_pos()
                    print("Saved a step at frame: " + str(frame))
            if mem.is_dead() and not(mem.is_practice_mode()):
                frame = 0
                
            if step > 0 and mem.is_practice_mode() and mem.is_dead():
               # frame = step
                step_setup = True
                while frame > step:
                    macro["macro"].pop(0)
                    frame = frame - 1
                    


        string = str(macro)
        f.write(string.replace("\'","\""))
        f.close()
        print ("Finished recording!")
    elif mem.get_x_pos() > 0 and recording == 0:
        frame = 0
        #macro = input("Enter macro name: ")
        # TODO add speedhack support 
        # p = open(macro + ".cobot")
        if not(playback_ended):
            print("Playing back")
            json_file = open("macro.cobot")
            data = json.load(json_file)
            speedhack = data['speedhack']
        # print(data)
        while mem.get_x_pos() > 0.1 and mem.is_in_level():
            try:
                if not(mem.is_dead()):
                    if physics == 1:
                        mem.set_x_pos(float(data['macro'][frame]['x']))
                        mem.set_y_pos(float(data['macro'][frame]['y']))
                    if data['macro'][frame]['click'] == 1:
                        click()
                    else:
                        unclick()
                    if data['macro'][frame]['arrow'] == 1:
                        clicktwo()
                    else:
                        unclicktwo()
                    time.sleep(delay/speedhack)
                    frame = frame + 1
                if mem.is_dead() and not(mem.is_practice_mode()):
                    frame = 0

            except:
                playback_ended = True
                print("Playback ended!")
                json_file.close()
                unclick()
                playback_ended = False
                break

