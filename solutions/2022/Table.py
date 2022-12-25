import requests
import os


class Table:

    def getInput(self, day):
        directory = "solutions/2022/input/"
        file_location = directory + "input" + str(day) + ".txt"

        # if the input file already exists, return the file
        if os.path.isfile(file_location):
            with open(file_location, 'r') as input_file:
                return input_file.read()

        # read the env file 
        with open('env', 'r') as env_file:
            env = {}
            for line in env_file.read().splitlines():
                key, value = line.split('=')
                env[key] = value

        # validate the env file
        if 'session' not in env:
            raise Exception("'session' is required in the env to automatically load input")

        if 'contact' not in env or env['contact'] == '':
            raise Exception("Please provide contact information in the env file as per Topaz's request: https://www.reddit.com/r/adventofcode/comments/z9dhtd/please_include_your_contact_info_in_the_useragent/")

        # request the input file
        url = "https://adventofcode.com/2022/day/" + str(day) + "/input"
        headers = { 'User-Agent': 'https://github.com/JonathandeGier/adventofcode by ' + env['contact'] }
        cookies = { 'session': env['session'] }

        text = requests.get(url, headers=headers, cookies=cookies).text

        # store the input file
        if not os.path.isdir(directory):
            os.mkdir(directory)

        with open(file_location, 'w') as write_input_file:
            write_input_file.write(text)

        return text

    def visual_path(self, name: str):
        directory = 'solutions/2022/visuals/'
        if not os.path.isdir(directory):
            os.mkdir(directory)

        directory += 'day' + str(self.day) + '/'
        if not os.path.isdir(directory):
            os.mkdir(directory)

        return directory + name

    def headers(self):
        return ("Day", "Title", "Part 1", "Part 2", "Time (s)")

    def printRow(self, values, end = "\n"):
        if values[0] == self.headers()[0]:
            print("")
        print(self.format(values), end=end)

    def format(self, values):
        return f"{values[0]:<5} {values[1]:<40} {values[2]:<30} {values[3]:<30} {values[4]:<20}"