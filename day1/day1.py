import sys


def part_1(list1, list2):
    list1.sort()
    list2.sort()
    total = 0
    for (item1, item2) in zip(list1, list2):
        distance = abs(item1 - item2)
        total += distance
    return total


def part_2(list1, list2):
    number_counts = {}
    total = 0
    for number in list1:
        count = number_counts.get(number, -1)
        if count == -1:
            count = list2.count(number)
            number_counts[number] = count
        total += number * count
    return total


def part_n(file_path, fn):
    with open(file_path, "r") as lines:
        list1 = []
        list2 = []
        for row in (line.rstrip("\n") for line in lines):
            elements = [int(x) for x in row.split()]
            list1.append(elements[0])
            list2.append(elements[1])
        answer = fn(list1, list2)
        print(answer)


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

if part == "1":
    part_n(file_path, part_1)
elif part == "2":
    part_n(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
