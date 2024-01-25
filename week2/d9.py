def for_all(input_v, predicate):
    for v in input_v:
        if not predicate(v):
            return False
    return True


def exists(input_v, predicate):
    for v in input_v:
        if predicate(v):
            return True
    return False


def next_sequence(source: list[int]) -> list[int]:
    return [
        source[i] - source[i - 1]
        for i in range(1, len(source))
    ]


def all_sequences_from(source: list[int]) -> list[list[int]]:
    r = [source]
    while exists(source, lambda x: x != 0):
        source = next_sequence(source)
        r.append(source)
    return r


def solve_one_a(source: list[int]) -> int:
    rr = all_sequences_from(source)
    rr.reverse()
    n = []
    for i in range(1, len(rr)):
        seq = rr[i]
        prev = rr[i - 1]
        num = seq[-1] + prev[-1]
        seq.append(num)
        n.append(num)
    # print(n)
    return n[-1]


def solve_one_b(source: list[int]) -> int:
    rr = all_sequences_from(source)
    rr.reverse()
    n = []
    for i in range(1, len(rr)):
        seq = rr[i]
        prev = rr[i - 1]
        num = seq[0] - prev[0]
        seq.insert(0, num)
        seq.append(num)
        n.append(num)
    # print(n)
    return n[-1]


def solve_a(lines: list[str]):
    s = 0
    for line in lines:
        if line:
            a = list(map(lambda x: int(x), line.strip().split(' ')))
            s += solve_one_a(a)
    return s


def solve_b(lines: list[str]):
    s = 0
    for line in lines:
        if line:
            a = list(map(lambda x: int(x), line.strip().split(' ')))
            s += solve_one_b(a)
    return s


print(solve_b("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".split('\n')))

# print(solve_a([0, 3, 6, 9, 12, 15]))
with open('d9.txt', 'r') as file:
    print(solve_b(file.readlines()))
