from getInput import get_input

class Packet:

    def __init__(self, version, type):
        self.version = version
        self.type = type
        self.sub_packets = []

    def is_literal(self):
        return self.type == 4

    def deep_version_sum(self):
        sub_sum = 0
        for sub_pack in self.sub_packets:
            sub_sum += sub_pack.deep_version_sum()
        return self.version + sub_sum

    def to_value(self):
        if self.type == 0:
            # sum
            return sum([pack.to_value() for pack in self.sub_packets])
        elif self.type == 1:
            # product
            product = 1
            for pack in self.sub_packets:
                product *= pack.to_value()
            return product
        elif self.type == 2:
            # min
            return min([pack.to_value() for pack in self.sub_packets])
        elif self.type == 3:
            # max
            return max([pack.to_value() for pack in self.sub_packets])
        elif self.type == 4:
            return self.value
        elif self.type == 5:
            # greater than
            if self.sub_packets[0].to_value() > self.sub_packets[1].to_value():
                return 1
            else:
                return 0
        elif self.type == 6:
            # less than
            if self.sub_packets[0].to_value() < self.sub_packets[1].to_value():
                return 1
            else:
                return 0
        else: # type == 7
            # equal to
            if self.sub_packets[0].to_value() == self.sub_packets[1].to_value():
                return 1
            else:
                return 0

    def string_type(self):
        if self.type == 0:
            return "Sum of subpackets" + "  (" + str(self.to_value()) + ")"
        elif self.type == 1:
            return "Product of subpackets" + "  (" + str(self.to_value()) + ")"
        elif self.type == 2:
            return "Minimum of subpackets" + "  (" + str(self.to_value()) + ")"
        elif self.type == 3:
            return "Maximum of subpackets" + "  (" + str(self.to_value()) + ")"
        elif self.type == 4:
            return "Value" + "  (" + str(self.to_value()) + ")"
        elif self.type == 5:
            return "First less than second" + "  (" + str(self.to_value()) + ")"
        elif self.type == 6:
            return "First more than second" + "  (" + str(self.to_value()) + ")"
        else: 
            return "First equal to" + "  (" + str(self.to_value()) + ")"

    def __str__(self, depth = 0):
        indent = ""
        for _ in range(depth):
            indent += "\t"
        self_string = indent + self.string_type() + "\n"

        for pack in self.sub_packets:
            self_string += pack.__str__(depth+1)
        return self_string

def get_data():
    return get_input(2021, 16).strip()

def to_bin_string(string):
    return bin(int(string, 16))[2:].zfill(len(string) * 4)


def parse(string, max = -1):
    packets = []

    while max != 0:
        max -= 1

        version = int(string[0:3], 2)
        type = int(string[3:6], 2)

        packet = Packet(version, type)

        if packet.is_literal():
            val = ""
            curr_group = -1

            while True:
                curr_group += 1
                group = string[6 + (curr_group * 5):11 + (curr_group * 5)]
                val += group[1:]

                if group[0] == "0":
                    break

            packet.value = int(val, 2)
            packet.raw_length = 11 + (curr_group * 5)

        else:
            packet.length_type_id = int(string[6:7])

            if packet.length_type_id == 0:
                # length = total length in bits
                packet.type_length = int(string[7:22], 2) # next 15 bits
                raw_sub_packets = string[22:22 + packet.type_length]
                packet.sub_packets = parse(raw_sub_packets)

                packet.raw_length = 22 + packet.type_length
                packet.raw = string[0:packet.raw_length]
            else:
                # length = number of sub_packets
                packet.type_length = int(string[7:18], 2) # next 11 bits
                packet.sub_packets = parse(string[18:], packet.type_length)

                length = 0
                for pack in packet.sub_packets:
                    length += pack.raw_length

                packet.raw_length = 18 + length


        packets.append(packet)
        string = string[packet.raw_length:]

        if string == "" or int(string, 2) == 0:
            break

    return packets

    


def main():
    data = get_data()

    binary = to_bin_string(data)

    packets = parse(binary)

    assert len(packets) == 1
    packet = packets[0]

    print("Puzzle 1:")
    print("Sum of all version numbers: " + str(packet.deep_version_sum()))

    print("")

    print("Puzzle 2:")
    print("Resulting value: " + str(packet.to_value()))


def visualize():
    data = get_data()

    binary = to_bin_string(data)

    packets = parse(binary)

    assert len(packets) == 1
    packet = packets[0]

    print(packet)


if __name__ == "__main__":
    main()
