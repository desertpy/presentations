import pytest
import sys
from badstats import _sum
xfail = pytest.mark.xfail

def test_sum_simple():
    data = (1, 2, 3, 4)
    assert _sum(data) == 10

@xfail(sys.platform == 'linux2', reason='requires windows')
def test_sum_fails():
    data = (1.2, -1.0)
    assert _sum(data) == 0.2
