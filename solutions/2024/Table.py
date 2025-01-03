import requests
import os

from PIL import Image

class Table:

    def getInput(self, day):
        directory = "solutions/2024/input/"
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
        url = "https://adventofcode.com/2024/day/" + str(day) + "/input"
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
        path = f'solutions/2024/visuals/day{self.day}/' + name
        
        # make directories if they dont exist
        folders = path.split('/')
        for i in range(1, len(folders)):
            sub_directory = '/'.join(folders[:i]) + '/'
            if not os.path.isdir(sub_directory):
                os.mkdir(sub_directory)
        
        return path
    
    def bounds(self, data: map, padding: int = 0):
        min_x = min([coord[0] for coord in data.keys()]) - padding
        max_x = max([coord[0] for coord in data.keys()]) + padding
        min_y = min([coord[1] for coord in data.keys()]) - padding
        max_y = max([coord[1] for coord in data.keys()]) + padding

        return (min_x, max_x, min_y, max_y)

    def image_map(self, data: map, colors: map, bounds: tuple = None, scale: int = 1, padding: int = 0, background_color: tuple = (0, 0, 0)):
        if bounds is None:
            bounds = self.bounds(data, padding)

        img = Image.new('RGB', (bounds[1] - bounds[0] + 1, bounds[3] - bounds[2] + 1), background_color)
        pixels = img.load()
        for position in data:
            if data[position] in colors:
                pixel = position[0] - bounds[0], position[1] - bounds[2]
                pixels[pixel] = colors[data[position]]

        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)
        return img

    def image_grid(self, data: list, colors: map, scale: int = 1, background_color: tuple = (0, 0, 0)):
        img = Image.new('RGB', (len(data[0]), len(data)), background_color)
        pixels = img.load()
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val in colors:
                    pixels[i, j] = colors[val]
        
        img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.Resampling.NEAREST)
        return img


    def headers(self):
        return ("Day", "Title", "Part 1", "Part 2", "Time (s)")

    def printRow(self, values, end = "\n"):
        if values[0] == self.headers()[0]:
            print("")
        print(self.format(values), end=end)

    def format(self, values):
        return f"{values[0]:<5} {values[1]:<40} {values[2]:<30} {values[3]:<40} {values[4]:<20}"