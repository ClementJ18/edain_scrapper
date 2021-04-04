import time
import pyautogui
import pyperclip
from heroes import hero_dict, summonable_dict
from utils import matching_unit, unit_first, okay, horde_search, unit_search, indexes, copy_box, get_buttons_and_sets

template = """
{{{{Unit
|image=Example
|faction=Example
|object_name={object}
|unit_type={type}
|size={number}
|location=Example
|requirement=Example
|cost={build_cost}
|command_points={cp}
|time={build_time}
|health={health_points}
|armor={armor}
|trample_damage={crush_damage}
|revenge_damage={crushrevengedamage}
|attack_speed={attack_duration}
|speed={speed}
|range={attack_range}
|health_alt={health_points}
|armor_alt={armor}
|trample_damage_alt={crush_damage}
|revenge_damage_alt={crushrevengedamage}
|attack_speed_alt={attack_duration}
|speed_alt={speed}
|range_alt={attack_range}{damages}
}}}}
"""

damage_templates = [
"""
|damage_type={damagetype}
|damage_targets=All
|damage={damage}
|radius={radius}""",

"""
|damage_type_2={damagetype}
|damage_targets_2=All
|damage_2={damage}
|radius_2={radius}""",
"""
|damage_type_alt={damagetype}
|damage_targets_alt=All
|damage_alt={damage}
|radius_alt={radius}""",

"""
|damage_type_alt_2={damagetype}
|damage_targets_alt_2=All
|damage_alt_2={damage}
|radius_alt_2={radius}""",
]

toggles = [
    "imladrisentfir"
]

summons = [
    "DolAmrothGardeFootHorde",
    "DolAmrothGardeMountedHorde",
    "AngmarTributKarrenCarnDum"
]

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
        "crush_damage":"",
        "crushrevengedamage":"",
        "attack_duration":"",
        "speed":"",
        "attack_range":"",
        "object": "",
        "type":""
    }

def get_all_units(commandbuttons, commandsets):
    units = set()
    for button in commandbuttons.values():
        if not "Command" in button or not "Object" in button:
            continue

        if button["Command"] == "UNIT_BUILD":
            units.add(button["Object"])

    return list(units)


def write_data(horde, toggled=False):
    if toggled:
        pyautogui.click(x=indexes[0][0], y=indexes[0][1])
    else:
        search(horde)
        time.sleep(5)

    data = copy_box()

    formatted = default_dict()
    formatted["object"] = horde
    damages = {}
    current_damage = None
    for x in data:
        if x.startswith(("Damage", "Radius")):
            if x.startswith("Damagetype"):
                current_damage = x.split("\t")[-1].strip()
                damages[current_damage] = {"damagetype": current_damage}
            else:
                key, value = x.split("\t", maxsplit=1)
                damages[current_damage][key.lower()] = value.strip()

            continue
    
        separator = "\t"
        if ":" in x:
            separator = ":"

        try:
            key, value = x.split(separator, maxsplit=1)
            formatted[key.lower().replace(" ", "_").strip()] = value.strip()
        except ValueError:
            print(f"WARNING: Could not parse: {x}")

    damage_formatted = ""
    if toggled:
        counter = 2
    else:
        counter = 0
    for value in damages.values():
        damage_formatted += damage_templates[counter].format(**value)
        counter += 1

    if toggled:
        return formatted, damage_formatted

    if horde.lower() in toggles:
        alt, dmgs = write_data(horde, toggled=True)
        damage_formatted += dmgs

        formatted = {**formatted, **alt}

    final = template.format(damages=damage_formatted, **formatted)


    with open("../stats/units.txt", "a+") as f:
        f.write(final)


def main():
    #one specific unit
    # for x in ["ImladrisEntFir"]:
    #     write_data(x)

    #all units
    hordes = get_all_units(*get_buttons_and_sets()).extend(summons)
    for horde in hordes:
        if horde not in hero_dict and horde not in summonable_dict:
            write_data(horde)
            reset()

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
