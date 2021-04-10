import pywikibot
from pywikibot import pagegenerators

import argparse
import os

parser = argparse.ArgumentParser(description='Get all the infoboxes to be updated, this is a clearner approach then parsing everything')
parser.add_argument("folder", help="The folder where to save the files")
parsed_args = parser.parse_args()


def main(category, temp_name):
    cat = pywikibot.Category(site,f'Category:{category}')
    gen = pagegenerators.CategorizedPageGenerator(cat)
    file = open(os.path.join(parsed_args.folder, f"{category.lower()}.txt"), "a+")

    for page in gen:
        print(page.title())
        template = None
        for temp in page.templatesWithParams():
            if f"Template:{temp_name}" == temp[0].title():
                template = temp
                break
        else:
            continue

        args = {}
        for x in template[1]:
            key = x.split("=", maxsplit=1)[0]
            try:
                value = x.split("=", maxsplit=1)[1]
            except IndexError:
                value = ""

            args[key] = value

        names = args.pop("object_name", None)
        if names is None:
            names = args.pop("object", None)

        if names is None:
            print(f"Could not find object name in: {args}")
            continue

        for name in names.split("/"):
            file.write(f"{name.strip()}\n")

    file.close()

if __name__ == '__main__':
    site = pywikibot.Site()
    site.login()
    for category_name, template_name in [("Unit", "Unit"), ("Hero", "Hero"), ("Building", "Infobox Building")]:
        print(category_name)
        main(category_name, template_name)
