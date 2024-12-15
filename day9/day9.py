import sys


def print_blocks(blocks):
    print("".join(blocks))


def print_extents(extents):
    print_blocks(extents_to_blocks(extents))


def calc_checksum(blocks):
    checksum = 0
    for n, block in enumerate(blocks):
        if block == ".":
            continue
        checksum += n * int(block)
    return checksum


def move_extent(extents, n, extent_n):
    dest_extent = extents[n]
    length = extents[extent_n]["length"]
    dest_extent["type"] = "hybrid"
    if "moved_extents" not in extents[n]:
        dest_extent["moved_extents"] = []
    moved_extents = dest_extent["moved_extents"]
    moved_extents.append({"type": "file", "id": id, "length": length})
    dest_extent["length"] -= length
    extents[extent_n] = {"type": "free_space", "length": length}
    return


def possibly_move_extent(extents, extent_n):
    n = 0
    length = extents[extent_n]["length"]
    id = extents[extent_n]["id"]
    while True:
        while extents[n]["type"] == "file":
            n += 1
        if n >= extent_n:
            break
        if extents[n]["length"] >= length:
            extents[n]["type"] = "hybrid"
            if "moved_extents" not in extents[n]:
                extents[n]["moved_extents"] = []
            moved_extents = extents[n]["moved_extents"]
            moved_extents.append({"type": "file", "id": id, "length": length})
            extents[n]["length"] -= length
            extents[extent_n] = {"type": "free_space", "length": length}
            return
        n += 1


def compact_extents(extents):
    n = len(extents) - 1
    while extents[n]["type"] != "file":
        n -= 1
    while n > 0:
        # print_extents(extents)
        possibly_move_extent(extents, n)
        n -= 1
        while extents[n]["type"] != "file":
            n -= 1
    # print_extents(extents)


def compact_blocks(blocks):
    n = 0
    m = len(blocks) - 1
    while True:
        while blocks[n] != ".":
            n += 1
        while blocks[m] == ".":
            m -= 1
        if n >= m:
            break
        while blocks[n] == "." and blocks[m] != ".":
            blocks[n] = blocks[m]
            blocks[m] = "."
            n += 1
            m -= 1
            # print("".join(blocks))


def extents_to_blocks(extents):
    blocks = []
    for extent in extents:
        type = extent["type"]
        length = extent["length"]
        if type == "hybrid":
            for moved_extent in extent["moved_extents"]:
                for _ in range(moved_extent["length"]):
                    blocks.append(str(moved_extent["id"]))
            for _ in range(length):
                blocks.append(".")
        else:
            for _ in range(length):
                blocks.append(str(extent["id"]) if type == "file" else ".")
    return blocks


def unpack_disk_map(disk_map):
    extents = []
    for n, c in enumerate(disk_map):
        type = "file" if n % 2 == 0 else "free_space"
        extent = {"type": type, "length": int(c)}
        if n % 2 == 0:
            extent["id"] = n // 2
        extents.append(extent)
    return extents


def part_1(disk_map):
    extents = unpack_disk_map(disk_map)
    blocks = extents_to_blocks(extents)
    compact_blocks(blocks)
    return calc_checksum(blocks)


def part_2(disk_map):
    extents = unpack_disk_map(disk_map)
    compact_extents(extents)
    blocks = extents_to_blocks(extents)
    return calc_checksum(blocks)


def part_n(file_path, fn):
    buffer = []
    with open(file_path, "r") as lines:
        for line in lines:
            buffer.append(line.rstrip("\n"))
    disk_map = "".join(buffer)
    print(fn(disk_map))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

# part = "2"
# file_path = "/Users/adavies/src/github/nalaseivad/advent-of-code-2024/day9/test-input.txt"

if part == "1":
    part_n(file_path, part_1)
elif part == "2":
    part_n(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
