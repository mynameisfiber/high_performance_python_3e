from utility import some_fn

def test_some_fn():
    assert some_fn(2) == 4
    assert some_fn(1) == 1
    assert some_fn(-1) == 1
