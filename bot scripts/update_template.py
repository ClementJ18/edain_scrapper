import pywikibot
import re
from pywikibot import pagegenerators
import datetime
import argparse

import os
import logging

parser = argparse.ArgumentParser(description='Update the stats in infoboxes for Units, Buildings and Heroes. This does not cover all the infoboxes are some of them are ridiculously complex. See User:The_Necromancer0#Problem_Children')
parser.add_argument("txt", help="Txt file containing the updated templates")
parser.add_argument("category", help="Category name of pages to grab")
parser.add_argument("template", help="Name of the template to update")
parsed_args = parser.parse_args()

path = os.path.join("C:\\Users\\Clement\\Documents\\GitHub\\edain_scrapper\\logs", f'{parsed_args.category}_{datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")}.log')

logger = logging.getLogger("edain")
logger.setLevel(logging.DEBUG)

pf = logging.FileHandler(path)
pf.setLevel(logging.INFO)
logger.addHandler(pf)

sm = logging.StreamHandler()
sm.setLevel(logging.DEBUG)
logger.addHandler(sm)

def load_stats():
    with open(parsed_args.txt, 'r') as f:
        matches = re.findall(r"{{(.*?)}}", f.read(), re.DOTALL|re.MULTILINE)

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
        if f"Template:{parsed_args.template}" == temp[0].title():
            template = temp
            break
    else:
        logger.error(f"Could not find template {parsed_args.template} on page {page.title()}")
        return

    args = {x.split("=", maxsplit=1)[0]: x.split("=", maxsplit=1)[1] for x in template[1]}

    names = args.pop("object_name", None)
    if names is None:
        names = args.pop("object", None)

    if names is None:
        logging.error(f"Could not find object name in: {args}")
        return

    names = names.lower()
    for name in names.split("/"):
        name = name.strip()
        new_stats = stats.get(name, None)
        if new_stats:
            break

        logger.error(f"KeyError: {name}")
    else:
        return

    changed = False
    logger.info(names)

    for arg in new_stats:
        if arg not in args:
            logger.info(f"Added {arg}: {new_stats[arg]}")
            args[arg] = new_stats[arg]

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
    updated_template = f"{{{{{parsed_args.template}\n{formatted}\n}}}}"
    old_template = re.findall(f"{{{{{parsed_args.template}.*?}}}}", page.text, re.DOTALL|re.MULTILINE)[0]
    page.text = page.text.replace(old_template, updated_template)

    if not changed:
        return

    logger.debug("======================================================================================")

    logger.debug(old_template)

    logger.debug("======================================================================================")

    logger.debug(updated_template)

    logger.debug("======================================================================================")

    approved = input(">>> ")
    if approved.lower().startswith("y") or approved == "":
        page.save(summary="Automatic update of template stats", minor=False)

if __name__ == '__main__':
    site = pywikibot.Site()
    site.login()
    txt_stats = load_stats()
    cat = pywikibot.Category(site,f'Category:{parsed_args.category}')
    gen = pagegenerators.CategorizedPageGenerator(cat)

    for pag in gen:
        update_page(pag, txt_stats)
