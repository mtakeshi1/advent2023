import itertools
from typing import Callable, Dict


class MapNodes:
    nodes: Dict[str, tuple[str, str]] = dict()

    def add(self, from_node: str, to_nodes: tuple[str, str]):
        self.nodes[from_node] = to_nodes

    def parse_line(self, line: str):
        if line.strip() == '':
            return
        from_node, to_nodes = (line.strip().replace(' ', '')
                               .replace('(', '')
                               .replace(')', '')
                               .split('='))
        left, right = to_nodes.split(',')
        self.add(from_node, (left, right))

    def navigate(self, instructions: str, from_node='AAA', final_node: Callable = lambda x: x == 'ZZZ'):
        count = 0
        node = from_node
        for next_step in itertools.cycle(instructions):
            prev = node
            if final_node(node):
                break
            if next_step == 'R':
                node = self.nodes[node][1]
            else:
                node = self.nodes[node][0]
            count += 1
            # print(f'{prev} {next_step} {node}')
        return count


def solve(lines: list[str]):
    instructions = lines[0]
    mm = MapNodes()
    for line in lines[2:]:
        mm.parse_line(line)
    return mm.navigate(instructions.strip())


def exists(vals: list[int], func: Callable) -> bool:
    for v in vals:
        if func(v):
            return True
    return False


def lcm(vals: list[int]) -> int:
    b = max(vals)
    r = 1
    for i in range(2, b + 1):
        while exists(vals, lambda x: (x % i) == 0):
            vals = list(map(lambda x: x if (x % i) != 0 else x // i, vals))
            r *= i
    return r


def solve_b(lines: list[str]):
    instructions = lines[0].strip()
    mm = MapNodes()
    for line in lines[2:]:
        mm.parse_line(line)
    all_paths = [
        mm.navigate(instructions, x, lambda xx: xx.endswith('Z'))
        for x in mm.nodes.keys()
        if x.endswith('A')
    ]
    return lcm(all_paths)


if __name__ == '__main__':
    #     print(solve("""RL
    #
    # AAA = (BBB, CCC)
    # BBB = (DDD, EEE)
    # CCC = (ZZZ, GGG)
    # DDD = (DDD, DDD)
    # EEE = (EEE, EEE)
    # GGG = (GGG, GGG)
    # ZZZ = (ZZZ, ZZZ)
    #     """.split('\n')))
    #     print(solve("""LLR
    #
    # AAA = (BBB, BBB)
    # BBB = (AAA, ZZZ)
    # ZZZ = (ZZZ, ZZZ)
    #         """.split('\n')))
    with open('d8.txt', 'r') as file:
        print(solve_b(file.readlines()))
