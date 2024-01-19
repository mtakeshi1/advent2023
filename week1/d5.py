import dataclasses
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
    return range(max(fr.start, tr.start), min(fr.stop, tr.stop))


def split_groups(lines: list[str]):
    acc = []
    index = 0
    while index < len(lines):
        if lines[index].strip() == '':
            yield acc
            acc = []
        else:
            acc.append(lines[index])
        index += 1
    yield acc


@dataclasses.dataclass(frozen=True)
class RangeWithOffset:
    init: int
    end: int
    offset: int

    def map(self, n):
        if self.init <= n < self.end:
            return n + self.offset
        pass

    def contains(self, range):
        return self.init <= range.start and self.end >= range.stop


def split_range(source: range, mapping: RangeWithOffset) -> list[range]:
    # if source.start > mapping.end or source.stop < mapping.init:
    #     return [source]
    if mapping.contains(source):
        return [range(source.start + mapping.offset, source.stop + mapping.offset)]

    acc = []

    if source.start < mapping.init <= source.stop:
        acc.append(range(mapping.init + mapping.offset, min(source.stop, mapping.end) + mapping.offset))
        if source.stop > mapping.end:
            acc.append(range(mapping.end, source.stop))
            pass
        source = range(source.start, mapping.init)
        # return [range(source.start, mapping.init), range(mapping.init + mapping.offset, source.stop + mapping.offset)]
    if source.start < mapping.end <= source.stop:
        acc.append(range(source.start + mapping.offset, mapping.end + mapping.offset))
        source = range(mapping.end, source.stop)
    if source.stop > source.start:
        acc.append(source)
    #     return [range(source.start + mapping.offset, mapping.end + mapping.offset), range(mapping.end, source.stop)]
    # return [source]
    return acc


def map_range(source: range, mappings: list[RangeWithOffset]) -> range:
    for rwo in mappings:
        if source.start >= rwo.init and source.stop <= rwo.end:
            return range(source.start + rwo.offset, source.stop + rwo.offset)
    return source


def split_range_all(source: range, mappings: list[RangeWithOffset]) -> list[range]:
    result = []
    bounds = list(set([
        p
        for r in mappings
        for p in [r.init, r.end]
    ] + [source.start, source.stop]))
    bounds.sort()
    for point in bounds:
        if point in source and point > source.start:
            p0 = range(source.start, point)
            source = range(point, source.stop)
            result.append(map_range(p0, mappings))
        if point >= source.stop:
            break
    if source.stop > source.start:
        result.append(map_range(source, mappings))
    return result


def part2(lines: list[str]):
    source = []
    for g in split_groups(lines):
        f = g.pop(0)
        if f.startswith('seeds:'):
            # seeds: 79 14 55 13
            parts = f[7:].split(' ')
            for i in range(len(parts) // 2):
                f = int(parts[2 * i])
                m = int(parts[2 * i + 1])
                source.append(range(f, f + m))
            source.sort(key=lambda t: t[0])
        else:
            ranges = []
            for line in g:
                dst, src, le = line.split(' ')
                ranges.append(RangeWithOffset(int(src), int(src) + int(le), int(dst) - int(src)))
            # print(ranges)
            # print(f'combining {source} with {ranges}')
            source = step(source, ranges)
            # print(source)
            # seed-to-soil map:

            #
            # 50 98 2
            # print(g)
    source.sort(key=lambda t: t.start)
    print(source)


def step(previous: list[range], next_mappings: list[RangeWithOffset]) -> list[range]:
    result = []
    for source in previous:
        result = result + split_range_all(source, next_mappings)
    merge_ranges(result)
    return result


def merge_ranges(result):
    result.sort(key=lambda t: t.start)
    i = 0
    while i < len(result) - 1:
        if result[i].stop >= result[i + 1].start:
            b = result.pop(i + 1)
            a = result.pop(i)
            result.insert(i, range(a.start, b.stop))
        else:
            i += 1


# print(min([map_seed(s) for s in seeds]))

if __name__ == '__main__':
    with open('d5.txt', 'r') as file:
        part2(file.readlines())
    # part2(input.split('\n'))


