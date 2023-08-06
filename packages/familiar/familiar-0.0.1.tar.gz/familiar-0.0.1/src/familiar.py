def dice_roll(number_of_dice, dice_sides, mod):
    import random
    total = 0
    for i in range(1, number_of_dice + 1):
        total += random.randint(1, dice_sides)
    return total + mod
