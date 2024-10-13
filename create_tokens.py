import jinja2
import sys
import json


def main():
    if len(sys.argv) != 2:
        print("Provide exactly 1 argument", file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as description:
        roles = json.load(description)[1::]

    l = []
    for role in roles:
        try:
            with open(f"assets/descriptions/{role}.txt") as description:
                l.append(
                    {
                        "description": description.read(),
                        "name": role,
                        "img": f"assets/icons/{role}.webp",
                    }
                )
        except:
            print(f"{role} not present as asset", file=sys.stderr)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(""))
    template = env.get_template("tokens.html.j2")
    content = template.render({"roles": l}, size=150)
    print(content)


if __name__ == "__main__":
    main()
