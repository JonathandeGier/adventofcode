import requests

def get_input(day):
    session = open("session", "r").read()

    text = requests.get("https://adventofcode.com/2021/day/1/input", cookies={"session": session}).text

    return text