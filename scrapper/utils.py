import os
import time
import pyautogui
import pyperclip
from ini_parser import parse_file

click_search_box = (43, 241)
click_search_button = (71, 101)
click_data_box_top = (631, 72)
click_data_box_bottom = (636, 251)

indexes = [
    (1625, 131),
    (1625, 190),
    (1625, 255),
    (1625, 320),
    (1625, 370)
]

new_obj = (1315, 365)

search_btn = (50, 100)

unit_search = (50, 240)
horde_search = (50, 615)

matching_unit = (330, 210)
matching_horde = (330, 590)

unit_first = (50, 265)
horde_first = (50, 635)

okay = (1090, 535)

level_box = (482, 96)
level3_box = (482, 146)

game_files_dir = "C:\\Users\\Clement\\Documents\\Game Files\\data\\ini"

def copy_box():
    pyautogui.click(x=click_data_box_top[0], y=click_data_box_top[1])
    time.sleep(1)
    pyautogui.hotkey("shift", "ctrl", "fn", "end")
    time.sleep(1)
    pyautogui.hotkey("ctrl", "c")

    return [x for x in pyperclip.paste().split("\n") if x.strip() != ""]

def search(hero):
    pyperclip.copy(hero)
    pyautogui.doubleClick(x=click_search_box[0], y=click_search_box[1])
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey("enter")

def get_buttons_and_sets():
    commandbuttons = {}
    for file in ["commandbutton.ini", "includes\\commandbutton.inc", "includes\\FBTempcommandbutton.inc"]:
        new = parse_file(os.path.join(game_files_dir, file))
        commandbuttons = {**commandbuttons, **new}

    commandsets = {}
    for file in ["commandset.ini", "includes\\commandset.inc", "includes\\FBTempcommandbutton.inc"]:
        new = parse_file(os.path.join(game_files_dir, file))
        commandsets = {**commandsets, **new}

    return commandbuttons, commandsets
