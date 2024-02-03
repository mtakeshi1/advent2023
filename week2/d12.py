import itertools

input = ''' ???.### 1,1,3
            .??..??...?##. 1,1,3
            ?#?#?#?#?#?#?#? 1,3,1,6
            ????.#...#... 4,1,1
            ????.######..#####. 1,6,5
            ?###???????? 3,2,1'''


class Solver:
    def __init__(self):
        self.cache = dict()

    def correct(equips, records):
        
        pass

    def solutions(self, equips, records):
        if len(records) == 0:
            # if next(filter(lambda x: x == '#', equips)):
                # return 0
            if equips.count('#') > 0:
                return 0
            return 1
        if len(equips) == 0:
            return 0
        i = 0
        # ignore leading dots
        while i < len(equips) and equips[i] == '.':
            i += 1
        if i < len(equips):
            equips = equips[i:]
        key = equips + '|' + str(records)
        if key in self.cache:
            return self.cache[key]
        i = 0
        while i < len(equips) and equips[i] == '#':
            i += 1
        # if i >= len(equips):
        #     self.cache[key] = 0
        #     return 0
        if i == len(equips) or equips[i] == '.':
            g0 = equips[:i]
            rest = equips[i+1:]
            if len(list(filter(lambda x: x == '#', g0))) == records[0]:
                x = self.solutions(rest, records[1:])
            else:
                x = 0
            self.cache[key] = x
            return x
        # equips[i] == '?':
        copy = equips[:i] + '.' + equips[i+1:]
        r0 = self.solutions(copy, records)
        copy = equips[:i] + '#' + equips[i+1:]
        r1 = self.solutions(copy, records)
        self.cache[key] = r0 + r1
        return r0 + r1

    def calculate(self, line):
        conditions, records = line.strip().split(' ')
        records = [int(x) for x in records.split(',')]
        ss = self.solutions(conditions, records)
        return ss
    
    def calculate_b(self, line):
        conditions, records = line.strip().split(' ')
        records = [int(x) for x in records.split(',')]
        conditions = (conditions + '?') * 5
        conditions = conditions[:-1]
        ss = self.solutions(conditions, records * 5)
        return ss
    

# s = Solver()
# print(s.calculate('???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3'))

# s = Solver()
# print(s.calculate_b('???.### 1,1,3'))

sum = 0
for line in input.splitlines():
    s = Solver()
    # print(line)
    # print(s.calculate_b(line))

with open('week2/d12.txt') as file:
    for line in file.readlines():
        s = Solver()
        # print(line)
        sum += s.calculate_b(line)

print(sum)