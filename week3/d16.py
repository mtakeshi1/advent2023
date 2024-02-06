import copy


def move(row, col, direction, tiles) -> list[(int, int, str)]:
    if 0 <= row < len(tiles) and 0 <= col < len(tiles[row]):
        next_tile = tiles[row][col]
        match direction, next_tile:
            case ('>', '|') | ('<', '|'):
                return [(row + 1, col, 'v'), (row - 1, col, '^')]
            case ('^', '-') | ('v', '-'):
                return [(row, col - 1, '<'), (row, col + 1, '>')]

            case ('>', '/'):
                return [(row - 1, col, '^')]
            case ('>', '\\'):
                return [(row + 1, col, 'v')]

            case ('<', '/'):
                return [(row + 1, col, 'v')]
            case ('<', '\\'):
                return [(row - 1, col, '^')]

            case ('^', '/'):
                return [(row, col + 1, '>')]
            case ('^', '\\'):
                return [(row, col - 1, '<')]

            case ('v', '/'):
                return [(row, col - 1, '<')]
            case ('v', '\\'):
                return [(row, col + 1, '>')]

    match direction:
        case '>':
            return [(row, col + 1, direction)]
        case '<':
            return [(row, col - 1, direction)]
        case '^':
            return [(row - 1, col, direction)]
        case 'v':
            return [(row + 1, col, direction)]
    return [(row, col, direction)]


def solve_a(lines: list[str], starting=(0, 0, '>')):
    tiles = [list(line.strip()) for line in lines]
    lit: set[tuple[int, int]] = set()
    beams: list[tuple[int, int, str]] = [starting]
    tiles[starting[0]][starting[1]] = '.'

    def debug():
        to_print = copy.deepcopy(tiles)
        for r, c, d in beams:
            to_print[r][c] = d
        for line in to_print:
            print(''.join(line))
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    def show_lit():
        to_print = [
            ['.' for x in range(len(tiles[0]))]
            for _ in lines
        ]
        for r, c in lit:
            to_print[r][c] = '#'
        for line in to_print:
            print(''.join(line))

    visited = set()
    t = 0
    while beams:
        next_turn = []
        # print(f'turn: {t}')
        # debug()
        # t += 1
        for beam in beams:
            if beam in visited:
                continue
            row, col, direction = beam
            visited.add(beam)
            lit.add((row, col,))
            nbs = move(row, col, direction, tiles)
            next_turn = next_turn + [new_beam for new_beam in nbs if
                                     new_beam not in visited and 0 <= new_beam[0] < len(tiles) and 0 <= new_beam[
                                         1] < len(tiles[0])]
        beams = next_turn
    # show_lit()
    return len(lit)


def solve_b(lines: list[str]):
    cols = len(lines[0].strip())
    all_starting = ([(row, 0, '>') for row in range(len(lines))] +
                    [(row, cols - 1, '<') for row in range(len(lines))] +
                    [(0, c, 'v') for c in range(cols)] +
                    [(len(lines) - 1, c, '^') for c in range(cols)])
    return max([solve_a(lines, s) for s in all_starting])


sample = '''.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''

print(solve_b(sample.splitlines()))
print(solve_b(open('d16.txt').readlines()))
