from ini_parser import parse_file
from heroes import hero_dict, summonable_dict, copy_box
import pyautogui
import time
import pyperclip

search_btn = (50, 100)

unit_search = (50, 240)
horde_search = (50, 615)

matching_unit = (330, 210)
matching_horde = (330, 590)

unit_first = (50, 265)  
horde_first = (50, 635)

okay = (1090, 535)

template = """
{{{{Unit
|image=Example
|faction=Example
|object_name={object}
|unit_type=Example
|size={number}
|location=Example
|requirement=Example
|cost={build_cost}
|command_points={cp}
|time={build_time}
|health={health_points}
|armor={armor}
|damage={damage}
|trample_damage={crush_damage}
|revenge_damage={crushrevengedamage}
|damage_type={damagetype}
|attack_speed={attack_duration}
|speed={speed}
|range={attack_range}
|radius={radius}
}}}}
"""

def search(unit):
    pyperclip.copy(unit)
    if "horde" in unit.lower():
        #fill in horde name and press enter
        pyautogui.doubleClick(x=horde_search[0], y=horde_search[1])
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey("enter")
        pyautogui.click(x=okay[0], y=okay[1])

        time.sleep(1)

        #select the matching unit and press okay incase the searcher complains
        pyautogui.click(x=matching_unit[0], y=matching_unit[1])
        pyautogui.doubleClick(x=unit_first[0], y=unit_first[1])
        pyautogui.click(x=okay[0], y=okay[1])
    else:
        #fill in unit name and press enter
        pyautogui.doubleClick(x=unit_search[0], y=unit_search[1])
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey("enter")
        pyautogui.click(x=okay[0], y=okay[1])

        time.sleep(1)

        #fill in unit name into horde and press enter
        pyautogui.doubleClick(x=horde_search[0], y=horde_search[1])
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey("enter")
        pyautogui.click(x=okay[0], y=okay[1])

def reset():
    pyautogui.doubleClick(x=horde_search[0], y=horde_search[1])
    pyautogui.hotkey("backspace")

    pyautogui.doubleClick(x=unit_search[0], y=unit_search[1])
    pyautogui.hotkey("backspace")

def default_dict():
    return {
        "number": "",
        "build_cost": "",
        "cp": "",
        "build_time":"",
        "health_points":"",
        "armor":"",
        "damage":"",
        "crush_damage":"",
        "crushrevengedamage":"",
        "damagetype":"",
        "attack_duration":"",
        "speed":"",
        "attack_range":"",
        "radius":"",
        "object": ""
    }

def get_all_units(commandsets, commandbuttons):
    units = set()
    for button in commandbuttons.values():
        if not "Command" in button or not "Object" in button:
            continue 

        if button["Command"] == "UNIT_BUILD":
            units.add(button["Object"])

    return list(units)


def write_data(horde):
    search(horde)
    time.sleep(5)
    data = copy_box()

    formatted = default_dict()
    formatted["object"] = horde
    for x in data:
        formatted[x.split("\t")[0].lower().replace(" ", "_").strip()] = x.split("\t")[-1].strip()

    final = template.format(**formatted)
    with open("units.txt", "a+") as f:
        f.write(final)


def main():
    # commandbuttons = {}
    # for file in ["commandbutton.ini", "includes\\commandbutton.inc", "includes\\FBTempcommandbutton.inc"]:
    #     new = parse_file("C:\\Users\\Clement\\Documents\\Beta Files\\data\\ini\\{}".format(file))
    #     commandbuttons = {**commandbuttons, **new}

    # commandsets = {}
    # for file in ["commandset.ini", "includes\\commandset.inc", "includes\\FBTempcommandbutton.inc"]:
    #     new = parse_file("C:\\Users\\Clement\\Documents\\Beta Files\\data\\ini\\{}".format(file))
    #     commandsets = {**commandsets, **new}

    for x in ["LothlorienMirkwoodPalaceGuardHorde"]:
        write_data(x)

    # hordes = get_all_units(commandsets, commandbuttons)
    # for horde in hordes:
    #     if horde not in hero_dict and horde not in summonable_dict:
    #         write_data(horde)
    #         reset()

if __name__ == '__main__':
    pyautogui.hotkey("numlock")
    pyautogui.hotkey("alt", "tab")
    try:
        main()
    except Exception as e:
        pyautogui.hotkey("alt", "tab")
        pyautogui.hotkey("numlock")
        raise

    pyautogui.hotkey("alt", "tab")
    pyautogui.hotkey("numlock")
