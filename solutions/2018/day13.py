from Table import Table
from time import time

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
STRAIGHT = 'straight'

DIRECTIONS = {
    '^': UP,
    'v': DOWN,
    '<': LEFT,
    '>': RIGHT,
}

NEXT_DIRECTION = {
    LEFT: STRAIGHT,
    STRAIGHT: RIGHT,
    RIGHT: LEFT,
}

APPLY_DIRECTION = {
    UP: {
        LEFT: LEFT,
        STRAIGHT: UP,
        RIGHT: RIGHT,
        '/': RIGHT,
        '\\': LEFT,
    },
    DOWN: {
        LEFT: RIGHT,
        STRAIGHT: DOWN,
        RIGHT: LEFT,
        '/': LEFT,
        '\\': RIGHT,
    },
    LEFT: {
        LEFT: DOWN,
        STRAIGHT: LEFT,
        RIGHT: UP,
        '/': DOWN,
        '\\': UP,
    },
    RIGHT: {
        LEFT: UP,
        STRAIGHT: RIGHT,
        RIGHT: DOWN,
        '/': UP,
        '\\': DOWN,
    },
}

class Cart:
    def __init__(self, id: int, position: tuple, direction: str):
        self.id = id
        self.position = position
        self.direction = direction
        self.next_direction = LEFT
        self.collided = False

class Day13(Table):

    def __init__(self):
        self.day = 13
        self.title = "Mine Cart Madness"
        self.input = self.getInput(self.day)

        self.track = None
        self.carts = None

        self.first_collision = None
        self.last_cart = None

    def load_track(self):

        self.track = [[*line] for line in self.input.splitlines()]
        self.carts = []

        # x is the vertical axis, y is the horizontal axis
        id = 1
        for x, line in enumerate(self.track):
            for y, char in enumerate(line):
                if char in ['^', 'v', '<', '>']:
                    self.carts.append(Cart(id, (x, y), DIRECTIONS[char]))

                    if char in ['^', 'v']:
                        self.track[x][y] = '|'
                    elif char in ['<', '>']:
                        self.track[x][y] = '-'

                    id += 1

    def tick(self):
        sorted_carts = sorted(self.carts, key=lambda x: x.position)

        for cart in sorted_carts:
            if cart.collided:
                continue

            x = cart.position[0]
            y = cart.position[1]

            # update the cart direction
            if self.track[x][y] == '+':
                cart.direction = APPLY_DIRECTION[cart.direction][cart.next_direction]
                cart.next_direction = NEXT_DIRECTION[cart.next_direction]
            elif self.track[x][y] in ['/', '\\']:
                cart.direction = APPLY_DIRECTION[cart.direction][self.track[x][y]]

            # move the cart
            if cart.direction == UP:
                cart.position = (x-1, y)
            elif cart.direction == DOWN:
                cart.position = (x+1, y)
            elif cart.direction == LEFT:
                cart.position = (x, y-1)
            elif cart.direction == RIGHT:
                cart.position = (x, y+1)

            # check for collision
            collided_carts = [other_cart for other_cart in self.carts if other_cart.position == cart.position and other_cart.id != cart.id and not other_cart.collided]
            for collided_cart in collided_carts:
                cart.collided = True
                collided_cart.collided = True

                if self.first_collision == None:
                    self.first_collision = cart.position

        remaining_carts = [cart for cart in self.carts if not cart.collided]
        if len(remaining_carts) == 1:
            self.last_cart = remaining_carts[0]
            return True

        return False

    def solve(self):
        start_time = time()

        self.load_track()

        finished = False
        while not finished:
            finished = self.tick()

        part1 = str(self.first_collision[1]) + ',' + str(self.first_collision[0])
        part2 = str(self.last_cart.position[1]) + ',' + str(self.last_cart.position[0])

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day13()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
