import requests

text = requests.get("https://adventofcode.com/2021/day/1/input").text

print(text)