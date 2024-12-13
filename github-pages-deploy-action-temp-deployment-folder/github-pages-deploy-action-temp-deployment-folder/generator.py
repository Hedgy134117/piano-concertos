import csv
import random
from datetime import date, timedelta

import jinja2


def load_data() -> dict:
    data = {}
    with open("output.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        for row in reader:
            data[row[0]] = row[1].split("|")

    return data


def remove_composition(data: dict, composer: str, composition: str) -> None:
    data[composer].remove(composition)
    if len(data[composer]) == 0:
        del data[composer]


data = load_data()

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
template = env.get_template("template.html")

start = date(2025, 1, 1)
end = date(2026, 1, 1)

days = []
while start < end:
    composer, composition = random.choice(list(data.items()))
    composition = random.choice(composition)
    remove_composition(data, composer, composition)
    days.append(
        {
            "composer": composer,
            "composition": composition,
            "date": start.strftime("%m-%d"),
        }
    )
    start += timedelta(days=1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(template.render(days=days))
