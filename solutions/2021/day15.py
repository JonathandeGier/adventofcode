from collections import deque
from getInput import get_input

class Node:
    def __init__(self, pos):
        self.pos = pos

def get_grid():
    input = get_input(2021, 15).splitlines()
    grid = []
    for line in input:
        row = []
        for char in line:
            row.append(int(char))
        grid.append(row)
    return grid

def brute_force(width, height):
    start = ((0,0), set((0,0)))
    routes = []
    queue = deque(start)
    while queue:
        pos, route = queue.popleft()
        if pos == (width - 1, height - 1):
            routes.append(route)
        
        directions = []
        if pos[0] != 0:
            directions.append((pos[0] - 1, pos[1]))
        if pos[1]!= 0:
            directions.append((pos[0], pos[1] - 1))
        if pos[0] != width - 1:
            directions.append((pos[0] + 1, pos[1]))
        if pos[1] != height - 1:
            directions.append((pos[0], pos[1] + 1))

        for new_pos in directions:
            pass

def next(pos, grid: list, route: list, checked):
    width = len(grid[0])
    height = len(grid)
    print(route)

    if pos == (width - 1, height - 1):
        print("Exit found", route, len(route))
        return

    all_directions = {}
    if pos[0] != 0 and (pos[0] - 1, pos[1]) != route[-1]:
        all_directions[(pos[0] - 1, pos[1])] = grid[pos[0] - 1][pos[1]]
    if pos[1] != 0 and (pos[0], pos[1] - 1) != route[-1]:
        all_directions[(pos[0], pos[1] - 1)] = grid[pos[0]][pos[1] - 1]
    if pos[0] != height - 1 and (pos[0] + 1, pos[1]) != route[-1]:
        all_directions[(pos[0] + 1, pos[1])] = grid[pos[0] + 1][pos[1]]
    if pos[1] != width - 1 and (pos[0], pos[1] + 1) != route[-1]:
        all_directions[(pos[0], pos[1] + 1)] = grid[pos[0]][pos[1] + 1]

    # if pos[0] != 0:
    #     all_directions[(pos[0] - 1, pos[1])] = grid[pos[0] - 1][pos[1]]
    # if pos[1] != 0:
    #     all_directions[(pos[0], pos[1] - 1)] = grid[pos[0]][pos[1] - 1]
    # if pos[0] != height - 1:
    #     all_directions[(pos[0] + 1, pos[1])] = grid[pos[0] + 1][pos[1]]
    # if pos[1] != width - 1:
    #     all_directions[(pos[0], pos[1] + 1)] = grid[pos[0]][pos[1] + 1]

    if len(all_directions) == 0:
        return

    min_risk = min(all_directions.values())
    
    directions = []
    for dir in all_directions:
        if all_directions[dir] == min_risk:
            directions.append(dir)
    print("directions", directions)

    temp_route = route.copy()
    for new_pos in directions:
        if new_pos in route:
            route.pop()
            break
        else:
            route.append(new_pos)
            result = next(new_pos, grid, temp_route, checked)
            print("result", result)
        # else:
        #     pass
            # print("here", route)
    else:
        pass
        print("heres", route)
        return False

    return True
    
def a_star():
    start = Node((0,0))
    start.f = 0
    openList = [start]
    closedList = []

    while openList:
        pass


def main():
    grid = get_grid()
    
    width = len(grid[0])
    height = len(grid)

    a_star()
    exit()

    # next((0,0), grid, [(0,0)], [])
    # start = ((0,0), [])
    Q = deque([[(0,0)]])
    while Q:
        route = Q.popleft()
        pos = route[-1]
        print(route, len(Q))

        if pos == (width - 1, height - 1):
            print("Exit found", route, len(route))
            exit()
            return
        
        all_directions = {}
        if pos[0] != 0:
            if len(route) >= 2:
                if (pos[0] - 1, pos[1]) != route[-2]:
                    all_directions[(pos[0] - 1, pos[1])] = grid[pos[0] - 1][pos[1]]
            else:
                all_directions[(pos[0] - 1, pos[1])] = grid[pos[0] - 1][pos[1]]
        if pos[1] != 0:
            if len(route) >= 2:
                if (pos[0], pos[1] - 1) != route[-2]:
                    all_directions[(pos[0], pos[1] - 1)] = grid[pos[0]][pos[1] - 1]
            else:
                all_directions[(pos[0], pos[1] - 1)] = grid[pos[0]][pos[1] - 1]
        if pos[0] != height - 1:
            if len(route) >= 2:
                if (pos[0] + 1, pos[1]) != route[-2]:
                    all_directions[(pos[0] + 1, pos[1])] = grid[pos[0] + 1][pos[1]]
            else:
                all_directions[(pos[0] + 1, pos[1])] = grid[pos[0] + 1][pos[1]]
        if pos[1] != width - 1:
            if len(route) >= 2:
                if (pos[0], pos[1] + 1) != route[-2]:
                    all_directions[(pos[0], pos[1] + 1)] = grid[pos[0]][pos[1] + 1]
            else:
                all_directions[(pos[0], pos[1] + 1)] = grid[pos[0]][pos[1] + 1]

        min_risk = min(all_directions.values())
    
        directions = []
        for dir in all_directions:
            # if all_directions[dir] == min_risk:
            directions.append(dir)

        # print("directions", all_directions)

        for new_pos in directions:
            if new_pos not in route:
                new_route = route.copy()
                new_route.append(new_pos)
                # print("new route", new_route)
                Q.append(new_route)
            else:
                pass
                # neighbour already on route, check if route to current is less risk
                # better_route = []
                # for i in range(len(route)):
                #     if route[i] != new_pos:
                #         better_route.append(route[i])
                #     else:
                #         better_route.append(pos)
                #         break
                # Q.append(better_route)


    print("Puzzle 1:")

    print("")

    print("Puzzle 2:")


if __name__ == "__main__":
    main()
