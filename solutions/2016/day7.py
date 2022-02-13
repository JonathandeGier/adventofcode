from email.policy import strict
from Table import Table
from time import time

class Day7(Table):

    def __init__(self):
        self.day = 7
        self.title = "Internet Protocol Version 7"
        self.input = self.getInput(self.day)

    def get_ips(self):
        return self.input.splitlines()

    def is_tls(self, string: str):
        abbas = []
        for i in range(1, len(string) - 2):
            if string[i] == string[i+1] and string[i-1] == string[i+2] and string[i-1] != string[i]:
                abbas.append(i-1)
        
        in_hypernet = False
        for abba_i in abbas:
            for i in range(abba_i + 4, len(string)):
                if string[i] == "[":
                    break
                elif string[i] == "]":
                    in_hypernet = True

        if in_hypernet:
            return False

        if len(abbas) > 0:
            return True

        return False

    def is_ssl(self, string: str):
        supernet_abas = []
        hypernet_abas = []
        in_hypernet = False

        for i in range(len(string) - 2):
            if string[i] == "[":
                in_hypernet = True
            elif string[i] == "]":
                in_hypernet = False

            elif string[i] == string[i+2] and string[i] != string[i+1] and string[i+1] not in ["[", "]"]:
                if in_hypernet:
                    hypernet_abas.append(string[i:i+3])
                else:
                    supernet_abas.append(string[i:i+3])

        for aba in hypernet_abas:
            inverse = self.inverse_aba(aba)
            if inverse in supernet_abas:
                return True

        return False

    def inverse_aba(self, aba):
        assert len(aba) == 3
        return "".join([aba[1], aba[0], aba[1]])

    def solve(self):
        start_time = time()

        ips = self.get_ips()

        tls_ips = [ip for ip in ips if self.is_tls(ip)]
        ssl_ips = [ip for ip in ips if self.is_ssl(ip)]

        part1 = str(len(tls_ips))
        part2 = str(len(ssl_ips))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day7()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
