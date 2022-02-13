from Table import Table
from time import time

class Day3(Table):

    def __init__(self):
        self.day = 3
        self.title = "Squares With Three Sides"
        self.input = self.getInput(self.day)

    def get_data(self):
        data = []
        num_strings = [num.split(" ") for num in [item.strip() for item in self.input.splitlines()]]
        for raw_triangle in num_strings:
            triangle = [int(num) for num in raw_triangle if num != '']
            data.append(triangle)
        return data

    def to_column_triangles(self, row_triangles):
        column_triangles = []
        for i in range(0, len(row_triangles), 3):
            for j in range(3):
                column_triangle = [row_triangles[i][j], row_triangles[i+1][j], row_triangles[i+2][j]]
                column_triangle.sort()
                column_triangles.append(column_triangle)
        return column_triangles

    def solve(self):
        start_time = time()

        triangles = self.get_data()
        column_triangles = self.to_column_triangles(triangles)

        for triangle in triangles:
            triangle.sort()

        part1 = str(len([triangle for triangle in triangles if triangle[2] < triangle[0] + triangle[1]]))

        part2 = str(len([triangle for triangle in column_triangles if triangle[2] < triangle[0] + triangle[1]]))

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day3()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")
