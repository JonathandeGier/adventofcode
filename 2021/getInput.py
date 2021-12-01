import requests

def get_input(year, day):
    session = open("session", "r").read()

    url = "https://adventofcode.com/" + str(year) + "/day/" + str(day) + "/input"

    text = requests.get(url, cookies={"session": session}).text

    return text