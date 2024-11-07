from unittest import TestCase
import unittest
from HMM import *

class Test(TestCase):
    def test_load(self):
        h = HMM()
        h.load("cat")
        print(h.emissions)
        print(h.transitions)


if __name__ == '__main__':
    unittest.main()

