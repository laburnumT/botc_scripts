import argparse
import jinja2
import json
import lxml.html
import os
import re
import requests
import sys


def get_base_3(role_info):
    return [x["id"] for x in role_info if "Experimental" not in x["version"]]


def get_asset(role, role_info):
    try:
        if os.path.isfile(f"assets/descriptions/{role}.txt"):
            return
    except:
        pass

    r_info = next((x for x in role_info if x["id"] == role))
    res = requests.get(
        f"https://script.bloodontheclocktower.com/{r_info['icon']}"
    )
    with open(f"assets/icons/{role}.webp", "wb") as img:
        img.write(res.content)
    res = requests.get(
        f"https://wiki.bloodontheclocktower.com/{r_info['name']}"
    )
    tree = lxml.html.fromstring(res.content)
    des = re.sub(
        r'^"(.*)"\n',
        r"\1",
        tree.xpath(
            "/html/body/div[1]/div/section/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/p[1]/text()"
        )[0],
    )
    with open(f"assets/descriptions/{role}.txt", "w") as description:
        description.write(des)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-3", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as description:
        roles = json.load(description)[1::]

    role_info = requests.get(
        "https://script.bloodontheclocktower.com/data/roles.json"
    ).json()

    base3_roles = get_base_3(role_info)

    l = []
    for role in roles:
        if not args.base_3 and role in base3_roles:
            continue

        if args.download:
            get_asset(role, role_info)

        try:
            with open(f"assets/descriptions/{role}.txt") as description:
                try:
                    with open(f"assets/count/{role}.txt") as cnt_file:
                        cnt = int(cnt_file.read())
                except IOError:
                    cnt = 1

                ins = {
                    "description": description.read(),
                    "name": role,
                    "img": f"assets/icons/{role}.webp",
                }

                for _ in range(cnt):
                    l.append(ins)
        except:
            print(f"{role} not present as asset", file=sys.stderr)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(""))
    template = env.get_template("tokens.html.j2")
    content = template.render({"roles": l}, size=150)
    print(content)


if __name__ == "__main__":
    main()
