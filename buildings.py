from ini_parser import parse_file
from heroes import hero_dict, summonable_dict, search, copy_box, click_search_button, click_search_box
import pyautogui
import time

commandset_names = [
    # 'MordorFoundationCommandSet', 'MordorEconomyPlotCommandSet', 'MordorOutpostCommandSet', 
    # 'RohanFoundationCommandSet', 'RohanEconomyPlotCommandSet', 'RohanOutpostCommandSet', 
    # 'GondorFoundationCommandSet', 'GondorEconomyPlotCommandSet', 'GondorOutpostCommandSet', 
    # 'IsengardFoundationCommandSet', 'IsengardEconomyPlotCommandSet', 'IsengardOutpostCommandSet', 
    # 'ImladrisFoundationCommandSet', 'ImladrisEconomyPlotCommandSet', 'ImladrisOutpostCommandSet', 
    # 'LothlorienFoundationCommandSet', 'LothlorienEconomyPlotCommandSet', 'LothlorienOutpostCommandSet', 
    # 'AngmarFoundationCommandSet', 'AngmarEconomyPlotCommandSet', 'AngmarOutpostCommandSet', 
    # 'ArnorGondorFoundationCommandSet', 'ArnorGondorEconomyPlotCommandSet', 'ArnorGondorOutpostCommandSet',
    # 'DwarvenFoundationCommandSet_Erebor', 'DwarvenEconomyPlotCommandSet_Erebor', 'DwarvenOutpostCommandSet_Erebor', 'DwarvenOutpostCommandSet_EredLuin', 'DwarvenOutpostCommandSet_Eisenberge',
    # 'DwarvenFoundationCommandSet_EredLuin', 'DwarvenEconomyPlotCommandSet_EredLuin', 'DwarvenOutpostCommandSet_EredLuin', 
    # 'DwarvenFoundationCommandSet_Eisenberge', 'DwarvenEconomyPlotCommandSet_Eisenberge', 'DwarvenOutpostCommandSet_Eisenberge'
]

level_box = (482, 96)
level3_box = (482, 146)
okay = (1090, 535)

template_start = """
{{Infobox Building"""

template_basic = """
|image=Example
|faction=Example
|type=Example
|object={object}
|level_up=Example
|cost={build_cost}
|time={build_time}
|location=Example"""

template_level = """
|armor{level}={armor}
|health{level}={health_points}
|resources{level}={money_production}
|interval{level}={money_interval}
|damage{level}={damage}
|damage_type{level}={damagetype}
|attack_speed{level}={attack_duration}
|range{level}={attack_range}
|level_effect{level}={effect}"""

template_end = """
}}
"""

def get_all_buildings(commandbuttons, commandsets):
    plots = {key : value for key, value in commandsets.items() if key in commandset_names}
    buildings = set()
    for key, meta_dict in plots.items():
        for key, value in meta_dict.items():
            if not key.isdigit():
                continue

            button = commandbuttons[value]
            if not "Command" in button or not "Object" in button:
                continue 

            if button["Command"] == "FOUNDATION_CONSTRUCT" or button["Command"] == "CASTLE_UNPACK_EXPLICIT_OBJECT":
                buildings.add(button["Object"])
                
    return buildings

def default_dict():
    return {
        "level": "",
        "object": "",
        "build_cost": "",
        "build_time": "",
        "armor": "",
        "health_points": "",
        "money_production": "",
        "money_interval": "",
        "damage":"",
        "damagetype":"",
        "attack_duration":"",
        "attack_range":"",
        "effect": ""
    }

def write_data(building):
    search(building)
    pyautogui.click(x=okay[0], y=okay[1])

    # pyautogui.click(x=level_box[0], y=level_box[1])
    # pyautogui.hotkey('down')
    # pyautogui.hotkey('down')

    data = copy_box()
    formatted = default_dict()
    formatted["object"] = building
    formatted["level"] = 1
    for x in data:
        if "Level 1:" in x:
            formatted["effect"] = x.split(":")[1].strip()
        formatted[x.split("\t")[0].lower().strip().replace(" ", "_")] = x.split("\t")[-1].strip()

    basic = template_basic.format(**formatted)
    level1 = template_level.format(**formatted).replace("Sekunden", "Seconds")

    eco_up = None
    try:
        eco_up = pyautogui.locateOnScreen("eco_1.png")
        pyautogui.click(x=eco_up[0] + 2, y=eco_up[1] + 2)
    except Exception:
        pyautogui.click(x=level_box[0], y=level_box[1])
        pyautogui.hotkey('down')
        pyautogui.hotkey('enter')

    data = copy_box()
    formatted = default_dict()
    formatted["object"] = building
    formatted["level"] = 2
    for x in data:
        if "Level 2:" in x:
            formatted["effect"] = x.split(":")[1].strip()
        formatted[x.split("\t")[0].lower().strip().replace(" ", "_")] = x.split("\t")[-1].strip()

    if formatted["money_production"].isdigit() and eco_up is not None:
        formatted["money_production"] = int(int(formatted["money_production"]) * 1.25)

    level2 = template_level.format(**formatted).replace("Sekunden", "Seconds") 

    eco_up = None
    try:
        eco_up = pyautogui.locateOnScreen("eco_2_extern.png")
        pyautogui.click(x=eco_up[0] + 2, y=eco_up[1] + 2)
    except Exception:
        try:
            eco_up = pyautogui.locateOnScreen("eco_2_intern.png")
            pyautogui.click(x=eco_up[0] + 2, y=eco_up[1] + 2)
        except Exception:
            pyautogui.click(x=level_box[0], y=level_box[1])
            pyautogui.hotkey('down')
            pyautogui.hotkey('enter')
    
    data = copy_box()
    formatted = default_dict()
    formatted["object"] = building
    formatted["level"] = 3
    for x in data:
        if "Level 3:" in x:
            formatted["effect"] = x.split(":")[1].strip()
        formatted[x.split("\t")[0].lower().strip().replace(" ", "_")] = x.split("\t")[-1].strip()

    if formatted["money_production"].isdigit() and eco_up is not None:
        formatted["money_production"] = int(int(formatted["money_production"]) * 1.25 * 1.20)
    level3 = template_level.format(**formatted).replace("Sekunden", "Seconds")

    final = template_start + basic + level1 + level2 + level3 + template_end
    with open("buildings.txt", "a+") as f:
        f.write(final)

def main():
    commandbuttons = {}
    for file in ["commandbutton.ini", "includes\\commandbutton.inc", "includes\\FBTempcommandbutton.inc"]:
        new = parse_file("C:\\Users\\Clement\\Documents\\Beta Files\\data\\ini\\{}".format(file))
        commandbuttons = {**commandbuttons, **new}

    commandsets = {}
    for file in ["commandset.ini", "includes\\commandset.inc", "includes\\FBTempcommandbutton.inc"]:
        new = parse_file("C:\\Users\\Clement\\Documents\\Beta Files\\data\\ini\\{}".format(file))
        commandsets = {**commandsets, **new}


    if False:
        buildings = get_all_buildings(commandbuttons, commandsets)
        for building in buildings:
            write_data(building)
    else:
        write_data("imladrislagerstätte")


if __name__ == '__main__':
    pyautogui.hotkey("numlock")
    pyautogui.hotkey("alt", "tab")
    try:
        # hordes, commandsets, commandbuttons = main()
        main()
    except Exception as e:
        pyautogui.hotkey("alt", "tab")
        pyautogui.hotkey("numlock")
        raise

    pyautogui.hotkey("alt", "tab")
    pyautogui.hotkey("numlock")