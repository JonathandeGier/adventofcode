import heapq
import re
from Table import Table
from time import time


class Day19(Table):

    def __init__(self):
        self.day = 19
        self.title = "Medicine for Rudolph"
        self.input = self.getInput(self.day)

        self.replacements = None
        self.reverse_replacements = None
        self.molecule_to_make = None

    def get_lines(self):
        lines = self.input.splitlines()
        return lines

    def get_data(self):
        replacements = {}
        reverse_replacements = {}
        molecule = ""

        do_replacements = True
        for line in self.input.splitlines():
            if line == "":
                do_replacements = False
                continue

            if do_replacements:
                from_, to_ = line.split(" => ")
                if from_ in replacements:
                    replacements[from_].append(to_)
                else:
                    replacements[from_] = [to_]

                reverse_replacements[tuple(self.seq_to_array(to_))] = from_
            else:
                molecule = line.strip()

        return replacements, reverse_replacements, molecule


    def seq_to_array(self, sequence: str) -> list:
        return re.findall("[A-Z][^A-Z]*", sequence)


    def product(self, array: list) -> int:
        product = 1
        for num in array:
            product *= num
        return product


    def count_transforms(self, sequence: list) -> int:
        transforms = 0
        for element in sequence:
            if type(element) == dict:
                transforms += 1
                transforms += self.count_transforms(list(element.values())[0])
        return transforms


    def value(self, element):
        if type(element) == str:
            return element
        elif type(element) == dict:
            return list(element.keys())[0]
        else:
            assert False, type(element)


    def collapse(self, sequence: list) -> list:
        new_sequence = []
        for element in sequence:
            if element == None:
                continue
            new_sequence.append(element)
        return new_sequence


    def top_level_sequence(self, sequence: list) -> list:
        new_sequence = []
        for element in sequence:
            if type(element) == dict:
                new_sequence.append(list(element.keys())[0])
            else:
                new_sequence.append(element)
        return new_sequence


    def detransform(self, sequence: list, part: tuple):
        sequence = sequence.copy()
        sub_sequence = sequence[part[0]:part[1]]
        transform_key = tuple([self.value(element) for element in sub_sequence])
        
        if transform_key not in self.reverse_replacements:
            assert False, "Not able to detransform " + str(transform_key)

        transform_result = self.reverse_replacements[transform_key]
        new_sub_sequence = {transform_result: sub_sequence}

        sequence[part[0]] = new_sub_sequence
        for i in range(part[0] + 1, part[1]):
            sequence[i] = None # parts were calculated based on sequence size, so we need it to stay the same size

        return sequence


    def decode(self, sequence: list):

        # keep track of molecules that have already been calculated with the number of transformations it took to get to that molecule
        # this makes sure that the end result is the shortest way to get to that molecule
        calculated = {}

        h = []
        i = 0
        # use a heap queue (priority queue) so that the molecules closest to the end result will be checked first (i is tie breaker)
        heapq.heappush(h, (0, i, sequence))

        while len(h) > 0:
            prio, _, sequence = heapq.heappop(h)

            calc_key = tuple(self.top_level_sequence(sequence))
            transforms = self.count_transforms(sequence)
            if calc_key in calculated and calculated[calc_key] < transforms:
                continue
            
            if len(sequence) == 1 and 'e' in sequence[0]:
                return sequence

            # find all possible transformations
            possible_transforms = []
            top_level_sequence = self.top_level_sequence(sequence)
            max_result_length = max([len(key) for key in self.reverse_replacements.keys()])
            for from_ in range(len(top_level_sequence)):
                for offset in range(1, max_result_length + 1):
                    to_ = from_ + offset
                    if to_ > len(top_level_sequence):
                        continue

                    part = tuple(top_level_sequence[from_:to_])

                    if part in self.reverse_replacements:
                        possible_transforms.append((from_, to_))
            
            # find overlapping transformations
            grouped_overlaps = []
            for part in possible_transforms:
                if len(grouped_overlaps) == 0:
                    grouped_overlaps.append(part)
                    continue

                if type(grouped_overlaps[-1]) == tuple:
                    if part[0] < grouped_overlaps[-1][1]:
                        grouped_overlaps[-1] = [grouped_overlaps[-1], part]
                    else:
                        grouped_overlaps.append(part)
                elif type(grouped_overlaps[-1]) == list:
                    if part[0] < grouped_overlaps[-1][-1][1]:
                        grouped_overlaps[-1].append(part)
                    else:
                        grouped_overlaps.append(part)

            # split grouped overlaps in overlaps and sure transforms
            overlaps = []
            sure_transforms = []
            for group in grouped_overlaps:
                if type(group) == tuple:
                    sure_transforms.append(group)
                elif type(group) == list:
                    overlaps.append(group)
            
            # apply detransform for single possebility transforms
            for part in sure_transforms:
                sequence = self.detransform(sequence, part)

            # if there are overlaps, apply each overlap per group one by one and add it to the queue if it has not been calculated
            if len(overlaps) > 0:
                for group in overlaps:
                    for part in group:
                        new_sequence = self.collapse(self.detransform(sequence, part))
                        transforms = self.count_transforms(new_sequence)
                        calc_key = tuple(self.top_level_sequence(new_sequence))

                        if calc_key not in calculated or calculated[calc_key] > transforms:
                            calculated[calc_key] = transforms
                            i += 1
                            heapq.heappush(h, (len(new_sequence), i, new_sequence))

            # if there are no overlaps, but there are sure transforms, add it to the queue if it has not been calculated
            elif len(sure_transforms) > 0:
                new_sequence = self.collapse(sequence)
                transforms = self.count_transforms(new_sequence)
                calc_key = tuple(self.top_level_sequence(new_sequence))

                if calc_key not in calculated or calculated[calc_key] > transforms:
                    calculated[calc_key] = transforms
                    i += 1
                    heapq.heappush(h, (len(new_sequence), i, new_sequence))
    

    def solve(self):
        start_time = time()

        self.replacements, self.reverse_replacements, self.molecule_to_make = self.get_data()

        mol_elements = self.seq_to_array(self.molecule_to_make)

        after_one_replacement = set()
        for i in range(len(mol_elements)):
            if mol_elements[i] in self.replacements:
                tmp_mol = mol_elements.copy()
                for rep in self.replacements[mol_elements[i]]:
                    tmp_mol[i] = rep
                    mol = "".join(tmp_mol)
                    after_one_replacement.add(mol)
        part1 = len(after_one_replacement)

        transformations = self.decode(self.seq_to_array(self.molecule_to_make))
        part2 = self.count_transforms(transformations)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
