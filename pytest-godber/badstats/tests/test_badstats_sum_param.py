import pytest
from badstats import _sum

@pytest.mark.parametrize("input,expected", [
    ((1, 2, 3, 4), 10),
    ((0, 0, 1, 5), 6),
    pytest.mark.xfail(((1.2, -1.0), 0.2)),
])
def test_sum(input, expected):
    assert _sum(input) == expected
