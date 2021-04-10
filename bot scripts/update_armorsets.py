import pywikibot

import argparse
from  string import ascii_uppercase
import os
import logging

parser = argparse.ArgumentParser(description='Update armor set pages')
parser.add_argument("set_dir", help="Directory where all the sets are stored")
args = parser.parse_args()

logger = logging.getLogger("edain")
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    site = pywikibot.Site()
    site.login()

    for letter in ascii_uppercase:
        logger.info(letter)
        page = pywikibot.Page(site, f"Armor Sets/{letter}")

        with open(os.path.join(args.set_dir, f"armorset_{letter}.txt"), "r") as f:
            new_set = f.read()

            if page.text == new_set:
                logger.info("Nothing changed")
                continue

            page.text = new_set
            logger.info("Updated")
            page.save(summary="Automatic update of armor sets", minor=False)
