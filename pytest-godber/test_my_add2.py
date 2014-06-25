def my_add(a,b):
    """ Sample doctest
    >>> my_add(3,4)
    7
    """
    return a + b

def test_my_add():
    assert my_add(2,3) == 5