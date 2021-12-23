from getInput import get_input
import numpy as np
from cubes import Workspace

def get_data():
    input = get_input(2021, 22).splitlines()
    steps = []
    for line in input:
        action, ranges = line.split(" ")
        ranges = ranges.split(",")

        dx = ranges[0].split("=")[1].split("..")
        dx = (int(dx[0]), int(dx[1]))

        dy = ranges[1].split("=")[1].split("..")
        dy = (int(dy[0]), int(dy[1]))

        dz = ranges[2].split("=")[1].split("..")
        dz = (int(dz[0]), int(dz[1]))

        steps.append((action, dx, dy, dz))

    return steps


def apply_step(step, reactor):
    if step[1][0] < -50 or step[2][0] < -50 or step[3][0] < -50 or step[1][1] > 50 or step[2][1] > 50 or step[3][1] > 50:
        return reactor

    for x in range(step[1][0] + 50, step[1][1] + 51):
        for y in range(step[2][0] + 50, step[2][1] + 51):
            for z in range(step[3][0] + 50, step[3][1] + 51):
                if step[0] == "on":
                    reactor[x][y][z] = 1.0
                else:
                    reactor[x][y][z] = 0.0
    return reactor


def change_in_sum(step, other_steps):
    dx = abs(step[1][1] - step[1][0])
    dy = abs(step[2][1] - step[2][0])
    dz = abs(step[3][1] - step[3][0])

    volume = dx * dy * dz

    intersect_with_on = 0
    intersect_with_off = 0
    # for other_step in other_steps:
    for i in range(len(other_steps) - 1, -1, -1):
        other_step = other_steps[i]
        intersect = intersection(step, other_step)

        if other_step[0] == "on":
            intersect_with_on += intersect
        else:
            intersect_with_off += intersect

    if step[0] == "on":
        return volume - intersect_with_on
    else:
        return intersect_with_on * -1


def intersection(step, other_step):
    dx = min(step[1][1], other_step[1][1]) - max(step[1][0], other_step[1][0])
    dy = min(step[2][1], other_step[2][1]) - max(step[2][0], other_step[2][0])
    dz = min(step[3][1], other_step[3][1]) - max(step[3][0], other_step[3][0])

    intersect = 0
    if dx >= 0 and dy >= 0 and dz >= 0:
        intersect = dx * dy * dz

    return intersect


def sum_intersect(steps):
    pass
        


def main():
    steps = get_data()
    
    reactor = np.zeros((100, 100, 100))

    for step in steps:
        reactor = apply_step(step, reactor)
    

    print("Puzzle 1:")
    print(int(np.sum(reactor)))
    print("")

    print("Puzzle 2:")
    print("...")

    workspace = Workspace("slicer.ini")
    browser = workspace.browser()


if __name__ == "__main__":
    main()
