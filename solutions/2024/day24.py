from Table import Table
from time import time

class Day24(Table):

    def __init__(self):
        self.day = 24
        self.title = "Crossed Wires"
        self.input = self.getInput(self.day)

    def evaluate(self, wire, gates, wires):
        gate = gates[wire]
        
        if wires[gate[1]] == None:
            self.evaluate(gate[1], gates, wires)
        if wires[gate[2]] == None:
            self.evaluate(gate[2], gates, wires)

        if gate[0] == 'AND':
            wires[wire] = wires[gate[1]] & wires[gate[2]]
        elif gate[0] == 'OR':
            wires[wire] = wires[gate[1]] | wires[gate[2]]
        elif gate[0] == 'XOR':
            wires[wire] = wires[gate[1]] ^ wires[gate[2]]

    def validate(self, gates: dict):
        wrong_pairs = []
        wrong = []

        # Find all the (x XOR y) and (x AND y) gates. These have to exist and cannot be swapped
        x_xor_y = {}
        for output, gate in gates.items():
            if gate[0] == 'XOR' and ((gate[1][0] == 'x' and gate[2][0] == 'y') or (gate[1][0] == 'y' and gate[2][0] == 'x')):
                assert gate[1][1:] == gate[2][1:]
                bit = gate[1][1:]
                if bit == '00':
                    # since bit 0 has no cayyi in, assert that the output of this gate is the sum of that bit
                    assert output == 'z00'
                x_xor_y[bit] = output

        x_and_y = {}
        for output, gate in gates.items():
            if gate[0] == 'AND' and ((gate[1][0] == 'x' and gate[2][0] == 'y') or (gate[1][0] == 'y' and gate[2][0] == 'x')):
                assert gate[1][1:] == gate[2][1:]
                bit = gate[1][1:]
                x_and_y[bit] = output

        # (x XOR y) has to be XOR'ed with the carry-in of the previous bit, so find those gates
        x_xor_y_xor_cin = {}
        cin = {}
        for bit, wire in x_xor_y.items():
            if bit == '00': # bit 0 has no carry in
                continue

            # The XOR gates with the output of (x XOR y) as one of its inputs
            possible_gates = [(out, gate) for out, gate in gates.items() if gate[0] == 'XOR' and (gate[1] == wire or gate[2] == wire)]
            
            # If no correct gate is found, we know that the output of (x XOR y) needs to be swapped with another wire
            # todo: which wire?
            if len(possible_gates) != 1:
                wrong.append(wire)
                continue

            # The output of ((x XOR y) XOR cin) is the sum bit, so check is the output is the correct sum bit
            gate = possible_gates[0]
            if gate[0] != ('z' + bit):
                # If the output is incorrect, we instantly know it needs to be swapped with the correct output
                wrong_pairs.append((gate[0], 'z' + bit))
                continue

            x_xor_y_xor_cin[bit] = gate[0]
            cin[bit] = gate[1][1] if gate[1][1] != wire else gate[1][2]


        x_xor_y_and_cin = {}
        # for bit, wire in x_xor_y.items():
        #     if bit == '00': # bit 0 has no carry in
        #         continue
        #     if bit not in cin: # we dont know the cin wire
        #         continue

        #     possible_gates = [(out, gate) for out, gate in gates.items() if gate[0] == 'AND' and ((gate[1] == wire and gate[2] == cin[bit]) or (gate[1] == cin[bit] and gate[2] == wire))]
        #     if len(possible_gates) != 1:
        #         wrong.append(wire)
        #         print(gate)
        #         continue

        #     gate = possible_gates[0]
        #     x_xor_y_and_cin[bit] = gate[0]

        cout = {}
        # for bit, wire in x_xor_y_and_cin.items():
        #     if bit not in x_and_y: # wire not known
        #         continue

        #     possible_gates = [(out, gate) for out, gate in gates.items() if gate[0] == 'OR' and ((gate[1] == wire and gate[2] == x_and_y[bit]) or (gate[1] == x_and_y[bit] and gate[2] == wire))]
        #     if len(possible_gates) != 1:
        #         wrong.append(wire)
        #         print(gate)
        #         continue

        #     gate = possible_gates[0]
        #     cout[bit] = gate[0]

        return wrong_pairs

    def swap(self, wire1, wire2, gates):
        tmp = gates[wire1]
        gates[wire1] = gates[wire2]
        gates[wire2] = tmp
        return gates

    def solve(self):
        start_time = time()

        wires = {}
        gates = {}
        output_wires = []
        init_wires, input_gates = self.input.split('\n\n')
        for gate in input_gates.splitlines():
            input, output = gate.split(' -> ')
            wires[output] = None
            if output[0] == 'z':
                output_wires.append(output)
            
            wire_a, gate_type, wire_b = input.split(' ')
            wires[wire_a] = None
            wires[wire_b] = None

            gates[output] = (gate_type, wire_a, wire_b)

        for initial_wire in init_wires.splitlines():
            name, val = initial_wire.split(': ')
            wires[name] = True if val == '1' else False

        for wire in output_wires:
            self.evaluate(wire, gates, wires)

        output_wires.sort(reverse=True)
        bin_num = ''.join(['1' if wires[wire] else '0' for wire in output_wires])
        

        fixed_gates = gates.copy()
        # fixed_gates = self.swap('z11', 'rpv', fixed_gates)
        fixed_gates = self.swap('z31', 'dmh', fixed_gates)
        fixed_gates = self.swap('z38', 'dvq', fixed_gates)
        fixed_gates = self.swap('rpb', 'ctg', fixed_gates)
        # print(fixed_gates['z31'])
        self.validate(fixed_gates)


        # print(x_and_y)

        part1 = int(bin_num, base=2)

        # not ctg,ctw,hhv,hnn,rpb,z11,z31,z38
        part2 = ','.join(sorted(['rpb', 'ctg', 'z38', 'dvq', 'z31', 'dmh', 'z11', 'rpv']))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day24()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
