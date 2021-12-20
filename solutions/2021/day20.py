from getInput import get_input
import numpy as np

def get_data():
    input = get_input(2021, 20).splitlines()
    mapping = ""
    image = []
    for line in input:
        if mapping == "":
            mapping = line.strip()
        elif line == "":
            continue
        else:
            row = [char for char in line.strip()]
            image.append(row)

    return mapping, image
            

def add_padding(image, fill):
    height = len(image)
    zeros = np.zeros(height)
    dots = [[fill] for zero in zeros]
    image = np.hstack((dots, image, dots))

    width = len(image[0])
    zeros = np.zeros(width)
    dots = [fill for zero in zeros]
    image = np.vstack([dots, image, dots])

    return image


def enhance(image, mapping, default):
    new_image = []
    width = len(image[0])
    height = len(image)
    for row, row_data in enumerate(image):
        new_row = []
        for col, val in enumerate(row_data):
            bin_index = ""
            for offset in [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]:
                selected_row = row + offset[0]
                selected_col = col + offset[1]
                if selected_row < 0 or selected_row >= height - 1 or selected_col < 0 or selected_col >= width - 1:
                    bin_index += default

                elif image[selected_row][selected_col] == "#":
                    bin_index += "1"
                else:
                    bin_index += "0"
            
            index = int(bin_index, 2)
            new_val = mapping[index]
            new_row.append(new_val)
        new_image.append(new_row)
    
    return np.array(new_image)


def main():
    mapping, image = get_data()
    image = np.array(image)

    image = add_padding(image, ".")
    image = enhance(image, mapping, "0")

    image = add_padding(image, "#")
    image = enhance(image, mapping, "1")

    pixels_lit = 0
    for row in image:
        for val in row:
            if val == "#":
                pixels_lit += 1

    print("Puzzle 1:")
    print(str(pixels_lit) + " pixels lit")
    print("")

    for i in range(24):
        image = add_padding(image, ".")
        image = enhance(image, mapping, "0")

        image = add_padding(image, "#")
        image = enhance(image, mapping, "1")

    pixels_lit = 0
    for row in image:
        for val in row:
            if val == "#":
                pixels_lit += 1

    print("Puzzle 2:")
    print(str(pixels_lit) + " pixels lit")
    print("")


if __name__ == "__main__":
    main()
