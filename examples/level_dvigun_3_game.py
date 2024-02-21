from general import piktomir
#210
game1 = piktomir.Game("level_dvigun_3.json")


def razvorot():
    for i in range(2):
        game1.rotate_left()


razvorot()


def G():
    game1.go()
    game1.rotate_left()
    game1.go()


def dlin_go(n):
    for i in range(n):
        game1.go()


game1.go()
game1.rotate_left()
game1.go()
game1.rotate_left()
dlin_go(4)
game1.rotate_right()
dlin_go(2)
game1.rotate_right()
game1.go()
razvorot()
dlin_go(2)
game1.rotate_left()
dlin_go(2)


# for i in range(2):
#     game1.rotate_right()
# game1.go()
# game1.rotate_left()
# game1.go()
# game1.rotate_left()
# for i in range(5):
#     game1.go()
# game1.rotate_right()
# game1.rotate_left()
# game1.rotate_left()
# game1.rotate_left()


game1.main_loop()
