from os import truncate
from getInput import get_input

def get_data():
    input = get_input(2021, 11).splitlines()
    data = []
    for row in input:
        row = [int(val) for val in row]
        data.append(row)
    return data

def not_flashed(row, column, flashed):
    for flash in flashed:
        if flash[0] == row and flash[1] == column:
            return False
    return True

def flashable(data):
    for row in data:
        for val in row:
            if val >= 10:
                return True
    return False

def flash(data, flashed = []):
    flashes = 0

    for row, row_data in enumerate(data):
        for column, val in enumerate(row_data):
            if val >= 10:
                flashes += 1
                flashed.append([row, column])
                data[row][column] = 0

                if row != 0 and column != 0 and not_flashed(row - 1, column - 1, flashed):
                    data[row - 1][column - 1] += 1

                if row != 0 and not_flashed(row - 1, column, flashed):
                    data[row - 1][column] += 1

                if row != 0 and column != len(data[0]) - 1 and not_flashed(row - 1, column + 1, flashed):
                    data[row - 1][column + 1] += 1

                if column != 0 and not_flashed(row, column - 1, flashed):
                    data[row][column - 1] += 1

                if column != len(data[0]) - 1 and not_flashed(row, column + 1, flashed):
                    data[row][column + 1] += 1

                if row != len(data) - 1 and column != 0 and not_flashed(row + 1, column - 1, flashed):
                    data[row + 1][column - 1] += 1

                if row != len(data) - 1 and not_flashed(row + 1, column, flashed):
                    data[row + 1][column] += 1

                if row != len(data) - 1 and column != len(data[0]) - 1 and not_flashed(row + 1, column + 1, flashed):
                    data[row + 1][column + 1] += 1
    
    if flashable(data):
        extra_flashes, data = flash(data, flashed)
        return flashes + extra_flashes, data
    else:
        return flashes, data

def main():
    data = get_data()
    print("Puzzle 1:")

    flashes = 0
    all_flash = 0
    for step in range(1000):
        for row, row_data in enumerate(data):
            for column, val in enumerate(row_data):
                data[row][column] = val + 1
        
        step_flashes, data = flash(data, [])
        if step < 100:
            flashes += step_flashes

        if all_flash == 0 and step_flashes == 100:
            all_flash = step + 1
            break

        
    print("Flashes: " + str(flashes))
    print("")

    print("Puzzle 2:")
    print("All flash at step " + str(all_flash))


if __name__ == "__main__":
    main()
