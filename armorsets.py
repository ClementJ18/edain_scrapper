from collections import defaultdict
import re

table_header = """
=== {armorset_lower} ===
<section begin={armorset_lower} />
{{| class="wikitable"
! colspan="2" |  <span class="mw-customtoggle-{armorset} wikia-menu-button" style="float:left">[+/-]</span>{armorset}"""

armorset_template = """
|- id="mw-customcollapsible-{armorset}" class="mw-collapsible mw-collapsed"
| {damage} || {number}%"""

armors_raw = []
for file in ["armor.ini", "armor.inc"]:
    try:
        with open(file) as f:
            armors_raw += f.readlines()
    except FileNotFoundError:
        pass

armor_dict = defaultdict(lambda: defaultdict(dict))
current = []
for line in armors_raw:
    line = line.strip()
    if line.lower() in ["", "end"] or line.startswith((";", "/", "#")):
        continue
    line = re.sub(r"\W*;.*", "", line).strip()
    line = re.sub(r"\W*//.*", "", line).strip()

    if line.startswith("Armor") and "=" not in line:
        current = line.strip().split(" ")[1].replace("ü", "u").replace("ä", "a")
    elif "FlankedPenalty" in line:
        number = line.split("=")[1]
        armor_dict[letter][current]["FlankedPenalty"] = number
    elif "DamageScalar" in line:
        number = line.split("=")[1]
        armor_dict[letter][current]["DamageScalar"] = number
    else:
        letter = current[0].upper()
        damage = line.split("=")[1].split()[0]
        number = line.split("=")[1].split()[1]
        armor_dict[letter][current][damage] = number

keys = list(armor_dict.keys())
keys.sort()
tabview = "<tabview>"
for key in keys:
    tabview += f"\nArmor Sets/{key}|{key}"
    final_string = "__NOTOC__"
    for armorset in armor_dict[key]:
        final_string += table_header.format(armorset=armorset, armorset_lower=armorset.lower())
        for damage in armor_dict[key][armorset]:
            number = armor_dict[key][armorset][damage]
            final_string += armorset_template.format(armorset=armorset, damage=damage, number=number.replace("%", ""))
        
        final_string += "\n|}}\n<section end={armorset_lower} />\n".format(armorset_lower=armorset.lower())

    with open(f"sets/armorset_{key}.txt", "w") as f:
        f.write(final_string)

tabview += "\n</tabview>"
with open("tabview.txt", "w") as f:
    f.write(tabview)
