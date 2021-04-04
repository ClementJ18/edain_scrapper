import time
import pyautogui
from utils import indexes, new_obj, copy_box, search

hero_dict = {
    'RohanPippin_mod': {'toggle': 0}, 
    'GondorBeregond': {}, 
    'GondorDenethorMod': {}, 
    'GondorBoromir_mod': {}, 
    'GondorAragornEntwicklung3': {'mount': 2}, 
    'GondorGandalf_mod': {'mount': 2},
    'GondorGandalfWhite_mod': {'mount': 2},
    'GondorImrahil': {'mount': 0}, 
    'GondorFaramir_mod': {'toggle': 0, 'mount': 3}, 

    'RohanMerry_mod': {'toggle': 0}, 
    'RohanOldMan': {}, 
    'RohanGamling_mod_neu': {'mount': 0}, 
    'RohanEowyn_mod': {'mount': 0}, 
    'RohanHama': {'mount': 0}, 
    'RohanTheodred': {'mount': 0}, 
    'RohanEomer_mod': {'mount': 0},
    'RohanTheoden_mod': {"mount": 0}, 

    'LothlorienRumil': {}, 
    'LothlorienOrophin': {},
    'LothlorienHaldir': {'toggle': 0}, 
    'LothlorienCeleborn': {}, 
    'LothlorienGaladriel': {}, 
    'LothlorienLegolas': {}, 
    'ElvenThranduil_mod': {'mount': 2, "new": True},
    'GasthausGrimbeorn': {'mount': 0},
    'ImladrisTreeberd': {'toggle': 0}, 
    'FangornFlinkbaum': {'toggle': 0},  

    'ImladrisGildor': {}, 
    'ImladrisArwen': {'mount': 0}, 
    'ImladrisZwillingeEdain': {}, 
    'ImladrisGlorfindel': {'mount': 0}, 
    'ImladrisElrond': {'mount': 1}, 
    'LothlorienCirdan': {}, 
    'DunedainHalbarad': {'toggle': 0},
    'ImladrisErestor': {},

    'DwarvenNoriErebor': {}, 
    'DwarvenGloin_mod': {}, 
    'DwarvenThorinIII': {}, 
    'DwarvenGimliMod': {}, 
    'DwarvenDainErebor': {}, 
    'DwarvenDrar': {}, 
    'DwarvenMurin': {}, 
    'DwarvenNarin': {}, 
    'DwarvenThorinIII_Eisenberge': {}, 
    'DwarvenDain_mod': {'mount': 2}, 
    'DwarvenBilbo': {'toggle': 0}, 
    'DwarvenBofur': {}, 
    'DwarvenBalin': {}, 
    'DwarvenDwalin': {'toggle': 0}, 
    'DwarvenThorin': {}, 
    'DwarvenBard': {'toggle': 1}, 
    'DwarvenBrand': {'toggle': 1}, 
    'DwarvenDurin': {},

    'IsengardWulfgar': {}, 
    'GasthausLutz': {}, 
    'IsengardWormTongue_Mod': {}, 
    'IsengardSharku_mod': {}, 
    'IsengardLurtz_mod': {'toggle': 0}, 
    'IsengardUgluk_mod': {}, 
    'IsengardSaruman_Mod': {}, 

    'MordorGorbag': {"mount": 0, "new": True},
    'MordorShagrat': {"mount": 0, "new": True},
    'MordorGothmog_mod': {'mount': 1}, 
    'GasthausKhamul': {}, 
    'MordorNazgul_CGmod': {}, 
    'MordorNazgul_CGmod2': {}, 
    'MordorMouthOfSauron_mod': {'mount': 1}, 
    'MordorWitchKingPferd': {},
    'MordorNekromantSauron': {}, 
    'MordorMollok': {'toggle': 1},
    'MordorGrond': {},
    'MordorSauron_mod': {},
    'MordorGorthaur': {},  

    'AngmarDrauglin': {}, 
    'AngmarHwaldar_mod': {}, 
    'AngmarHelegwen': {}, 
    'AngmarKarsh_mod': {}, 
    'AngmarMorgramir_mod': {}, 
    'AngmarDurmarth': {}, 
    'AngmarGulzar_Alone': {}, 
    'AngmarZaphragor': {}, 
    'AngmarWitchking_mod': {'mount': 0, "new": True}, 

    'ArnorCaptainStealthless_mod': {'toggle': 0}, 
    'ArnorMalbethRecruit': {}, 
    'ArnorAraphant': {'mount': 1}, 
    'ArnorAranarthDunedain': {},
    'ArnorAranarth': {},  
    'GondorArvedui': {}, 

    'WildYazneg': {},
    'WildGoblinKing_mod': {'toggle': 2},
    'WildAzog_mod': {'mount': 0},
    'WildGroßork': {},
    'Wildbolg': {},
    'WildDreiTrolle': {},
    'MoriaSmaugFly': {'mount': 0},

    'RohanFrodo_mod': {"toggle": 0},
    'RohanSam_mod': {'toggle': 0},
    "GasthausAlatar": {},
    'MordorCastamir': {},
    'AngmarLichkönig': {},
    'GasthausPalando': {}, 


}

summonable_dict = {
    'GondorAnarion': {},
    'RohanTreeBerd': {"toggle": 0},
    'GondorElendil': {},
    'IsengardMauhur': {},
    'GasthausBilbo': {},
    'ImladrisZwillingeEdain_GraueSchar': {},
    'MordorGrishnak_mod': {},
    'GondorEarnur': {},   

}

template_start = """
{{Hero"""

template_basic = """
|image=Example
|faction=Example
|role={role}
|importance=Example
|object={hero}
|location=Example
|cost={build_cost}
|command_points={cp}
|time={build_time}
|health={health_points}"""

template_melee = """
|armor_melee={armor}
|damage_melee={damage}
|damage_type_melee={damagetype}
|attack_speed_melee={attack_duration}
|range_melee={attack_range}
|speed_melee={speed}"""

template_ranged = """
|armor_ranged={armor}
|damage_ranged={damage}
|damage_type_ranged={damagetype}
|attack_speed_ranged={attack_duration}
|range_ranged={attack_range}
|speed_ranged={speed}"""

template_mounted = """
|armor_mounted={armor}
|damage_mounted={damage}
|trample_damage_mounted={crush_damage}
|damage_type_mounted={damagetype}
|attack_speed_mounted={attack_duration}
|range_mounted={attack_range}
|speed_mounted={speed}"""

template_end = """
}}
"""

def default_dict(hero):
    return {
        "armor": "",
        "damage": "",
        "damagetype": "",
        "attack_duration": "",
        "attack_range": "",
        "speed": "",
        "hero": hero,
        "crush_damage": "",
        "role": ""
    }

def write_data(hero):
    #initial query to figure out what the hero has available
    print(hero)
    data = copy_box()
    formatted = default_dict(hero)

    for x in data:
        if x.startswith("Strengths"):
            formatted["role"] = x.split(":")[1].strip()

        formatted[x.split("\t")[0].lower().replace(" ", "_").strip()] = x.split("\t")[-1].strip()

    #figure out initial state of hero
    string = template_basic
    if (int(formatted["speed"]) if formatted["speed"] else 1) > 80:
        string += template_mounted
    elif (int(formatted["attack_range"]) if formatted["attack_range"] else 1) > 30:
        string += template_ranged
    else:
        string += template_melee

    string = string.format(**formatted)

    #search for alternate states starting with range/melee toggle
    if "toggle" in hero_dict[hero]:
        toggle = indexes[hero_dict[hero]["toggle"]]
        pyautogui.click(x=toggle[0], y=toggle[1])
        data = copy_box()

        formatted = default_dict(hero)
        for x in data:
            formatted[x.split("\t")[0].lower().replace(" ", "_").strip()] = x.split("\t")[-1].strip()

        if (int(formatted["attack_range"]) if formatted["attack_range"] else 1) > 35:
            string += template_ranged
        else:
            string += template_melee

        string = string.format(**formatted)
        search(hero)

    #now look for a possible mount
    if "mount" in hero_dict[hero]:
        mount = indexes[hero_dict[hero]["mount"]]
        pyautogui.click(x=mount[0], y=mount[1])

        if "new" in hero_dict[hero]:
            pyautogui.click(x=new_obj[0], y=new_obj[1])

        data = copy_box()

        formatted = default_dict(hero)
        for x in data:
            formatted[x.split("\t")[0].lower().replace(" ", "_").strip()] = x.split("\t")[-1].strip()

        if (int(formatted["attack_range"]) if formatted["attack_range"] else 1) > 30:
            string += template_ranged
        else:
            string += template_mounted

        string = string.format(**formatted)

    final = template_start + string + template_end
    with open("../stats/heroes.txt", "a+") as f:
        f.write(final)

def main():
    for hero in hero_dict:
        search(hero)
        time.sleep(2)
        write_data(hero)

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
