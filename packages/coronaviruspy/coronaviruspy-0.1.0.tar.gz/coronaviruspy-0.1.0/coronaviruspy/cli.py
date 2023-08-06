import click
import requests
from bs4 import BeautifulSoup


def design(text, country, info):
    print("-" * 20)
    print()
    print(f"{text} in {country}: {info}")
    print()
    print("-" * 20)


@click.command()
@click.option(
    "--country", help="Country to show info about - default: world", default="world"
)
@click.option(
    "--type", help="Which info should be showned - default: cases", default="cases"
)
def coronavirus(country, type):
    """Shows coronavirus info about country"""
    r = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(r.content, "html.parser")
    if country == "world":
        stats = soup.find_all("div", class_="maincounter-number")
        if type == "cases":

            return design("Total cases", "the World", stats[0].text.strip())
        if type == "dead":
            return design("Dead people", "the World", stats[1].text.strip())
        if type == "recovered":
            return design("Recovered people", "the World", stats[2].text.strip())
        if type == "infected":
            return design(
                "Infected people",
                "the World",
                soup.find("div", class_="number-table-main").text.strip(),
            )
        if type == "closed-cases":
            return design(
                "Closed cases",
                "the World",
                soup.find_all("div", class_="number-table-main")[1].text.strip(),
            )

    try:
        tab = soup.find("a", string=country.capitalize()).parent.parent
        index_list = [2, 3, 4, 5, 6, 7, 8]
    except AttributeError:
        try:
            tab = soup.find("td", string=country.capitalize()).parent
            index_list = [1, 2, 3, 4, 5, 6, 7]
        except AttributeError:
            print(f"ERROR: There aren't any ill people in {country} or {country} isn't valid country")
            return
    stats = tab.find_all()

    if type == "cases":
        return design("Total cases", country, stats[index_list[0]].text.strip())
    if type == "new-cases":
        if stats[index_list[1]].text.strip():
            return design("New cases", country, stats[index_list[1]].text.strip())
        return design("There aren't any new cases", country, "")
    if type == "dead":
        if stats[index_list[2]].text.strip():
            return design("Dead people", country, stats[index_list[2]].text.strip())
        return design("There aren't any dead people", country, "")
    if type == "new-deads":
        if stats[index_list[3]].text.strip():
            return design("New deads", country, stats[index_list[3]].text.strip())
        return design("There aren't any new deads", country, "")
    if type == "recovered":
        if stats[index_list[2]].text.strip():
            return design("Recovered people", country, stats[index_list[3]].text.strip())
        return design("There aren't any recovered people", country, "")

    if type == "infected":
        if stats[index_list[3]].text.strip():
            return design("Infected people", country, stats[index_list[4]].text.strip())
        return design("There aren't any infected people", country, "")
