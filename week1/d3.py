import dataclasses
import functools

def is_digit(c):
    return ord('0') <= ord(c) <= ord('9')


def is_symbol(c):
    if c == '.' or is_digit(c):
        return False
    return True


@dataclasses.dataclass(frozen=True)
class NumRange:
    row: int
    col: int

    len: int

    def int_val(self, board):
        iv = int(board[self.row][self.col:self.col + self.len])
        return iv

    def is_part_number(self, board):
        rows = range(self.row - 1, self.row + 2)
        cols = range(self.col - 1, self.col + self.len + 1)
        for r in rows:
            if r < 0 or r >= len(board):
                continue
            for c in cols:
                if 0 <= c < len(board[r]):
                    if is_symbol(board[r][c]):
                        return True
                    pass
        return False


def parse_ranges(row, row_i, col_i=0) -> list[NumRange]:
    if col_i >= len(row):
        return list()
    i = col_i
    while i < len(row) and is_digit(row[i]):
        i += 1

    rest = parse_ranges(row, row_i, i + 1)
    if i > col_i:
        r = NumRange(row_i, col_i, i - col_i)
        rest.insert(0, r)

    return rest


ex_input = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''


def find_num_at(board, row, col) -> NumRange:
    left = col
    right = col+1
    while left > 0 and is_digit(board[row][left]):
        left -= 1
    while right < len(board[row]) and is_digit(board[row][right]):
        right += 1
    return NumRange(row, left+1, right - left-1)


def search_nums(board, row, col) -> list[NumRange]:
    r = list()
    for x in range(row-1, row+2):
        if x < 0 or x >= len(board):
            continue
        for y in range(col-1, col+2):
            if y < 0 or y >= len(board[x]):
                continue
            if is_digit(board[x][y]):
                n = find_num_at(board, x, y)
                r.append(n)
    return r


def part_2(board):
    acc = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == '*':
                nums = set(search_nums(board, row, col))
                if len(nums) == 2:
                    acc += functools.reduce(lambda a,b: a.int_val(board)*b.int_val(board), nums)
    print(acc)


if __name__ == '__main__':
    with open('d3.txt') as file:
        board = [x.strip() for x in file.readlines()]
        num_ranges = [parse_ranges(line, row) for row, line in enumerate(board)]
        print(sum([n.int_val(board) for l in num_ranges for n in l if n.is_part_number(board)]))
        part_2(board)
