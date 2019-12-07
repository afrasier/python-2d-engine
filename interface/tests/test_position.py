from interface import Position


def test_position_shift():
    p = Position()
    p.shift(1, 1)

    assert p.x == 1
    assert p.y == 1

    p.shift(-2, -1)
    assert p.x == -1
    assert p.y == 0
