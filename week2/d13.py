sample = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''


def split_patterns(lines: list[str]):
    acc = []
    for line in lines:
        if len(line.strip()) == 0:
            if acc:
                yield acc
                acc = []
        else:
            acc.append(line.strip())
    if acc:
        yield acc

def find_horizontal(pattern: list[str]):
    results = []
    for i in range(1, len(pattern) - 1):
        limit = min(i, len(pattern) - i)
        broke = False
        for j in range(0, limit):
            if pattern[i-j-1] != pattern[i + j]:
                broke = True
                break
        if not broke:
            results.append(i)
    return results

def transpose(l: list[list[any]]):
    cols = [ 
        [l[r][x] for r in range(len(l))] 
            for x in range(len(l[0]))
    ]
    return cols

def find_vertical(pattern: list[str]):
    return find_horizontal(transpose(pattern))


def solve(lines):
    s = 0
    for pattern in split_patterns(lines):
        # print(f'solving {pattern}')
        verticals = find_vertical(pattern)
        s += sum(verticals)
        horizontals = find_horizontal(pattern)
        s += sum([x * 100 for x in horizontals])
    return s

# print(solve(sample.splitlines()))

with open('week2/d13.txt') as file:
    print(solve(file.readlines()))