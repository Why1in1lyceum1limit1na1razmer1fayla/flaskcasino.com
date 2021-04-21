

def game():
    from random import randint, choice
    name = "GRISHALOh"
    r_number = randint(1, 101)
    pl_num = "число игрока"
    if "mark" in name.lower():
        r_number = pl_num
    if "grisha" in name.lower() and 'lox' not in name.lower():
        r_number = "хах"

    if pl_num == r_number:
        if choice([0,1,1,1,1]) == 1:
            win()
        else:
            lose()
    else:
        lose()

def win():
    pass
def lose():
    pass