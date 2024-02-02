import dataclasses
from typing import Dict, List, Optional


@dataclasses.dataclass(unsafe_hash=True, frozen=True)
class Node:
    row: int
    col: int

    def north(self):
        return Node(row=self.row - 1, col=self.col)

    def west(self):
        return Node(row=self.row, col=self.col - 1)

    def south(self):
        return Node(row=self.row + 1, col=self.col)

    def east(self):
        return Node(row=self.row, col=self.col + 1)

    def cell(self, graph):
        return graph.nodes.get(self, '.')

    def neighbours(self, graph):
        match self.cell(graph):
            case 'S':
                n = []
                if self.north().cell(graph) in ['|', 'F', '7']:
                    n.append(self.north())
                if self.west().cell(graph) in ['F', 'L', '-']:
                    n.append(self.west())
                if self.east().cell(graph) in ['-', 'J', '7']:
                    n.append(self.east())
                if self.south().cell(graph) in ['|', 'J', 'L']:
                    n.append(self.south())
                return n

            case '|':
                return [self.north(), self.south()]
            case '-':
                return [self.east(), self.west()]
            case 'J':
                return [self.west(), self.north()]
            case 'L':
                return [self.north(), self.east()]
            case '7':
                return [self.west(), self.south()]
            case 'F':
                return [self.east(), self.south()]
        return []


@dataclasses.dataclass(frozen=True)
class Link:
    node: Node
    next: Optional[any] = None

    def __len__(self):
        if self.next:
            return 1 + len(self.next)
        return 1

    def all_values(self):
        n = self
        while n is not None:
            yield n.node
            n = n.next

    def prepend(self, nn: Node):
        return Link(nn, next=self)

    def has_next(self):
        return self.next is not None


class Graph:
    nodes: Dict[Node, str] = dict()
    start: Node | None = None
    rows: int = 0
    cols: int = 0

    def add_lines(self, lines: list[str]):
        for row_i, row in enumerate(lines):
            for col_i, cell in enumerate(row):
                node = Node(row=row_i, col=col_i)
                self.nodes[node] = cell
                if cell == 'S':
                    self.start = node
            self.cols = max(self.cols, len(row))
        self.rows = len(lines)

    def print(self, nodes):
        needed = set(nodes)
        for i in range(self.rows):
            row = [Node(i, x) for x in range(self.cols)]
            line = [self.nodes[node] if node in needed else ' ' for node in row]
            print(''.join(line))

    def solve(self):
        queue = []
        visited = set()
        max_len = 0
        queue.append((self.start, 0,))
        while len(queue) > 0:
            node, path_len = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            max_len = max(max_len, path_len)
            for n in node.neighbours(self):
                if n not in visited:
                    queue.append((n, path_len + 1,))
        return max_len

    def find_fences(self):
        queue: List[Link] = []
        visited = {self.start}
        start, goal = self.start.neighbours(self)
        queue.append(Link(start, Link(self.start)))

        while len(queue) > 0:
            link = queue.pop(0)
            if link.node in visited:
                continue
            if link.node == goal:
                return link.all_values()
            visited.add(link.node)
            for n in link.node.neighbours(self):
                if n not in visited:
                    queue.append(link.prepend(n))

    def solve_b(self):
        fences = set(self.find_fences())
        self.print(fences)
        low = min([n.row for n in fences])
        high = max([n.row for n in fences]) + 1
        count = 0
        for row_i in range(low, high):
            row = sorted([n.col for n in fences if n.row == row_i])
            inside = True
            for col_i in range(1, len(row)):
                if inside:
                    count += row[col_i] - row[col_i - 1] - 1
                inside = not inside

        # print(fences)
        return count


input = """ ...........
            .S-------7.
            .|F-----7|.
            .||.....||.
            .||.....||.
            .|L-7.F-J|.
            .|..|.|..|.
            .L--J.L--J.
            ..........."""

graph = Graph()
graph.add_lines([c.strip() for c in input.split('\n')])
print(graph.solve_b())

with open('d10.txt', 'r') as file:
    graph = Graph()
    graph.add_lines([c.strip() for c in file.readlines()])
    print(graph.solve_b())
