import pywikibot
import sys
import re
from pywikibot import pagegenerators
import datetime

import os
import logging

path = os.path.join("C:\\Users\\Clement\\Documents\\GitHub\\edain_scrapper\\logs", f'{datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")}.log')


logger = logging.getLogger("edain")
logger.setLevel(logging.DEBUG)

pf = logging.FileHandler(path)
pf.setLevel(logging.INFO)
logger.addHandler(pf)

sm = logging.StreamHandler()
sm.setLevel(logging.DEBUG)
logger.addHandler(sm)

site = pywikibot.Site()

def load_stats():
    try:
        with open(sys.argv[1], 'r') as f:
            matches = re.findall(r"{{(.*?)}}", f.read(), re.DOTALL|re.MULTILINE)
    except IndexError:
        raise IndexError("Specify path")

    stats = {}
    for match in matches:
        raw = match.split("|")
        args = {x.split("=", maxsplit=1)[0]: x.split("=", maxsplit=1)[1].replace("\n", "") for x in raw[1:]}
        try:
            stats[args["object_name"].lower()] = args
        except KeyError:
            stats[args["object"].lower()] = args

    return stats

def update_page(page, stats):
    template = None
    for temp in page.templatesWithParams():
        if f"Template:{sys.argv[3]}" == temp[0].title():
            template = temp
            break
    else:
        logger.error(f"Could not find template {sys.argv[3]} on page {page.title()}")
        return

    args = {x.split("=", maxsplit=1)[0]: x.split("=", maxsplit=1)[1] for x in template[1]}

    try:
        name = args["object_name"].lower()
    except KeyError:
        try:
            name = args["object"].lower()
        except KeyError:
            return

    try:
        new_stats = stats[name]
    except KeyError:
        logger.error(f"KeyError: {name}")
        return

    changed = False
    logger.info(name)
    changelog = ""
    for arg in args:
        if not arg in new_stats:
            continue

        if new_stats[arg] == "Example" or new_stats[arg] == "":
            continue

        if args[arg] != new_stats[arg]:
            logger.info(f"{arg}: {args[arg]} to {new_stats[arg]}")
            args[arg] = new_stats[arg]
            changed = True

    updated_stats = [f"|{key}={value}" for key, value in args.items()]
    formatted = '\n'.join(updated_stats)
    updated_template = f"{{{{{sys.argv[3]}\n{formatted}\n}}}}"
    old_template = re.findall(f"{{{{{sys.argv[3]}.*?}}}}", page.text, re.DOTALL|re.MULTILINE)[0]
    page.text = page.text.replace(old_template, updated_template)

    if not changed:
        return

    logger.debug("======================================================================================")

    logger.debug(old_template)

    logger.debug("======================================================================================")

    logger.debug(updated_template)

    logger.debug("======================================================================================")

    approved = input(">>> ")
    if approved.lower().startswith("y"):
        page.save(summary=f"Automatic update of template stats", minor=False)


def main():
    stats = load_stats()

    try:
        cat = pywikibot.Category(site,f'Category:{sys.argv[2]}')
    except IndexError:
        raise IndexError("Specify a category")

    gen = pagegenerators.CategorizedPageGenerator(cat)

    for pag in gen:
        update_page(pag, stats)

if __name__ == '__main__':
    main()
