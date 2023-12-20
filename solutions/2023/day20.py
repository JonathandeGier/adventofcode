from Table import Table
from time import time
from collections import deque
from collections import defaultdict
import math

BROADCASTER = 'broadcaster'
FLIP_FLOP = '%'
CONJUNCTION = '&'

LOW = 'low'
HIGH = 'high'

TOGGLE = {
    LOW: HIGH,
    HIGH: LOW,
}

class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "Pulse Propagation"
        self.input = self.getInput(self.day)

        self.modules = {}
        self.module_states = {}

        self.rx_source = None
        self.rx_sources = []

    
    def parse_modules(self):
        self.modules = {}
        self.rx_source = None
        self.rx_sources = []

        # parse the modules
        for line in self.input.splitlines():
            left, right = line.split(' -> ')
            if left[0] in '%&':
                _type = left[0]
                name = left[1:]
            else:
                _type = left
                name = left

            self.modules[name] = (_type, *right.split(', '))

            # initialize the states
            if _type == FLIP_FLOP:
                self.module_states[name] = LOW
            elif _type == CONJUNCTION:
                self.module_states[name] = {}

        # initialize the conjunction states
        for module_name in self.modules:
            for destination_module in self.modules[module_name][1:]:
                if destination_module in self.module_states and type(self.module_states[destination_module]) == dict:
                    self.module_states[destination_module][module_name] = LOW

        # Find the module that sends a pulse to rx
        for module_name in self.modules:
            if 'rx' in self.modules[module_name]:
                if self.rx_source is None:
                    assert self.modules[module_name][0] == CONJUNCTION, 'rx source not a conjunction'
                    self.rx_source = module_name
                else:
                    assert False, 'Multiple inputs in rx'

        # Find the modules that sends a pulse to the modules that sends a pulse to rx
        assert self.rx_source is not None, 'rx source not found'
        for module_name in self.modules:
            if self.rx_source in self.modules[module_name]:
                self.rx_sources.append(module_name)        
             

    def push_buttons(self):
        total_pulses = {LOW: 0, HIGH: 0}
        part1 = None
        
        part2 = None
        low_pulses = defaultdict(int)
        last_low_pulse = {}
        pulse_cycle = []

        button_push = 0
        while True:
            button_push += 1
            queue = deque()
            queue.append(('button', LOW, BROADCASTER))
            pulses = {LOW: 0, HIGH: 0}

            while queue:
                # get the next pulse to process
                source, strength, module_name = queue.popleft()
                pulses[strength] += 1

                # part 2 magic
                if strength == LOW:
                    if module_name in last_low_pulse and low_pulses[module_name] == 2 and module_name in self.rx_sources:
                        pulse_cycle.append(button_push - last_low_pulse[module_name])
                    
                    last_low_pulse[module_name] = button_push
                    low_pulses[module_name] += 1

                if len(pulse_cycle) == len(self.rx_sources):
                    part2 = math.lcm(*pulse_cycle)

                # rx has no next module, so skip it
                if module_name not in self.modules:
                    continue

                module = self.modules[module_name]

                # Broadcast logic
                if module[0] == BROADCASTER:
                    for destination in module[1:]:
                        queue.append((module_name, strength, destination))
                
                # Flip Flop logic
                elif module[0] == FLIP_FLOP:
                    if strength == LOW:
                        self.module_states[module_name] = TOGGLE[self.module_states[module_name]]
                        new_strength = self.module_states[module_name]
                        for destination in module[1:]:
                            queue.append((module_name, new_strength, destination))
                
                # Conjunction logic
                elif module[0] == CONJUNCTION:
                    assert source in self.module_states[module_name]
                    self.module_states[module_name][source] = strength
                    if all([mem == HIGH for mem in self.module_states[module_name].values()]):
                        new_strength = LOW
                    else:
                        new_strength = HIGH

                    for destination in module[1:]:
                        queue.append((module_name, new_strength, destination))
                else:
                    assert False, f'Unknown module type: {module[0]}'

            # part 1 answer
            total_pulses[LOW] += pulses[LOW]
            total_pulses[HIGH] += pulses[HIGH]
            if button_push == 1000:
                part1 = total_pulses[LOW] * total_pulses[HIGH]

            # break if both parts solved
            if part1 is not None and part2 is not None:
                break

        return part1, part2


    def solve(self):
        start_time = time()

        self.parse_modules()
        
        part1, part2 = self.push_buttons()

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
