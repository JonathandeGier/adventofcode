from Table import Table
from time import time

class Day5(Table):

    def __init__(self):
        self.day = 5
        self.title = "If You Give A Seed A Fertilizer"
        self.input = self.getInput(self.day)

        self.seeds = []
        self.category_mapping = {}
        self.mappings = {}


    def parse_mappings(self):
        self.seeds = []
        self.category_mapping = {}
        self.mappings = {}

        groups = self.input.split('\n\n')
        _seeds = groups[0]
        self.seeds = [int(x) for x in _seeds.split(': ')[1].split()]
        
        mappings = groups[1:]
        for mapping in mappings:
            lines = mapping.splitlines()
            name = lines[0].split(' ')[0].split('-')
            _from = name[0]
            _to = name[-1]

            self.category_mapping[_from] = _to
            self.mappings[_to] = {}

            for values in lines[1:]:
                to_start, from_start, length = values.split()
                self.mappings[_to][int(from_start), int(length)] = (int(to_start), int(length))


    def find_value(self, current_value: int, current_type: str, target_type: str) -> int:
        if current_type == target_type:
            return current_value
        
        assert current_type in self.category_mapping, "Invalid current type"

        next_type = self.category_mapping[current_type]

        available_keys = [key for key in self.mappings[next_type].keys() if key[0] <= current_value and current_value - key[0] < key[1]]
        
        if len(available_keys) == 0:
            return self.find_value(current_value, next_type, target_type)
        else:
            assert len(available_keys) == 1, 'Multiple keys found'
            key = available_keys[0]
            map_value = self.mappings[next_type][key]

            next_value = current_value + (map_value[0] - key[0])

            return self.find_value(next_value, next_type, target_type)
        

    def find_ranges(self, current_range: tuple, current_type: str, target_type: str) -> list:
        if current_type == target_type:
            return [current_range]
        
        assert current_type in self.category_mapping, "Invalid current type"

        next_type = self.category_mapping[current_type]

        next_ranges = []
        current_val = current_range[0]
        while current_val < current_range[1]:
            in_range_keys = [key for key in self.mappings[next_type].keys() if key[0] <= current_val and current_val - key[0] < key[1]]
            if len(in_range_keys) == 0:
                # not in range? find next start of range
                next_range_starts = [key[0] for key in self.mappings[next_type].keys() if key[0] >= current_val]
                if len(next_range_starts) > 0:
                    source_max = min(next_range_starts) - 1

                    next_ranges.append((current_val, source_max))

                    current_val = source_max + 1
                else:
                    # no next range, fill to max
                    next_ranges.append((current_val, current_range[1]))
                    current_val = current_range[1] + 1
            else:
                assert len(in_range_keys) == 1, 'Multiple keys found'
                key = in_range_keys[0]
                # print(key)
                map_value = self.mappings[next_type][key]

                new_range_min = current_val + (map_value[0] - key[0])

                source_max = min(current_range[1], (key[0] + key[1] - 1)) # current range max or key range max, lowest of two
                new_range_max = source_max + (map_value[0] - key[0])

                next_ranges.append((new_range_min, new_range_max))
                current_val = source_max + 1

        result_ranges = []
        for next_range in next_ranges:
            result_ranges.extend(self.find_ranges(next_range, next_type, target_type))

        return result_ranges


    def solve(self):
        start_time = time()

        self.parse_mappings()

        part1 = min([self.find_value(val, 'seed', 'location') for val in self.seeds])

        min_locations = []
        for i in range(0, len(self.seeds), 2):
            _range = (self.seeds[i], self.seeds[i] + self.seeds[i+1] - 1)

            min_locations.append(min([result[0] for result in self.find_ranges(_range, 'seed', 'location')]))

        part2 = min(min_locations)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day5()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
