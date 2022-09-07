import requests
import os


class Table:

    def getInput(self, day):
        directory = "solutions/2018/input/"
        file_location = directory + "input" + str(day) + ".txt"

        if os.path.isfile(file_location):
            return open(file_location, "r").read()

        session = open("session", "r").read()

        url = "https://adventofcode.com/2018/day/" + str(day) + "/input"

        text = requests.get(url, cookies={"session": session}).text

        if not os.path.isdir(directory):
            os.mkdir(directory)

        file = open(file_location, "w")
        file.write(text)
        file.close()

        return text

    def headers(self):
        return ("Day", "Title", "Part 1", "Part 2", "Time (s)")

    def printRow(self, values, end = "\n"):
        if values[0] == self.headers()[0]:
            print("")
        print(self.format(values), end=end)

    def format(self, values):
        return f"{values[0]:<5} {values[1]:<40} {values[2]:<18} {values[3]:<34} {values[4]:<20}"