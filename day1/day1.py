import sys


def part_1(file_path):
    with open(file_path, 'r') as lines:
        rows = (line.rstrip('\n') for line in lines)
        list1 = []
        list2 = []
        for row in rows:
            elements = row.split()
            list1.append(int(elements[0]))
            list2.append(int(elements[1]))
        list1.sort()
        list2.sort()
        total = 0
        for (item1, item2) in zip(list1, list2):
            distance = abs(item1 - item2)
            total += distance
        print(total)


def part_2(file_path):
    with open(file_path, "r") as lines:
        rows = (line.rstrip("\n") for line in lines)
        list1 = []
        list2 = []
        for row in rows:
            elements = row.split()
            list1.append(int(elements[0]))
            list2.append(int(elements[1]))
        list1.sort()
        list2.sort()

        number_counts = {}
        total = 0
        for number in list1:
            count = number_counts.get(number, -1)
            if count == -1:
                count = list2.count(number)
                number_counts[number] = count
            total += number * count
        print(total)


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

if part == "1":
    part_1(file_path)
elif part == "2":
    part_2(file_path)
else:
    print("Unknown part")
    exit(1)
