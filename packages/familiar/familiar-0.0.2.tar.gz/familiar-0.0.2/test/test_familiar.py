from familiar import dice_roll, get_modifier


def test_dice_roll():
    roll = dice_roll(2, 6, 0)
    print(roll)
    assert roll <= 12


def test_get_modifier():
    mod = get_modifier(12)
    assert mod == 1


def test_get_modifier_big_int():
    mod = get_modifier(18)
    assert mod == 4


def test_negative_get_modifier():
    mod = get_modifier(8)
    assert mod == -1


def test_negative_get_modifier_on_big_int():
    mod = get_modifier(4)
    assert mod == -3
