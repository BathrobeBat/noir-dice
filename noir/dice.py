import random

def roll_d10():
    return random.randint(1, 10)

def noir_roll(roll_func=roll_d10):
    rolls = [roll_func(), roll_func()]
    original_rolls = rolls.copy()

    tens = rolls.count(10)
    ones = rolls.count(1)

    available_explosions = max(0, tens - ones)

    extra_rolls = []

    for _ in range(available_explosions):
        new_roll = roll_func()
        extra_rolls.append(new_roll)

        while new_roll == 10:
            new_roll = roll_func()
            extra_rolls.append(new_roll)

    total = sum(rolls) + sum(extra_rolls)
    exceptional = (rolls[0] == rolls[1])

    return {
        "grundslag": original_rolls,
        "extra": extra_rolls,
        "tärningssumma": total,
        "exceptionellt": exceptional
    }