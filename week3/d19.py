import dataclasses
import re

first_rule = 'in'


def split_patterns(lines: list[str]):
    acc = []
    for line in lines:
        if len(line.strip()) == 0:
            if acc:
                yield acc
                acc = []
        else:
            acc.append(line.strip())
    if acc:
        yield acc


part_pattern = re.compile('{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)}')


@dataclasses.dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    def val(self):
        return self.x + self.m + self.a + self.s

    @staticmethod
    def parse(line: str):
        # {x=787,m=2655,a=1222,s=2876}
        m = part_pattern.match(line.strip())
        if m:
            return Part(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))


always_accept = 'A'
always_reject = 'R'


def eval_condition(condition, part) -> bool:
    match condition[0]:
        case 'x':
            att = part.x
        case 'm':
            att = part.m
        case 'a':
            att = part.a
        case s:
            att = part.s
    target = int(condition[2:])
    if condition[1] == '<':
        return att < target
    return att > target


class Rule:
    name: str
    conditions: list[str]

    def __init__(self, name, conditions: list[str]):
        self.name = name
        self.condition = conditions

    def eval(self, part: Part) -> str:
        for c in self.condition:
            # a<2006:qkq
            if ':' in c:
                condition, target = c.split(':')
                if eval_condition(condition, part):
                    return target
            else:
                return c


def parse_rule(line: str):
    f = line.index('{')
    name = line[:f]
    rules = line[f + 1:-1].split(',')
    return Rule(name, rules)


def solve_a(lines: list[str]):
    rules_t, parts = list(split_patterns(lines))
    rules = {r.name: r for r in [parse_rule(r.strip()) for r in rules_t]}
    sum = 0
    for part in [Part.parse(p.strip()) for p in parts]:
        rule = rules[first_rule]
        while rule is not None:
            next = rule.eval(part)
            if next == always_accept:
                sum += part.val()
                break
            elif next == always_reject:
                break
            else:
                rule = rules[next]
    return sum


def and_range(r0: range, r1: range):
    return range(max(r0.start, r1.start), min(r0.stop, r1.stop))


@dataclasses.dataclass
class InputSet:
    x: range
    m: range
    a: range
    s: range

    @staticmethod
    def zero():
        return InputSet(range(0), range(0), range(0), range(0))

    @staticmethod
    def all():
        return InputSet(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))

    def and_r(self, other):
        return InputSet(
            and_range(self.x, other.x),
            and_range(self.m, other.m),
            and_range(self.a, other.a),
            and_range(self.s, other.s))

    def total(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)


def narrow(input: InputSet, rule: str) -> tuple[InputSet, InputSet]:
    def target():
        return int(rule[2:])

    match rule[0]:
        case 'x':
            if rule[1] == '<':
                x_lt = dataclasses.replace(input, x=(range(input.x.start, min(input.x.stop, target()))))
                x_ge = dataclasses.replace(input, x=(range(max(input.x.start, target()), input.x.stop)))
                return x_lt, x_ge
            else:
                x_gt = dataclasses.replace(input, x=(range(max(input.x.start, target() + 1), input.x.stop)))
                x_le = dataclasses.replace(input, x=(range(input.x.start, min(input.x.stop, target()))))
                return x_gt, x_le
        case 'm':
            if rule[1] == '<':
                x_lt = dataclasses.replace(input, m=(range(input.m.start, min(input.m.stop, target()))))
                x_ge = dataclasses.replace(input, m=(range(max(input.m.start, target()), input.m.stop)))
                return x_lt, x_ge
            else:
                x_gt = dataclasses.replace(input, m=(range(max(input.m.start, target() + 1), input.m.stop)))
                x_le = dataclasses.replace(input, m=(range(input.m.start, min(input.m.stop, target()))))
                return x_gt, x_le
        case 'a':
            if rule[1] == '<':
                x_lt = dataclasses.replace(input, a=(range(input.a.start, min(input.a.stop, target()))))
                x_ge = dataclasses.replace(input, a=(range(max(input.a.start, target()), input.a.stop)))
                return x_lt, x_ge
            else:
                x_gt = dataclasses.replace(input, a=(range(max(input.a.start, target() + 1), input.a.stop)))
                x_le = dataclasses.replace(input, a=(range(input.a.start, min(input.a.stop, target()))))
                return x_gt, x_le
        case 's':
            if rule[1] == '<':
                x_lt = dataclasses.replace(input, s=(range(input.s.start, min(input.s.stop, target()))))
                x_ge = dataclasses.replace(input, s=(range(max(input.s.start, target()), input.s.stop)))
                return x_lt, x_ge
            else:
                x_gt = dataclasses.replace(input, s=(range(max(input.s.start, target() + 1), input.s.stop)))
                x_le = dataclasses.replace(input, s=(range(input.s.start, min(input.s.stop, target()))))
                return x_gt, x_le


def and_all(group: list[InputSet]):
    if len(group) == 0:
        return InputSet.zero()
    if len(group) == 1:
        return group[0]
    i = group[0]
    for g in group[1:]:
        i = InputSet.and_r(i, g)
    return i


def solve_b(lines: list[str]):
    rules_t, parts = list(split_patterns(lines))
    rules = {r.name: r for r in [parse_rule(r.strip()) for r in rules_t]}
    rules_accept: dict[str, list[InputSet]] = dict()

    def calc_accept(rule_name: str) -> list[InputSet]:
        if rule_name == 'A':
            return [InputSet.all()]
        if rule_name == 'R':
            return []
        if rule_name in rules_accept:
            return rules_accept[rule_name]

        rule = rules[rule_name]
        current = InputSet.all()
        accepts = []
        for cond in rule.condition:
            if ':' not in cond:
                accepts = accepts + calc_accept(cond)
                pass
            else:
                exp, target = cond.split(':')
                cond_true, cond_false = narrow(current, exp)
                current = cond_false
                accepts = accepts + [cond_true.and_r(r) for r in calc_accept(target)]
        rules_accept[rule_name] = accepts
        return accepts

    accept = calc_accept('in')
    total = sum([c.total() for c in accept])
    # total = 0
    sig = -1
    import itertools
    for i in range(2, len(accept) + 1):
        groups = list(itertools.combinations(accept, i))
        for group in groups:
            r = and_all(group)
            total += sig * r.total()
        # sig = -sig
    return total

# 167409079868000
# 205987200000000
#  65616538878000

print(solve_b('''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''.splitlines()))

# print(solve_a(open('d19.txt').readlines()))
