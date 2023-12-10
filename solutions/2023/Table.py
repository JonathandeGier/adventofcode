import requests
import os

from PIL import Image

class Table:

    def getInput(self, day):
        directory = "solutions/2023/input/"
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
            raise Exception("Please provide contact information to comply with automation guidelines: https://www.reddit.com/r/adventofcode/comments/z9dhtd/please_include_your_contact_info_in_the_useragent/")

        # request the input file
        url = "https://adventofcode.com/2023/day/" + str(day) + "/input"
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
        directory = 'solutions/2023/visuals/'
        if not os.path.isdir(directory):
            os.mkdir(directory)

        directory += 'day' + str(self.day) + '/'
        if not os.path.isdir(directory):
            os.mkdir(directory)

        return directory + name
    
    def bounds(self, data: map):
        min_x = min([coord[0] for coord in data.keys()])
        max_x = max([coord[0] for coord in data.keys()])
        min_y = min([coord[1] for coord in data.keys()])
        max_y = max([coord[1] for coord in data.keys()])

        return (min_x, max_x, min_y, max_y)

    def image_map(self, data: map, colors: map, bounds: tuple = None, scale: int = 1):
        # bounds = None
        # scale = 1
        # if 'bounds' in kwargs:
        #     bounds = kwargs['bounds']
        # if 'scale' in kwargs:
        #     scale = kwargs['scale']

        if bounds is None:
            bounds = self.bounds(data)

        img = Image.new('RGB', (bounds[1] - bounds[0] + 1, bounds[3] - bounds[2] + 1), "black")
        pixels = img.load()
        for position in data:
            if data[position] in colors:
                pixel = position[0] - bounds[0], position[1] - bounds[2]
                pixels[pixel] = colors[data[position]]

        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)
        return img


    def headers(self):
        return ("Day", "Title", "Part 1", "Part 2", "Time (s)")

    def printRow(self, values, end = "\n"):
        if values[0] == self.headers()[0]:
            print("")
        print(self.format(values), end=end)

    def format(self, values):
        return f"{values[0]:<5} {values[1]:<40} {values[2]:<30} {values[3]:<30} {values[4]:<20}"