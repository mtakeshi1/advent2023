import unittest

from week1.d5 import RangeWithOffset, split_range


class MyTestCase(unittest.TestCase):
    sources = [range(79, 79 + 14), range(55, 55 + 13)]

    seed_to_soil = [
        RangeWithOffset(init=98, end=100, offset=-48),
        RangeWithOffset(init=50, end=50 + 48, offset=2)
    ]

    def test_map_simple(self):
        r0 = RangeWithOffset(init=98, end=100, offset=-48)
        self.assertEqual(50, r0.map(98))  # add assertion here

    def test_split_range_fully_contained(self):
        # [79, 94[
        # map to
        # [50, 99[ -> offset + 2
        r0 = split_range(source=self.sources[0], mapping=self.seed_to_soil[1])
        print(r0)
        self.assertEqual(1, len(r0))
        self.assertEqual(range(81, 95), r0[0])

    def test_split_range_left(self):
        r0 = split_range(source=range(40, 61), mapping=RangeWithOffset(init=50, end=50 + 48, offset=2))
        print(r0)
        self.assertEqual(2, len(r0))
        self.assertTrue(range(40, 50) in r0)
        self.assertTrue(range(52, 63) in r0)

    def test_split_range_right(self):
        r0 = split_range(source=range(90, 100), mapping=RangeWithOffset(init=80, end=95, offset=-10))
        print(r0)
        self.assertEqual(2, len(r0))
        self.assertTrue(range(95, 100) in r0)
        self.assertTrue(range(80, 85) in r0)

    def test_source_bigger(self):
        r0 = split_range(source=range(70, 100), mapping=RangeWithOffset(init=80, end=95, offset=+100))
        print(r0)
        self.assertEqual(3, len(r0))
        self.assertTrue(range(70, 80) in r0)
        self.assertTrue(range(180, 195) in r0)
        self.assertTrue(range(95, 100) in r0)


if __name__ == '__main__':
    unittest.main()
