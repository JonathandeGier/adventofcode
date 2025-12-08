from Table import Table
from time import time
from itertools import combinations
from collections import defaultdict

class Box:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

        self.circuit = None

    def distance(self, other) -> float:
        if type(other) != Box:
            assert False, 'Other value must be a box'

        return ((self.x - other.x) ** 2) + ((self.y - other.y) ** 2) + ((self.z - other.z) ** 2)
    
    def set_circuit(self, circuit):
        self.circuit = circuit
    
    def __hash__(self):
        return (self.x, self.y, self.z)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        circuit = 'None'
        if self.circuit != None:
            circuit = self.circuit.id

        return f'Box[x={self.x},y={self.y},z={self.z},circuit={circuit}]'


class Circuit:
    def __init__(self, id: int):
        self.id = id

        self.boxes = []

    def add_box(self, box: Box):
        self.boxes.append(box)
        box.set_circuit(self)

    def merge(self, other):
        if type(other) != Circuit:
            assert False, 'Other value must be a circuit'

        # print(other.boxes)
        for box in other.boxes:
            self.add_box(box)

    def __hash__(self):
        return self.id
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'Circuit[id={self.id},boxes={len(self.boxes)}]'


class Day8(Table):

    def __init__(self):
        self.day = 8
        self.title = "Playground"
        self.input = self.getInput(self.day)

    def solve(self):
        start_time = time()

        boxes = []
        for line in self.input.splitlines():
            x, y, z = line.split(',')

            boxes.append(Box(int(x), int(y), int(z)))


        distances = []
        distance_pairs = defaultdict(lambda: [])
        for box1, box2 in combinations(boxes, 2):
            distance = box1.distance(box2)
            distances.append(distance)
            distance_pairs[distance].append((box1, box2))

        distances.sort()

        part1 = 1
        part2 = 0
        done = False
        circuits = []
        next_circuit_id = 0
        connections = 0
        for distance in distances:
            for box1, box2 in distance_pairs[distance]:
                if box1.circuit == None and box2.circuit == None:
                    circuit = Circuit(next_circuit_id)
                    circuits.append(circuit)
                    next_circuit_id += 1

                    circuit.add_box(box1)
                    circuit.add_box(box2)
                    connections += 1
                elif box1.circuit == None:
                    circuit = box2.circuit
                    circuit.add_box(box1)
                    connections += 1
                elif box2.circuit == None:
                    circuit = box1.circuit
                    circuit.add_box(box2)
                    connections += 1
                elif box1.circuit != None and box2.circuit != None:
                    circuit1 = box1.circuit
                    circuit2 = box2.circuit

                    connections += 1
                    if circuit1 == circuit2:
                        continue

                    circuit1.merge(circuit2)
                    circuits.remove(circuit2)
                else:
                    assert False, 'Impossible'

                if connections == 1000:
                    sizes = sorted(list(set(len(circuit.boxes) for circuit in circuits)), reverse=True)
                    for size in sizes[:3]:
                        part1 *= size
                elif all([box.circuit != None for box in boxes]):
                    done = True
                    part2 = box1.x * box2.x
                    break

            if done:
                break


        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day8()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
