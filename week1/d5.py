import re

input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def nums(line: str):
    return [int(c) for c in re.findall(r"\d+", line)]


def split_empty(lines: list[str], start_from: int = 0):
    acc = list()
    for i in range(start_from, len(lines)):
        if lines[i].strip() == '':
            yield acc
            acc = list()
        else:
            acc.append(lines[i].strip())
    if acc:
        yield acc


def parse_group_header(line: str):
    m = re.search(r"(.+)-to(.+) ", line)
    if m:
        return m.group(1), m.group(2)


def parse_ranges(lines: list[str]) -> dict[range, range]:
    nn = [nums(t) for t in lines]
    return {
        range(src_start, src_start + size): range(dst_start, dst_start + size)
        for dst_start, src_start, size in nn
    }


def parse_input(lines: list[str]):
    seeds = nums(lines[0])
    groups = split_empty(lines, 2)
    mappings = []
    for group in groups:
        mappings.append(parse_ranges(group[1:]))
    print(f'seeds: {seeds}')
    for m in mappings:
        print(f'mappings: {m}')

    def map_seed(seed):
        i = 0
        for m in mappings:
            tmp = seed
            for f, t in m.items():
                if seed in f:
                    offset = seed - f[0]
                    seed = t[0] + offset
                    break
            print(f'{i} -> {tmp} mapping to {seed} ')
            i += 1
        return seed

    print(min([map_seed(s) for s in seeds]))


def range_intersection(fr: range, tr: range) -> range:
    return range(max(fr[0], tr[0]), min(fr[-1], tr[-1]) + 1)


def part2(lines: list[str]):
    seeds = nums(lines[0])
    groups = split_empty(lines, 2)
    mappings = []
    for group in groups:
        mappings.append(parse_ranges(group[1:]))

    starting = [range(a, b) for (a, b) in zip(seeds, seeds[1:])]
    for m in mappings:
        starting = sorted(starting)
        for f, t in m.items():
            pass

            # inter = range_intersection(r, f)
            # inter_len = len(inter)
            # if inter_len > 0:
            #     new_start = max(inter.start, t.start)
            #     break
            # pass


# print(min([map_seed(s) for s in seeds]))


parse_input(input.split('\n'))

with open('d5.txt', 'r') as file:
    part2(file.readlines())
