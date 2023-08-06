from familiar import dice_roll


def test_dice_roll():
    roll = dice_roll(2, 6, 0)
    print(roll)
    assert roll <= 12
