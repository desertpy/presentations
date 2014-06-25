import unittest

def my_add(a,b):
    return a + b

class TestMyAdd(unittest.TestCase):
    def test_add1(self):
        assert my_add(3,4), 7