import json
import re
from flask import Markup


def readstatusfile():
    """
    Returns all the downloaded package names, descriptions and dependencies
    in a list of lists.
    """

    pkg_names = []

    with open("/var/lib/dpkg/status", encoding="utf8") as f:
        for line in f:
            # make a list: name
            if line.startswith('Package:'):
                pkg_name = line.partition(': ')[2]
                pkg_names.append(pkg_name.replace("\n", ""))

    # with the saved package names, we can scan through
    # the whole file again !
    dependlines = ""
    dependlist = []
    after_depends = ("pre-depends:", "recommends:", "suggests:", "enhances:",
                     "breaks:", "conflicts:", "installed-size:", "maintainer:",
                     "description:", "conffiles:", "package:")
    read_depend = False

    desclines = ""
    desclist = []
    after_description = ("homepage:", "original-maintainer:", "package:")

    read_description = False

    pkg_iterator = -1
    pkg_cnt = len(pkg_names)

    # getting all the dependencies and descriptions package by package
    with open("/var/lib/dpkg/status", "rt", encoding="utf8") as f:
        # contents = f.read()
        for line in f:
            if line.lower().startswith('package:'):
                pkg_iterator = pkg_iterator + 1

            # Depends!
            if line.lower().startswith('depends:') or read_depend:
                # last row was included last time!
                if line.lower().startswith(after_depends):
                    read_depend = False

                    # if no dependenst in packages before:
                    for x in range(pkg_iterator - len(dependlist)):
                        dependlist.append("")
                    dependlist.append(dependlines)
                    dependlines = ""
                    continue

                dependlines = dependlines + line.replace("\n", " ")
                read_depend = True
                continue

            # Descriptions !!
            if line.lower().startswith('description:') or read_description:
                # last row was included last time!
                if line.lower().startswith(after_description):
                    read_description = False

                    # if no dependenst in packages before:
                    for x in range(pkg_iterator - len(desclist)):
                        desclist.append("")
                    desclist.append(desclines)
                    desclines = ""
                    continue

                desclines = desclines + line  # .replace("\n", " ")
                read_description = True
                continue

    for x in range(pkg_cnt - len(dependlist)):
        dependlist.append("")

    for x in range(pkg_cnt - len(desclist)):
        desclist.append("")

    # sanity checking
    # print(pkg_names[666:699])
    # print(dependlist[666:699])

    # to make formating more presentable
    dependsplit = []

    for dep in dependlist:
        dep = dep.replace(" ", "")
        dep = dep.replace("Depends:", "")
        dep = dep.replace(":any", "")
        dep = dep.replace("/|(.*?)(?=/,)", "")
        dependsplit.append(re.sub(r'\([^)]*\)', '', dep).split(','))

    descsplit = []
    for i, desc in enumerate(desclist):
        desc = desc.replace("Description: ", "")
        desc = desc.replace("\n", "<br>")

        if len(desc) > 1:
            desc = desc[0].upper() + desc[1:]

        descsplit.append(Markup(desc))

    # makejson = []

    # for i in range(0, pkg_cnt):
    #     name = pkg_names[i]
    #     depends = dependsplit[i]
    #     description = descsplit[i]
    #     adict =
    # {"name": name, "depends": depends, "description": description}
    #     makejson.append(adict)

    # with open('test.json', 'w') as fout:
    #     json.dump(makejson, fout)

    resultlist = [pkg_names, dependsplit, descsplit]
    # alphabetical order:
    resultlist = list(zip(*sorted(zip(*resultlist))))
    resultlist = [list(elem) for elem in resultlist]

    return resultlist
