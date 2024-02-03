input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

def distance(gal1, gal2):
    return abs(gal1[0] - gal2[0]) + abs(gal1[1] - gal2[1])

def solve(lines):
    cols_plus = [0 for i in range(len(lines[0]))]
    rows_plus = [0 for i in range(len(lines))]
    galaxies = []
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == '#':
                galaxies.append((row, col,))
    
    empty_cols = [[lines[x][col] for x in range(len(lines)) if lines[x][col] == '#'] for col in range(len(lines[0]))]
    # print(empty_cols)
    empty_rows = [[lines[row][x] for x in range(len(lines[0])) if lines[row][x] == '#'] for row in range(len(lines))]
    # print(empty_rows)
    num_exp = 1000000-1
    exp = 0
    for col in range(len(empty_cols)):
        if empty_cols[col] == []:
            exp += num_exp
        cols_plus[col] = exp
    exp = 0
    for row in range(len(empty_rows)):
        if empty_rows[row] == []:
            exp += num_exp
        rows_plus[row] = exp

    # print(cols_plus)
    # print(rows_plus)
    galaxies = [
        (g[0] + rows_plus[g[0]], g[1] + cols_plus[g[1]], ) for g in galaxies
    ]
    import itertools
    all_pairs = list(itertools.combinations(galaxies, 2))
    return sum([
        distance(*x) for x in all_pairs
    ])
    # print(len(all_pairs))
    

print(solve([c.strip() for c in input.split('\n')]))

with open('week2/d11.txt') as file:
    print(solve([c.strip() for c in file.readlines()]))