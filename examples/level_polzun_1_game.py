from general import piktomir
#212
game1 = piktomir.Game("level_polzun_1.json")
# proideno
# game1.go()
# game1.rotate_right()
#
# game1.go()
# for i in range(2):
#     game1.go()
#     game1.rotate_right()
# game1.go()
# game1.rotate_left()
# game1.go()
#
# game1.rotate_left()
# game1.go()
# game1.go()
# game1.rotate_left()
#
# for i in range(3):
#     game1.go()
# game1.rotate_left()
# for i in range(2):
#     game1.go()

# ne proideno
for i in range(2):
    game1.go()
def pov():
    game1.rotate_right()
    game1.go()
    game1.rotate_right()

def pov2():
    game1.rotate_left()
    game1.go()
    game1.rotate_left()
def GO():
    for i in range(3):
        game1.go()

pov()
GO()
pov2()
GO()
pov()
GO()


# for i in range(2):
#     game1.rotate_left()
#     game1.go()
game1.main_loop()
