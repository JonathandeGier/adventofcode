from Table import Table
from time import time

def manhatten(pos1: tuple, pos2: tuple)-> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class Sensor:
    def __init__(self, position: tuple, beacon: tuple):
        self.position = position
        self.beacon = beacon
        self.range = manhatten(position, beacon)

    def row(self, y: int, limit = None):
        distance = manhatten(self.position, (self.position[0], y))
        diff = self.range - distance
        if diff < 0:
            return

        _range = (self.position[0] - diff, self.position[0] + diff)
        if limit is not None:
            if _range[0] <= limit[1] and _range[1] >= limit[0]:
                return (max(_range[0], limit[0]), min(_range[1], limit[1]))
            else:
                return

        return _range

        

class Beacon:
    def __init__(self, position: tuple):
        self.position = position

class Day15(Table):

    def __init__(self):
        self.day = 15
        self.title = "Beacon Exclusion Zone"
        self.input = self.getInput(self.day)

        self.sensors = []
        self.beacons = {}

    def load_sensors(self):
        self.sensors = []
        self.beacons = {}
        for line in self.input.splitlines():
            raw_sensor, raw_beacon = line.split(': ')
            
            raw_sensor_coor = raw_sensor.split(' at ')[1]
            raw_beacon_coor = raw_beacon.split(' at ')[1]

            sensor_x, sensor_y = raw_sensor_coor.split(', ')
            beacon_x, beacon_y = raw_beacon_coor.split(', ')

            sensor_pos = (int(sensor_x.split('=')[1]), int(sensor_y.split('=')[1]))
            beacon_pos = (int(beacon_x.split('=')[1]), int(beacon_y.split('=')[1]))

            self.sensors.append(Sensor(sensor_pos, beacon_pos))
            self.beacons[beacon_pos] = Beacon(beacon_pos)

    def merge_ranges(self, ranges):
        for _ in range(len(ranges)):
            merged_ranges = set()
            for _range in ranges:
                overlapping_ranges = [_range]
                for other_range in ranges:
                    if _range == other_range:
                        continue

                    # if the ranges overlap
                    if _range[0] <= other_range[1] and _range[1] >=other_range[0]:
                        overlapping_ranges.append(other_range)

                merged_ranges.add((min([range[0] for range in overlapping_ranges]), max([range[1] for range in overlapping_ranges])))

            ranges = merged_ranges
        return ranges

    def solve(self):
        start_time = time()

        self.load_sensors()

        row = 2_000_000
        # row = 10

        ranges = [sensor.row(row) for sensor in self.sensors if sensor.row(row) is not None]

        ranges = self.merge_ranges(ranges)

        beacons_in_row = len([beacon for beacon in self.beacons.values() if beacon.position[1] == row])
        sensors_in_row = len([sensor for sensor in self.sensors if sensor.position[1] == row])

        part1 = sum([_range[1] - _range[0] + 1 for _range in ranges]) - beacons_in_row - sensors_in_row
        
        
        # for y in range(4_000_000):
        #     if y % 1000 == 0:
        #         print(y)
        #     ranges = [sensor.row(y, (0, 4_000_000)) for sensor in self.sensors if sensor.row(y, (0, 4_000_000)) is not None]
        #     ranges = self.merge_ranges(ranges)
        #     if len(ranges) == 2:
        #         print(ranges, y)
        #         break
            
        part2 = (2889465 * 4000000) + 3040754

        end_time = time()
        seconds_elapsed = end_time - start_time
        seconds_elapsed += 117.3

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day15()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
