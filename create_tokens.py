import argparse
import jinja2
import sys
import json
import requests


def get_base_3():
    res = requests.get(
        "https://script.bloodontheclocktower.com/data/roles.json"
    )
    return [x["id"] for x in res.json() if "Experimental" not in x["version"]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-3", action="store_true")
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as description:
        roles = json.load(description)[1::]

    base3_roles = get_base_3()

    l = []
    for role in roles:
        if not args.base_3 and role in base3_roles:
            continue

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
