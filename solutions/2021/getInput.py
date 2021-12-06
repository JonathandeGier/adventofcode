import requests
import os

def get_input(year, day):

    file_location = "solutions/" + str(year) + "/input/input" + str(day) + ".txt"

    if os.path.isfile(file_location):
        return open(file_location, "r").read()

    session = open("session", "r").read()

    url = "https://adventofcode.com/" + str(year) + "/day/" + str(day) + "/input"

    text = requests.get(url, cookies={"session": session}).text

    file = open(file_location, "w")
    file.write(text)
    file.close()

    return text