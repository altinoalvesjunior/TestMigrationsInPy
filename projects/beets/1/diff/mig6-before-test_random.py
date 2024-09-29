import math
import unittest
from random import Random

from beets import random
from beets.test.helper import TestHelper


class RandomTest(TestHelper, unittest.TestCase):
    def test_equal_permutation(self):
        """We have a list of items where only one item is from artist1 and the
        rest are from artist2. If we permute weighted by the artist field then
        the solo track will almost always end up near the start. If we use a
        different field then it'll be in the middle on average.
        """

        def experiment(field, histogram=False):
            """Permutes the list of items 500 times and calculates the position
            of self.item1 each time. Returns stats about that position.
            """
            positions = []
            for _ in range(500):
                shuffled = list(
                    random._equal_chance_permutation(
                        self.items, field=field, random_gen=self.random_gen
                    )
                )
                positions.append(shuffled.index(self.item1))
            # Print a histogram (useful for debugging).
            if histogram:
                for i in range(len(self.items)):
                    print("{:2d} {}".format(i, "*" * positions.count(i)))
            return self._stats(positions)

        mean1, stdev1, median1 = experiment("artist")
        mean2, stdev2, median2 = experiment("track")
        self.assertAlmostEqual(0, median1, delta=1)
        self.assertAlmostEqual(len(self.items) // 2, median2, delta=1)
        assert stdev2 > stdev1