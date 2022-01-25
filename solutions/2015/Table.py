import requests
import os


class Table:

    def getInput(self, day):
        file_location = "solutions/2015/input/input" + str(day) + ".txt"

        if os.path.isfile(file_location):
            return open(file_location, "r").read()

        session = open("session", "r").read()

        url = "https://adventofcode.com/2015/day/" + str(day) + "/input"

        text = requests.get(url, cookies={"session": session}).text

        file = open(file_location, "w")
        file.write(text)
        file.close()

        return text

    def headers(self):
        return ("Day", "Title", "Part 1", "Part 2", "Time (s)")

    def printRow(self, values):
        if values[0] == self.headers()[0]:
            print("")
        print(self.format(values), end="")

    def format(self, values):
        return f"{values[0]:<5} {values[1]:<40} {values[2]:<15} {values[3]:<15} {values[4]:<20}\n"