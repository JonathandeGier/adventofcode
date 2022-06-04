import math


def func(number: int):
    divisions = []
    didDivision = True

    while didDivision:
        didDivision = False
        for i in range(2, 10):
            result = number / i

            # if the result is a whole nuber
            if str(result)[:-3:-1] == '0.':
                divisions.append(i)
                number = int(result)
                didDivision = True
                break
                # print(str(result))

    if number == 0:
        return divisions
    else:
        divisions.append(number)
        return divisions

def factors(number: int):
        factors = []
        for num in range(1, int(math.sqrt(number)) + 1):
            if number % num == 0:
                factors.append(num)
                if number // num != num:
                    factors.append(number // num)
        return factors

def product(array: list) -> int:
    result = 1
    for num in array:
        result *= num
    
    return result


number = 247539732096723096839025762
numbers = func(number)
print(numbers)
print(factors(number))

print(product(numbers) == number)

# 2, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 9, 9