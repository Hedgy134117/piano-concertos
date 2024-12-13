import csv
import re
from pprint import pprint
from typing import Any

import requests
from bs4 import BeautifulSoup, ResultSet, Tag


def get_composer_name(tag: Tag) -> str:
    if tag == None or tag.name != "li":
        return ""

    if tag.find("a"):
        return tag.find("a").text
    return tag.text


def get_compositions(tag: Tag) -> list[str]:
    if tag == None or tag.name != "ul":
        return []

    compositions = []
    for comp in tag.find_all("li"):
        text = comp.text

        # remove citations
        text = re.sub(r"\[.*\]", "", text)

        compositions.append(text)

    return compositions


def get_composers_compositions(letters: list[ResultSet[Tag]]) -> dict:
    result = {}
    for letter in letters:
        composerTags = letter.find_all("li", recursive=False)

        if composerTags[0].find("a") != None:
            if (
                composerTags[0].find("a").text
                == "List of compositions for keyboard and orchestra"
            ):
                break

        composers = [get_composer_name(li) for li in composerTags]
        compositions = [
            get_compositions(ul) for ul in map(lambda x: x.find("ul"), composerTags)
        ]

        for i in range(len(composers)):
            result[composers[i]] = compositions[i]

    return result


def composers_compositions_csv(data: dict, name: str) -> None:
    with open(name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["composer", "compositions"])

        for composer, compositions in data.items():
            writer.writerow([composer, "|".join(compositions)])


if __name__ == "__main__":
    soup = BeautifulSoup(
        requests.get(
            "https://en.wikipedia.org/wiki/List_of_compositions_for_piano_and_orchestra"
        ).content,
        features="html.parser",
    )

    letters: ResultSet[Tag] = soup.find("div", {"class": "mw-content-ltr"}).find_all(
        "ul", recursive=False
    )

    result = get_composers_compositions(letters)
    composers_compositions_csv(result, "output.csv")
