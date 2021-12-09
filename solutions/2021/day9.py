from getInput import get_input

def get_data():
    input = get_input(2021, 9).splitlines()
    data = []
    for row in input:
        row = [int(val) for val in row]
        data.append(row)
    return data

def is_lowest_of_ajecent(row, column, data):
    top = 99
    left = 99
    right = 99
    bottom = 99

    if row != 0:
        top = data[row - 1][column]
    if column != 0:
        left = data[row][column -1]
    if column != len(data[0]) - 1:
        right = data[row][column + 1]
    if row != len(data) - 1:
        bottom = data[row + 1][column]

    value = data[row][column]
    return value < top and value < left and value < right and value < bottom


def recursive_basin_size(row, column, data, visited = []):
    top = 0
    bottom = 0
    left = 0
    right = 0

    if data[row][column] == 9:
        return 0

    if is_visited(row, column, visited):
        return 0

    visited.append([row, column])

    if row != 0:
        top = recursive_basin_size(row - 1, column, data, visited)
    if row != len(data) - 1:
        bottom = recursive_basin_size(row + 1, column, data, visited)
    if column != 0:
        left = recursive_basin_size(row, column - 1, data, visited)
    if column != len(data[0]) - 1:
        right = recursive_basin_size(row, column + 1, data, visited)

    return top + bottom + left + right + 1


def is_visited(row, column, visited):
    for place in visited:
        if place[0] == row and place[1] == column:
            return True
    return False


def n_largest_elements(list, n):
    largest = []
  
    for i in range(0, n): 
        max = 0
          
        for j in range(len(list)):     
            if list[j] > max:
                max = list[j]
                  
        list.remove(max)
        largest.append(max)
          
    return largest


def main():
    data = get_data()

    risk = 0
    basin_sizes = []
    for row, list in enumerate(data):
        for column, value in enumerate(list):
            if is_lowest_of_ajecent(row, column, data):
                risk += value + 1
                basin_sizes.append(recursive_basin_size(row, column, data))

    print("Puzzle 1:")
    print("Risk: " + str(risk))
    print("")

    print("Puzzle 2:")
    largest = n_largest_elements(basin_sizes, 3)
    print("Answer: " + str(largest[0] * largest[1] * largest[2]))


if __name__ == "__main__":
    main()
