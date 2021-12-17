from getInput import get_input

def get_target():
    input = get_input(2021, 17).strip().split(" ")
    x_raw = input[2]
    y_raw = input[3]
    x = []
    y = []

    x.append(int(x_raw.split("..")[0].replace("x=", "")))
    x.append(int(x_raw.split("..")[1].replace(",", "")))

    y.append(int(y_raw.split("..")[0].replace("y=", "")))
    y.append(int(y_raw.split("..")[1].replace(",", "")))

    return ((min(x), max(x)), (max(y), min(y)))
    


def main():
    target_x, target_y = get_target()

    valid_starts = set()
    highest_y_pos = 0
    for vx in range(300):
        for vy in range(-400, 400):
            pos = (0,0)
            v = (vx, vy)
            init_v = (vx, vy)
            loc_highest = 0
            hit_target = False
            while pos[0] < target_x[1] and pos[1] > target_y[1]:
                pos = (pos[0] + v[0], pos[1] + v[1])
                
                if v[0] > 0:
                    new_x = v[0] - 1
                elif v[0] < 0:
                    new_x = v[0] + 1
                else:
                    new_x = v[0]

                v = (new_x, v[1] - 1)

                if pos[1] > loc_highest:
                    loc_highest = pos[1]
                
                if pos[0] >= target_x[0] and pos[0] <= target_x[1] and pos[1] <= target_y[0] and pos[1] >= target_y[1]:
                    hit_target = True

            if loc_highest > highest_y_pos and hit_target:
                highest_y_pos = loc_highest

            if hit_target:
                valid_starts.add(init_v)


    print("Puzzle 1:")
    print(highest_y_pos)
    print("")

    print("Puzzle 2:")
    print(len(valid_starts))

    


if __name__ == "__main__":
    main()
