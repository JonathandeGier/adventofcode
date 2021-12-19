from getInput import get_input
import numpy as np
from scipy.spatial.transform import Rotation as R
from collections import deque
from itertools import combinations
import time


class Grid:
    def __init__(self):
        self.beacons = set()
        self.scanners = []
        self.scanner_locations = {}
        self.scanners_to_match = deque([])

    def add_scanner(self, scanner):
        self.scanners.append(scanner)

        if len(self.scanners) == 1:
            for point in scanner.points:
                self.beacons.add(point)
            self.scanner_locations[scanner.id] = (0,0,0)
            print("Match " + str(scanner.id))
            return

        self.scanner_locations[scanner.id] = None
        self.scanners_to_match.append(scanner)
        self.match()


    def match(self):
        new_queue = deque([])

        while self.scanners_to_match:
            scanner = self.scanners_to_match.pop()
            found_match = False

            for rotation in scanner.rotated_points:
                for new_point in scanner.rotated_points[rotation]:
                    for existing_point in self.beacons:
                        trans_x = existing_point[0] - new_point[0]
                        trans_y = existing_point[1] - new_point[1]
                        trans_z = existing_point[2] - new_point[2]

                        translated_points = self.__translate(scanner.rotated_points[rotation], trans_x, trans_y, trans_z)

                        temp_set = self.beacons.copy()
                        for point in translated_points:
                            temp_set.add(point)

                        len_without_matches = len(translated_points) + len(self.beacons)
                        if len_without_matches - len(temp_set) >= 12:
                            # MATCH
                            found_match = True
                            print("Match " + str(scanner.id) + " from rotation " + str(rotation))

                            # add points to beacon set
                            for point in translated_points:
                                self.beacons.add(point)

                            # add location to scanner
                            self.scanner_locations[scanner.id] = (trans_x, trans_y, trans_z)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

            if not found_match:
                new_queue.append(scanner)
        self.scanners_to_match = new_queue

    def __translate(self, points, x, y, z):
        new_points = []
        for point in points:
            new_points.append((point[0] + x, point[1] + y, point[2] + z))
        return new_points


class Scanner:
    def __init__(self, id: int):
        self.id = id
        self.points = []
        self.rotated_points = {
            ("u", 0): [], ("u", 90): [], ("u", 180): [], ("u", 270): [],
            ("l", 0): [], ("l", 90): [], ("l", 180): [], ("l", 270): [],
            ("r", 0): [], ("r", 90): [], ("r", 180): [], ("r", 270): [],
            ("f", 0): [], ("f", 90): [], ("f", 180): [], ("f", 270): [],
            ("b", 0): [], ("b", 90): [], ("b", 180): [], ("b", 270): [],
            ("d", 0): [], ("d", 90): [], ("d", 180): [], ("d", 270): [],
        }
        self.rot_2 = {}

    def add_point(self, point):
        self.points.append(point)
        for rotation in self.rotated_points.keys():
            if rotation[0] == "u":
                first_degree = 0
                first_axis = np.array([0,0,0])
                second_axis = np.array([0,1,0])
            elif rotation[0] == "l":
                first_degree = 90
                first_axis = np.array([1,0,0])
                second_axis = np.array([0,0,1])
            elif rotation[0] == "r":
                first_degree = -90
                first_axis = np.array([1,0,0])
                second_axis = np.array([0,0,1])
            elif rotation[0] == "f":
                first_degree = 90
                first_axis = np.array([0,0,1])
                second_axis = np.array([1,0,0])
            elif rotation[0] == "b":
                first_degree = -90
                first_axis = np.array([0,0,1])
                second_axis = np.array([1,0,0])
            elif rotation[0] == "d":
                first_degree = 180
                first_axis = np.array([1,0,0])
                second_axis = np.array([0,1,0])
            else:
                assert False, rotation[0]

            first_radians = np.radians(first_degree)
            first_vector = first_radians * first_axis
            first_rotation = R.from_rotvec(first_vector)
            rotated_point = first_rotation.apply(point)

            second_radians = np.radians(rotation[1])
            second_vector = second_radians * second_axis
            second_rotation = R.from_rotvec(second_vector)
            rotated_point = second_rotation.apply(rotated_point)

            self.rotated_points[rotation].append((round(float(rotated_point[0])), round(float(rotated_point[1])), round(float(rotated_point[2]))))


    def print_rotations(self):
        string = "Scanner " + str(self.id) + "\n"
        for rotation in self.rotated_points:
            for points in self.rotated_points[rotation]:
                for point in points:
                    string += str(point) + ", "
                string += "\n"
            string += "\n"
        return string
    
    def has_duplicates(self):
        rotations = set()
        for rotation in self.rotated_points:
            tup = tuple(self.rotated_points[rotation])
            if tup in rotations:
                print(rotation)
            rotations.add(tup)

        assert len(rotations) == 24, len(rotations)
        print(len(rotations))

    def __str__(self):
        string = "Scanner " + str(self.id)
        # for rotation in self.rotated_points:
        #     for points in self.rotated_points[rotation]:
        #         for point in points:
        #             string += str(point) + ", "
        #         string += "\n"
        #     string += "\n"
        return string


def get_scanners():
    input = get_input(2021, 19).splitlines()
    scanners = []
    scanner = None
    for line in input:
        if "---" in line:
            scanner = Scanner(int(line.split(" ")[2]))
        elif line == "":
            scanners.append(scanner)
        else:
            point = line.split(",")
            scanner.add_point((int(point[0]), int(point[1]), int(point[2])))
    scanners.append(scanner)

    return scanners
    


def main():
    start = time.time_ns()
    scanners = get_scanners()
    print("precalculated rotations")

    grid = Grid()
    for i, scanner in enumerate(scanners):
        assert scanner.id == i
        grid.add_scanner(scanner)

    while len([scan for scan in grid.scanner_locations if grid.scanner_locations[scan] == None]) > 0:
        grid.match()


    print("")
    print("Puzzle 1:")
    print(str(len(grid.beacons)) + " Beacons")
    print("")

    # distances = {0: (0, 0, 0), 1: (30, 58, 3463), 2: (3, 122, 2402), 3: (-30, -1099, 4776), 4: (1175, -2333, 1161), 5: (1113, -1093, -1193), 6: (58, -3440, 1180), 7: (35, 41, 1043), 8: (-122, 59, 4708), 9: (1254, 75, -39), 10: (-1276, -3535, 1131), 11: (2451, 155, 2221), 12: (1103, 2383, 1149), 13: (-58, -4748, 1207), 14: (1073, 166, 2276), 15: (1103, 1340, 1046), 16: (34, -1160, 2248), 17: (1075, 30, 1147), 18: (1121, -3548, 1143), 19: (1082, -2324, 2251), 20: (-72, -2250, 2305), 21: (1157, -1099, -185), 22: (21, 1221, 3496), 23: (2338, -1123, -155), 24: (-71, -3608, 2309), 25: (1160, -1041, 1026)}
    # comb = list(combinations(distances.values(), 2))

    comb = list(combinations(grid.scanner_locations.values(), 2))
    max_distance = 0
    for points in comb:
        x = abs(points[0][0] - points[1][0])
        y = abs(points[0][1] - points[1][1])
        z = abs(points[0][2] - points[1][2])
        distance = x + y + z
        # print(distance)
        max_distance = max(max_distance, distance)

    print("Puzzle 2:")
    # 8254 < x
    print("Largest manhattan distande: " + str(max_distance))

    end = time.time_ns()
    dif = end - start
    print("")
    print("Execution took " + str(dif / 1_000_000_000) + " seconds")


if __name__ == "__main__":
    main()
