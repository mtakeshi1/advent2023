import dataclasses


def hash_for(msg: str) -> int:
    h = 0
    for c in msg:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


def all_hash(msg: str):
    return sum([hash_for(piece) for piece in msg.strip().split(',')])


@dataclasses.dataclass(frozen=False)
class Lens:
    label: str
    focus: int


class Solver:
    boxes: dict[int, list[Lens]]

    def __init__(self):
        self.boxes = {}

    def cmd(self, line: str):
        for cmd in line.strip().split(','):
            if '=' in cmd:
                label, focus_s = cmd.split('=')
                self.add(label, int(focus_s))
            else:
                label = cmd[:-1]
                self.remove(label)
        return self.total_focus_power()

    def add(self, lens_label: str, focus: int):
        index = hash_for(lens_label)
        box = self.boxes.get(index, [])
        found = False
        for lens in box:
            if lens.label == lens_label:
                found = True
                lens.focus = focus
                break
        if not found:
            box.append(Lens(lens_label, focus))
        self.boxes[index] = box

    def remove(self, lens_label: str):
        index = hash_for(lens_label)
        box = self.boxes.get(index, [])
        nb = list(filter(lambda x: x.label != lens_label, box))
        self.boxes[index] = nb

    def total_focus_power(self):
        s = 0
        for box_num, box in self.boxes.items():
            s += sum(
                (box_num + 1) * (slot + 1) * lens.focus
                for slot, lens in enumerate(box)
            )
        return s


# print(hash_for('rn=1'))
sample = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
# print(all_hash(sample))
s = Solver()
print(s.cmd(sample))
#
with open('d15.txt') as file:
    # print(all_hash(file.readline()))
    s = Solver()
    print(s.cmd(file.readline()))
