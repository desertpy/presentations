import pytest
from badstats import _sum

def test_sum_simple():
    data = (1, 2, 3, 4)
    assert _sum(data) == 10

@pytest.mark.xfail
def test_sum_fails():
    data = (1.2, -1.0)
    assert _sum(data) == 0.2
