import math

sample = """Time:        63     78     94     68
Distance:   411   1274   2047   1035
"""


def solve(total_time: int, min_distance: int) -> tuple[float, float]:
    b = -total_time
    a = 1
    c = min_distance
    delta = b * b - 4 * a * c
    x0 = (-b - math.sqrt(delta)) / (2 * a)
    x1 = (-b + math.sqrt(delta)) / (2 * a)
    return x0, x1


def parse(lines: list[str]):
    times = []
    distances = []
    for line in lines:
        if line.startswith('Time:'):
            times = [int(x) for x in line[5:].strip().split(' ') if len(x) > 0]
        elif line.startswith('Distance:'):
            distances = [int(x) for x in line[10:].strip().split(' ') if len(x) > 0]
        if times and distances:
            break
    if len(times) != len(distances):
        raise Exception(f'lengths mismatch: {len(times)} and {len(distances)}')
    return zip(times, distances)


if __name__ == '__main__':
    r = 1
    # for T, D in parse(sample.split('\n')):
    #     x0, x1 = solve(T, D + 1)
    #     a0 = math.ceil(x0)
    #     a1 = math.floor(x1)
    #     # print(f'x={x0, x1}')
    #     # print(f'a={a0, a1}')
    #     rr = a1 - a0 + 1
    #     # print(f'diff: {rr}')
    #     # if rr > 0:
    #         # r *= rr

    x0, x1 = solve(63789468, 411127420471035 + 1)
    a0 = math.ceil(x0)
    a1 = math.floor(x1)
    # print(f'x={x0, x1}')
    # print(f'a={a0, a1}')
    rr = a1 - a0 + 1
    # print(f'diff: {rr}')
    if rr > 0:
        r *= rr
    print(r)
