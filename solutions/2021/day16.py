from getInput import get_input

class Packet:

    def __init__(self, version, type):
        self.version = version
        self.type = type

    def is_literal(self):
        return self.type == 4

def get_data():
    return get_input(2021, 16).strip()

def to_bin_string(string):
    return bin(int(string, 16))[2:].zfill(len(string) * 4)


def parse(string, max = -1):
    packets = []
    print(len(packets))

    while max != 0:
        max -= 1

        version = int(string[0:3], 2)
        type = int(string[3:6], 2)

        packet = Packet(version, type)

        if packet.is_literal():
            val = ""
            curr_group = 0

            while True:
                group = string[6 + (curr_group * 5):11 + (curr_group * 5)]
                val += group[1:-1]
                curr_group += 1

                if group[0] == 0:
                    break
            data_length = 11 + (curr_group * 5)
            packet_length = data_length
            while packet_length % 4 != 0:
                packet_length += 1

            packet.value = int(val, 2)
            packet.raw_length = packet_length
            packet.raw = string[0:packet_length]

        else:
            packet.length_type_id = int(string[6:7])

            if packet.length_type_id == 0:
                # length = total length in bits
                packet.type_length = int(string[7:22]) # next 15 bits
                raw_sub_packets = string[22:22 + packet.type_length]
                packet.sub_packets = parse(raw_sub_packets)

                packet.raw_length = 22 + packet.type_length
                packet.raw = string[0:packet.raw_length]
            else:
                # length = number of sub_packets
                packet.type_length = int(string[7:18]) # next 11 bits
                packet.sub_packets = parse(string[18:], packet.type_length)

            print("operational packet")
            exit()
            # operational packet

        packets.append(packet)
        string = string[packet.raw_length:]
    return packets

    


def main():
    data = get_data()
    data = data[1:-1] # remove beginning and end 0 bits

    # Example
    # data = "8A004A801A8002F478"
    data = "38006F45291200" # 1 op packet, 2 sub literal packets

    binary = to_bin_string(data)

    parse(binary)
    
    print(to_bin_string(data))

    print("Puzzle 1:")

    print("")

    print("Puzzle 2:")


if __name__ == "__main__":
    main()
