import dataclasses


def navigate(lines: list[str]):
    row, col = 0, 0
    graph: set[(int, int)] = set()

    def print_graph():

        len_x = max([x[0] for x in graph]) + 1
        len_y = max([x[1] for x in graph]) + 1
        print('-' * len_y)
        debug = [
            ''.join(['#' if (x, y) in graph else '.' for y in range(len_y)]) for x in range(len_x)
        ]
        print('\n'.join(debug))
        print('-' * len_y)

    # R 6 (#70c710)
    for line in lines:
        direction, steps, _ = line.strip().split(' ')
        delta_x, delta_y = 0, 0
        sig_x, sig_y = 1, 1
        match direction:
            case 'U':
                delta_x = int(steps)
                sig_x = -1
            case 'D':
                delta_x = int(steps)
            case 'L':
                delta_y = int(steps)
                sig_y = -1
            case 'R':
                delta_y = int(steps)
        for x in range(delta_x + 1):
            for y in range(delta_y + 1):
                graph.add((row + (sig_x * x), col + (sig_y * y),))
        row += sig_x * delta_x
        col += sig_y * delta_y
        # print_graph()
    return graph


def solve_a(lines: list[str]):
    graph = {x: True for x in navigate(lines)}
    len_x = max([x[0] for x in graph.keys()]) + 1
    len_y = max([x[1] for x in graph.keys()]) + 1

    min_x = min([x[0] for x in graph.keys()])
    min_y = min([x[1] for x in graph.keys()])

    def symbol(x, y):
        if (x, y) in graph:
            return '#' if graph[(x, y)] else ' '
        return '.'

    def print_graph():
        debug = [
            ''.join([symbol(x, y) for y in range(min_y, len_y)]) for x in range(min_x, len_x)
        ]
        print('\n'.join(debug))

    print_graph()

    def out_of_bounds(x: int, col: int) -> bool:
        return x < min_x or x >= len_x or col < min_y or col >= len_y

    def find_hole(x, y, dx, dy):
        """
        Returns True if it finds a hole in that direction. False if it reaches the edge of the 'screen'
        """
        while min_x <= x < len_x and min_y <= y < len_y:
            if (x, y) in graph:
                return graph[(x, y)]
            x += dx
            y += dy
        return False

    def surrounded(x: int, col: int) -> bool:
        if (x, col) in graph:
            return graph[(x, col)]
        if out_of_bounds(x, col):
            return False
        im_surrounded = find_hole(x, col, -1, 0) and find_hole(x, col, 1, 0) and find_hole(x, col, 0, -1) and find_hole(
            x, col, 0, 1)
        graph[x, col] = im_surrounded
        return im_surrounded

    for x in range(min_x, len_x):
        for y in range(min_y, len_y):
            surrounded(x, y)
    print('-' * len_y)
    print_graph()
    print('-' * len_y)

    with open('img1.pgm', 'w') as file:
        file.write(f'P2\n{len_y - min_y} {len_x - min_x}\n20\n')
        edges = navigate(lines)

        def s(x, y):
            if (x, y) in edges:
                return '10'
            if (x, y) in graph:
                return '20' if graph[(x, y)] else '0'
            return '0'

        lines = [
            (' '.join([s(x, y) for y in range(min_y, len_y)]) + '\n') for x in range(min_x, len_x)
        ]
        file.writelines(lines)

    # def print_graph():
    #     debug = [
    #         ''.join([symbol(x, y) for y in range(min_y, len_y)]) for x in range(min_x, len_x)
    #     ]
    # print('\n'.join(debug))

    return len([x for x, y in graph.items() if y])


def solve_a2(lines: list[str]):
    graph = {x: True for x in navigate(lines)}
    len_x = max([x[0] for x in graph.keys()]) + 1
    len_y = max([x[1] for x in graph.keys()]) + 1

    min_x = min([x[0] for x in graph.keys()])
    min_y = min([x[1] for x in graph.keys()])

    queue = ([(min_x, y) for y in range(min_y, len_y) if (0, y) not in graph] +
             [(len_x - 1, y) for y in range(min_y, len_y) if (len_x - 1, y) not in graph] +
             [(x, min_y) for x in range(min_x, len_x) if (x, 0) not in graph] +
             [(x, len_y - 1) for x in range(min_x, len_x) if (x, len_y - 1) not in graph])
    dirs = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    while len(queue) > 0:
        first = queue.pop()
        if first in graph:
            continue
        graph[first] = False
        for dx, dy in dirs:
            nx = first[0] + dx
            ny = first[1] + dy
            if (nx, ny) not in graph and min_x <= nx < len_x and min_y <= ny < len_y:
                queue.append((nx, ny,))
    for x in range(min_x, len_x):
        for y in range(min_y, len_y):
            if (x, y) not in graph:
                graph[(x, y)] = True

    write_file(len_x, len_y, lines, min_x, min_y, graph)
    return (len_x - min_x) * (len_y - min_y) - (len([x for x, y in graph.items() if not y]))
    #


def write_file(len_x, len_y, lines, min_x, min_y, graph, f_name='img2.pgm'):
    with open(f_name, 'w') as file:
        file.write(f'P2\n{len_y - min_y} {len_x - min_x}\n20\n')
        edges = navigate(lines)

        def s(x, y):
            if (x, y) in edges:
                return '10'
            if (x, y) in graph:
                return '20' if graph[(x, y)] else '0'
            return '20'

        lines = [
            (' '.join([s(x, y) for y in range(min_y, len_y)]) + '\n') for x in range(min_x, len_x)
        ]
        file.writelines(lines)


@dataclasses.dataclass(frozen=True)
class Rect:
    x0: int
    y0: int
    x1: int
    y1: int

    def size(self):
        return abs(self.x1 - self.x0) * (self.y1 - self.y0)


def solve_b(lines: list[str]):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    row, col = 0, 0
    rows = set()
    cols = set()
    rects = dict()
    for line in lines:
        ins = line.strip().split(' ')[-1][2:-1]
        amount = int(ins[:5], 16)
        dx, dy = dirs[int(ins[-1])]
        nx = row + dx * amount
        ny = col + dy * amount
        rows.add(nx)
        cols.add(ny)
        if dx > 0:
            rects[Rect(row, col, nx, ny + 1)] = True
            cols.add(ny + 1)
        else:
            rects[Rect(row, col, nx + 1, ny)] = True
            rows.add(nx + 1)
        row, col = nx, ny

    rows = list(sorted(rows))
    cols = list(sorted(rows))
    num_rows = len(rows) - 1
    num_cols = len(cols) - 1

    def rect_for(x, y):
        return Rect(rows[x], cols[y], rows[x + 1], cols[y + 1])

    queue = ([(0, y) for y in range(0, num_cols - 1) if rect_for(0, y) not in rects] +
             [(num_rows - 1, y) for y in range(0, num_cols - 1) if rect_for(num_rows - 1, y) not in rects] +
             [(x, 0) for x in range(0, num_rows) if rect_for(x, 0) not in rects] +
             [(x, num_cols - 1) for x in range(0, num_rows - 1) if rect_for(x, num_cols - 1) not in rects])

    while len(queue) > 0:
        first = queue.pop()
        if first in rects:
            continue
        rects[rect_for(*first)] = False
        for dx, dy in dirs:
            nx = first[0] + dx
            ny = first[1] + dy
            if 0 <= nx < num_rows and 0 <= ny < num_cols and rect_for(nx, ny) not in rects:
                queue.append((nx, ny,))
    print(''.join(["{:7d}".format(c) for c in cols]))
    for row in range(num_rows):
        pre = '{:7d}'.format(rows[row])
        for col in range(num_cols):
            rect = rect_for(row, col)
            if rect in rects.keys():
                if rects.get(rect):
                    c = '  ###  '
                else:
                    c = ' ' * 7
            else:
                c = '  ???  '
            pre += c
        print(pre)
    for x in range(num_rows):
        for y in range(num_cols):
            r = rect_for(x, y)
            if r not in rects:
                rects[r] = True
    print(f'{len(rows)} x {len(cols)}')
    return sum([k.size() for k, v in rects.items() if v])


#
print(solve_b('''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''.splitlines()))

# print(solve_b(open('d18.txt').readlines()))
