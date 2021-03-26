import pywikibot
import sys
import re
from pywikibot import pagegenerators
import datetime


from  string import ascii_uppercase
import os
import logging

site = pywikibot.Site()

def main():
    set_dir = sys.argv[1]

    for letter in ascii_uppercase:
        print(letter)
        page = pywikibot.Page(site, f"Armor Sets/{letter}")

        with open(os.path.join(set_dir, f"armorset_{letter}.txt"), "r") as f:
            new_set = f.read()

            if page.text == new_set:
                print("Nothing changed")
                return

            page.text = new_set
            print("Updated")
            page.save(summary="Automatic update of armor sets", minor=False)


if __name__ == '__main__':
    main()