import heapq
from getInput import get_input


def get_grid():
    input = get_input(2021, 15).splitlines()
    grid = []
    for line in input:
        row = []
        for char in line:
            row.append(int(char))
        grid.append(row)
    return grid


def path(pos, calculated_distances, grid):
    # if the distance to the position is already calculated, return the calculated distance
    if pos in calculated_distances:
        return calculated_distances[pos]

    # if the position is outside the grid, return a absurdly high number
    if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0]):
        return 1e9

    # if the current position is in the bottom-right corner (final position), return just the distance (risk) at that position
    if pos[0] == len(grid) - 1 and pos[1] == len(grid[0]) - 1:
        return grid[pos[0]][pos[1]]

    # calculate the lowest distance to the final point
    ans = grid[pos[0]][pos[1]] + min(path((pos[0] + 1, pos[1]), calculated_distances, grid), path((pos[0], pos[1] + 1), calculated_distances, grid))
    calculated_distances[pos] = ans
    return ans
    

def main():
    # Load the grid
    grid = get_grid()

    # solve part 1
    result = path((0,0), {}, grid)
    risk = result - grid[0][0]

    print("Puzzle 1:")
    print("Lowest risk path: " + str(risk))
    print("")

    # expand the grid
    new_grid = []
    for i in range(5):
        for row in grid:
            new_row = []        
            for j in range(5):
                for cell in row:
                    val = cell + i + j
                    if val >= 10:
                        val -= 9
                    new_row.append(val)
            new_grid.append(new_row)

    # solve part 2
    calculated_distances = [[None for _ in range(len(new_grid[0]))] for _ in range(len(new_grid))]
    queue = [(0,0,0)]
    while queue:
        (distance, row, col) = heapq.heappop(queue)

        if row < 0 or row >= len(new_grid) or col < 0 or col >= len(new_grid[0]):
            continue

        cost = distance + new_grid[row][col]

        if calculated_distances[row][col] == None or cost < calculated_distances[row][col]:
            calculated_distances[row][col] = cost
        else: 
            continue

        if row == len(new_grid) - 1 and col == len(new_grid[0]) - 1:
            break

        for pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row = row + pos[0]
            new_col = col + pos[1]

            heapq.heappush(queue, (calculated_distances[row][col], new_row, new_col))
        
    risk = calculated_distances[len(new_grid) - 1][len(new_grid[0]) - 1] - new_grid[0][0]
    
    print("Puzzle 2:")
    print("Lowest risk path: " + str(risk))


if __name__ == "__main__":
    main()
