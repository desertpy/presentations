import pytest
import badstats

@pytest.fixture
def data():
    return (1.0, 2.0, 3.0, 4.0)

def test_sum_simple(data):
    assert badstats._sum(data) == 10.0

def test_mean_simple(data):
    assert badstats.mean(data) == 2.5
