from dataclasses import dataclass, field
import heapq
from typing import Optional


@dataclass(frozen=True, order=True)
class Position:
    row: int = field(compare=False)
    col: int = field(compare=False)
    direction: str = field(compare=False)
    fwd: int = field(compare=False)
    heat_loss: int = field(compare=True)
    path: Optional[any] = field(compare=False, repr=False, default=None)

    def to_list(self) -> list[any]:
        if self.path is not None:
            tmp = self.path.to_list()
            tmp.append(self)
            return tmp
        return [self]


directions = {'>': (0, 1, '<'), '<': (0, -1, '>'), 'v': (1, 0, '^'), '^': (-1, 0, 'v')}


def solve_a(lines: list[str], max_fwd=2):
    tiles = [[int(x) for x in line.strip()] for line in lines]
    finish = (len(lines) - 1, len(lines[0].strip()) - 1,)
    queue: list[Position] = [Position(0, 0, '.', max_fwd, 0)]
    visited: set[(int, int, str, int)] = set()
    while len(queue) > 0:
        first: Position = heapq.heappop(queue)
        f = (first.row, first.col, first.direction, first.fwd)
        if f in visited:
            continue
        if first.row == finish[0] and first.col == finish[1]:
            hl = first.heat_loss
            print_path(finish, first, tiles)
            return hl

        visited.add(f)

        for direction, vec in directions.items():
            nr = vec[0] + first.row
            nc = vec[1] + first.col
            if 0 <= nr < len(tiles) and 0 <= nc < len(tiles[0]):
                heat = first.heat_loss + tiles[nr][nc]
                if direction == first.direction and first.fwd > 0:
                    heapq.heappush(queue, Position(nr, nc, direction, first.fwd - 1, heat, first))
                elif direction != first.direction and first.direction != vec[2]:
                    heapq.heappush(queue, Position(nr, nc, direction, max_fwd, heat, first))
    print(visited)


def solve_b(lines: list[str], min_fwd=4, max_fwd=10):
    tiles = [[int(x) for x in line.strip()] for line in lines]
    finish = (len(lines) - 1, len(lines[0].strip()) - 1,)
    queue: list[Position] = [Position(0, 0, '>', 0, 0), Position(0, 0, 'v', 0, 0)]
    visited: set[(int, int, str, int)] = set()
    while len(queue) > 0:
        first: Position = heapq.heappop(queue)
        f = (first.row, first.col, first.direction, first.fwd)
        if f in visited:
            continue
        if first.row == finish[0] and first.col == finish[1] and first.fwd >= min_fwd:
            hl = first.heat_loss
            print_path(finish, first, tiles)
            return hl

        visited.add(f)

        for direction, vec in directions.items():
            nr = vec[0] + first.row
            nc = vec[1] + first.col
            if 0 <= nr < len(tiles) and 0 <= nc < len(tiles[0]):
                heat = first.heat_loss + tiles[nr][nc]
                if direction == first.direction and first.fwd < max_fwd:
                    heapq.heappush(queue, Position(nr, nc, direction, first.fwd + 1, heat, first))
                elif direction != first.direction and first.direction != vec[2] and first.fwd >= min_fwd:
                    heapq.heappush(queue, Position(nr, nc, direction, 1, heat, first))
    print(visited)


def print_path(finish, first, tiles):
    path_map = [
        [' ' for x in range(len(tiles[0]))] for _ in range(len(tiles))
    ]
    path_map[finish[0]][finish[1]] = 'F'
    path: list[Position] = first.to_list()
    for i in range(len(path) - 1):
        path_map[path[i].row][path[i].col] = path[i + 1].direction
    for line in path_map:
        print(''.join(line))


sample = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''.splitlines()

print(solve_b(sample))
# print(solve_b('''111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991'''.splitlines()))
print(solve_b(open('d17.txt').readlines()))
