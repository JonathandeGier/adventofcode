from numpy import product
from Table import Table
from time import time

class Bot:
    def __init__(self, id: int):
        self.id = id
        self.low = None
        self.high = None
        self.chips = []

    def setOutputs(self, outputLow, outputHigh):
        self.low = outputLow
        self.high = outputHigh

    def append(self, chip: int):
        assert len(self.chips) < 2
        self.chips.append(chip)

    def give(self) -> tuple:
        if len(self.chips) != 2:
            return (False, None)

        low = min(self.chips)
        high = max(self.chips)

        self.low.append(low)
        self.high.append(high)

        part1 = None
        if 61 in self.chips and 17 in self.chips:
            part1 = self.id

        self.chips = []

        return (True, part1)


class Day10(Table):

    def __init__(self):
        self.day = 10
        self.title = "Balance Bots"
        self.input = self.getInput(self.day)
        self.bots = {}
        self.outputs = {}

    def load_bots(self):
        # parse input
        values = [] # value = (bot_id, chip_value)
        bots = [] # temp bots
        outputs = [] # int array
        for line in self.input.splitlines():
            segments = line.split(" ")
            if segments[0] == "value":
                values.append((int(segments[-1]), int(segments[1])))

            elif segments[0] == "bot":
                bot_id = int(segments[1])
                low_id = int(segments[6])
                high_id = int(segments[11])

                if segments[5] == "bot":
                    low_target = "b"
                else:
                    low_target = "o"
                    outputs.append(low_id)

                if segments[10] == "bot":
                    high_target = "b"
                else:
                    high_target = "o"
                    outputs.append(high_id)

                bots.append((bot_id, low_target, low_id, high_target, high_id))

            else:
                assert False, "unable to parse line"

        # initialize bots
        for tmp_bot in bots:
            bot_id = tmp_bot[0]
            self.bots[bot_id] = Bot(bot_id)

        # initialize outputs
        for output_id in outputs:
            self.outputs[output_id] = []
        
        # initialize bot outputs
        for tmp_bot in bots:
            bot = self.bots[tmp_bot[0]]

            if tmp_bot[1] == "b":
                low_output = self.bots[tmp_bot[2]]
            else:
                low_output = self.outputs[tmp_bot[2]]

            if tmp_bot[3] == "b":
                high_output = self.bots[tmp_bot[4]]
            else:
                high_output = self.outputs[tmp_bot[4]]

            bot.setOutputs(low_output, high_output)

        # initialize bot values
        for value in values:
            bot = self.bots[value[0]]
            bot.append(value[1])

    def product(self, array: list) -> int:
        product = 1
        for val in array:
            product *= val
        return product

    def solve(self):
        start_time = time()

        self.load_bots()

        part1 = "None"
        has_given = True
        while has_given:
            has_given = False
            for bot_id in self.bots:
                bot = self.bots[bot_id]
                result = bot.give()

                has_given = has_given or result[0]

                if result[1] != None:
                    part1 = result[1]

        part2 = str(self.product([self.product(self.outputs[0]), self.product(self.outputs[1]), self.product(self.outputs[2])]))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day10()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
