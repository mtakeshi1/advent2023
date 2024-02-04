sample = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

expected = 136


def calculate_load(input: list[str]):
    total = 0
    h = len(input)
    for line in input:
        total += h * line.count('O')
        h -= 1
    return total
    


def tilt_north_col(input: list[str], column: int) -> tuple[int, str]:
    top = 0
    load = 0
    rows = len(input)
    col = [input[c][column] for c in range(rows)]
    for i in range(len(input)):
        match input[i][column]:
            case 'O':
                col[i] = '.'
                col[top] = 'O'
                load += rows - top
                top = top + 1
            case '#':
                top = i + 1
    return load, ''.join(col)


def tilt_north(input: list[str]) -> tuple[int, str]:
    total_load = 0
    cols: list[str] = []
    for i in range(len(input[0])):
        l, c = tilt_north_col(input, i)
        total_load += l
        cols.append(c)
    m = []
    for row_i in range(len(input)):
        line = ''.join([cols[c][row_i] for c in range(len(cols))])
        m.append(line)
    return total_load, '\n'.join(m)


def tilt_south_col(input: list[str], column: int):
    load = 0
    rows = len(input)
    top = rows - 1
    col = [input[c][column] for c in range(rows)]
    i = top
    while i >= 0:
        match input[i][column]:
            case 'O':
                col[i] = '.'
                col[top] = 'O'
                load += rows - top
                top = top - 1
            case '#':
                top = i - 1
        i -= 1
    return ''.join(col)


def tilt_south(input: list[str]) -> str:
    cols: list[str] = []
    for i in range(len(input[0])):
        c = tilt_south_col(input, i)
        cols.append(c)
    m = []
    for row_i in range(len(input)):
        line = ''.join([cols[c][row_i] for c in range(len(cols))])
        m.append(line)
    return '\n'.join(m)


def tilt_west_row(input: list[str], row_i: int) -> str:
    row = [c for c in input[row_i]]
    top = 0
    for col_i in range(len(input[row_i])):
        if input[row_i][col_i] == 'O':
            row[col_i] = '.'
            row[top] = 'O'
            top = top + 1
        elif input[row_i][col_i] == '#':
            top = col_i + 1
        
    return ''.join(row)

def tilt_west(input: list[str]):
    rows = [tilt_west_row(input, row_i) for row_i in range(len(input))]
    return '\n'.join(rows)


def tilt_east_row(input: list[str], row_i: int) -> str:
    row = [c for c in input[row_i]]
    col_i = len(input[row_i]) - 1
    top = col_i
    # for col_i in range(len(input[row_i])):
    while col_i >= 0:
        if input[row_i][col_i] == 'O':
            row[col_i] = '.'
            row[top] = 'O'
            top = top - 1
        elif input[row_i][col_i] == '#':
            top = col_i - 1
        col_i -= 1
        
    return ''.join(row)


def tilt_east(input: list[str]):
    rows = [tilt_east_row(input, row_i) for row_i in range(len(input))]
    return '\n'.join(rows)

def cycle(input: list[str]):
    _, m = tilt_north(input)
    # print(m)
    # print('----------------------------')
    m = tilt_west(m.splitlines())
    # print(m)
    # print('----------------------------')
    m = tilt_south(m.splitlines())
    # print(m)
    # print('----------------------------')
    return tilt_east(m.splitlines())

def cycles(input: list[str], n):
    m = input
    for i in range(n):
        m = cycle(input)
        input = m.splitlines()
    return ''.join(m)

def solve_b(input: list[str]):
    n = 1000000000
    known = dict()
    m:str = '\n'.join([c.strip() for c in input])
    # known.add(m)
    while m not in known:
        known[m] = len(known)
        m = cycle(m.splitlines())
    n -= known[m]
    r = n % (len(known) - known[m])

    m = cycles(m.splitlines(), r)
    print(calculate_load(m.splitlines()))

# print(tilt_north(sample.splitlines())[1])
# print(cycles(sample.splitlines(), 3))
solve_b(sample.splitlines())
with open('week2/d14.txt') as file:
    solve_b(file.readlines())
#     print(tilt_north([c.strip() for c in file.readlines()]))
