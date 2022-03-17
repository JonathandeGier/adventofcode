from Table import Table
from time import time

class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "Firewall Rules"
        self.input = self.getInput(self.day)

    def getIps(self):
        ipRanges = []
        for line in self.input.splitlines():
            low, high = line.split('-')

            low = int(low)
            high = int(high)

            assert low < high

            ipRanges.append((int(low), int(high)))

        return ipRanges

    def solve(self):
        start_time = time()

        ipRanges = self.getIps()

        subOnes = [ipRange[0] - 1 for ipRange in ipRanges if ipRange[0] > 0]

        validSubOnes = []
        for ip in subOnes:
            valid = True
            for ipRange in ipRanges:
                if ip >= ipRange[0] and ip <= ipRange[1]:
                    valid = False
                    break
            
            if valid:
                validSubOnes.append(ip)


        part1 = min(validSubOnes)


        # merge overlapping ipRanges
        ipRanges.sort()
        merged_ipRanges = []
        merged_ipRanges.append(ipRanges[0])
        for i in range(1, len(ipRanges)):
            ipRange = ipRanges[i]
            mergedipRange = merged_ipRanges.pop()

            # check overlap
            if ipRange[0] <= mergedipRange[1] and ipRange[1] >= mergedipRange[0]:
                new_ipRange = (mergedipRange[0], max(ipRange[1], mergedipRange[1]))
                merged_ipRanges.append(new_ipRange)
            else:
                merged_ipRanges.append(mergedipRange)
                merged_ipRanges.append(ipRange)

        # part in between ipRanges are valid
        validAddresses = 0
        for i in range(len(merged_ipRanges) - 1):
            ipRange1 = merged_ipRanges[i]
            ipRange2 = merged_ipRanges[i + 1]

            diff = (ipRange2[0] - ipRange1[1]) - 1
            validAddresses += diff
                    

        part2 = validAddresses

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
