
entries = {}

with open("_gamedata.inc", "r") as f:
    for line in f.readlines():
        if line.startswith("#define"):
            line = line.split("//")[0].split(";")[0]
            _, name, value = line.split(maxsplit=2)
            entries[name] = value
string = ""
for entry, value in entries.items():
    string += f"{entry} - <section begin={entry} />{value}<section end={entry} />\n"

with open("gamedata.txt", "w") as f:
    f.write(string)