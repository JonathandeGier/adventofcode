from Table import Table
from time import time

class Day14(Table):

    def __init__(self):
        self.day = 14
        self.title = "Reindeer Olympics"
        self.input = self.getInput(self.day)

    def get_reindeer(self):
        reindeers = {}
        for line in self.input.splitlines():
            segments = line.split(" ")
            name = segments[0]
            speed = int(segments[3])
            stamina = int(segments[6])
            recover = int(segments[13])
            reindeers[name] = {"speed": speed, "stamina": stamina, "recover": recover, "distance": 0, "state": "fly", "cooldown": stamina, "points": 0}

        return reindeers

    def solve(self):
        start_time = time()

        reindeers = self.get_reindeer()

        most_distance = 0
        most_points = 0
        for _ in range(2503):
            leading_deers = []
            distance = 0

            for reindeer_name in reindeers:
                reindeer = reindeers[reindeer_name]
                reindeer["cooldown"] -= 1

                if reindeer["state"] == "fly":
                    reindeer["distance"] += reindeer["speed"]

                if reindeer["cooldown"] == 0:
                    if reindeer["state"] == "fly":
                        reindeer["state"] = "rest"
                        reindeer["cooldown"] = reindeer["recover"]
                    else:
                        reindeer["state"] = "fly"
                        reindeer["cooldown"] = reindeer["stamina"]

                if reindeer["distance"] > most_distance:
                        most_distance = reindeer["distance"]

                if reindeer["distance"] > distance:
                    leading_deers = [reindeer_name]
                    distance = reindeer["distance"]
                elif reindeer["distance"] == distance:
                    leading_deers.append(reindeer_name)

            for deer in leading_deers:
                reindeers[deer]["points"] += 1
                if reindeers[deer]["points"] > most_points:
                    most_points = reindeers[deer]["points"]

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, most_distance, most_points, seconds_elapsed)


if __name__ == "__main__":
    day = Day14()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
