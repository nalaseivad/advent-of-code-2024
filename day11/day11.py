import sys
import math


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def append(self, data):
        if self.count == 0:
            new_node = Node(data)
            self.head = self.tail = new_node
            self.count += 1
            return
        self.insert_after(self.tail, data)

    def insert_after(self, target_node, data):
        new_node = Node(data)
        new_node.next = target_node.next
        new_node.prev = target_node
        if target_node.next:
            target_node.next.prev = new_node
        target_node.next = new_node
        if target_node == self.tail:
            self.tail = new_node
        self.count += 1

    def print(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()


def count_digits(n):
    if n == 0:
        return 1
    return math.floor(math.log10(abs(n))) + 1


def split_number(number, num_digits):
    s = str(number)
    n = num_digits // 2
    return int(s[:n]), int(s[n:])


def blink(stones):
    stone = stones.head
    while stone:
        if stone.data == 0:
            stone.data = 1
            stone = stone.next
            continue
        num_digits = count_digits(stone.data)
        if num_digits % 2 == 0:
            n1, n2 = split_number(stone.data, num_digits)
            stone.data = n1
            stones.insert_after(stone, n2)
            stone = stone.next.next
            continue
        stone.data = stone.data * 2024
        stone = stone.next


def _count_stones(stone_value, num_blinks):
    if num_blinks == 0:
        return 1

    if stone_value == 0:
        return count_stones(1, num_blinks - 1)

    string = str(stone_value)
    length = len(string)
    if length % 2 == 0:
        half = length // 2
        return count_stones(int(string[:half]), num_blinks - 1) + count_stones(int(string[half:]), num_blinks - 1)

    return count_stones(stone_value * 2024, num_blinks - 1)


cache = {}

def count_stones(stone_value, num_blinks):
    cache_key = (stone_value, num_blinks)
    if cache_key in cache:
        return cache[(stone_value, num_blinks)]

    result =  _count_stones(stone_value, num_blinks)
    cache[cache_key] = result
    return result


#
# Using the same approach as part 2
#
def part_1(stones):
    print(stones)
    count = 0
    for stone in stones:
        count += count_stones(stone, 25)
    return count


#
# This suffices for part 1, in fact this would be fine using just a native Python list.  I thought I was being clever by
# using a linked list to make the stone splits more efficient but that was not going to help with part 2.
#
def part_1_brute_force(stones):
    print(stones)
    ll = LinkedList()
    for stone in stones:
        ll.append(stone)
    for _ in range(25):
        blink(ll)
    return ll.count


#
# I realized that I needed a fundamentally different approach for part 2.  I then back ported the same idea to part 1
# as well.
#
def part_2(stones):
    print(stones)
    count = 0
    for stone in stones:
        count += count_stones(stone, 75)
    return count


def part_n(file_path, fn):
    stones = []
    with open(file_path, "r") as lines:
        for line in lines:
            row = line.rstrip("\n")
            stones.extend([int(n) for n in row.split()])
    print(fn(stones))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "1"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day11/test-input-2.txt"

if part == "1":
    part_n(file_path, part_1)
    #part_n(file_path, part_1_brute_force)
elif part == "2":
    part_n(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
