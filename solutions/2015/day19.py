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
        
        self.steps = None

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

                reverse_replacements[to_] = from_
            else:
                molecule = line.strip()

        return replacements, reverse_replacements, molecule

    def part_in_any_replacement(self, part):
        for val in self.reverse_replacements.keys():
            if part in val:
                return True
        return False


    def decode(self, sequence: str):
        from_i = 0
        to_i = 1
        while to_i <= len(sequence):
            part = sequence[from_i:to_i]
            part_plus_one = sequence[from_i:to_i+1]

            last_letter = part_plus_one[-1]
            if last_letter == last_letter.lower():
                to_i += 1
                continue

            if self.part_in_any_replacement(part) and not self.part_in_any_replacement(part_plus_one) and part not in self.reverse_replacements:
                from_i = to_i
            if part in self.reverse_replacements:
                # sequence = sequence.replace(part, reverse_replacements[part], 1)
                sequence = sequence[:from_i] + self.reverse_replacements[part] + sequence[to_i:]
                self.steps += 1
                from_i = 0
                to_i = 1
                continue
            
            to_i += 1


    def decode_from_back(self, sequence: str):

        from_i = len(sequence) - 1
        to_i = len(sequence)
        while from_i >= 0:
            part = sequence[from_i:to_i]
            part_plus_one = sequence[from_i-1:to_i]

            if self.part_in_any_replacement(part) and not self.part_in_any_replacement(part_plus_one) and part not in self.reverse_replacements:
                to_i = from_i
            if part in self.reverse_replacements:
                sequence = sequence.replace(part, self.reverse_replacements[part], 1)
                self.steps += 1
                from_i = len(sequence) - 1
                to_i = len(sequence)
                continue
            
            from_i -= 1

    def solve(self):
        start_time = time()

        self.replacements, self.reverse_replacements, self.molecule_to_make = self.get_data()

        mol_elements = re.findall("[A-Z][^A-Z]*", self.molecule_to_make)

        after_one_replacement = set()
        for i in range(len(mol_elements)):
            if mol_elements[i] in self.replacements:
                tmp_mol = mol_elements.copy()
                for rep in self.replacements[mol_elements[i]]:
                    tmp_mol[i] = rep
                    mol = "".join(tmp_mol)
                    after_one_replacement.add(mol)
        part1 = len(after_one_replacement)

        self.steps = 0
        self.decode(self.molecule_to_make)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, "- 207 -", seconds_elapsed)


if __name__ == "__main__":
    day = Day19()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
