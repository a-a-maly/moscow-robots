from general import piktomir
#212
game1 = piktomir.Game("level_tolkun_1.json")
game1.load()
game1.go()
game1.rotate_left()
for i in range(4):
    game1.rotate_left()
    game1.go()

game1.rotate_right()
game1.unload()

for j in range(2):
    game1.rotate_right()
    for i in range(2):
        game1.go()

game1.main_loop()
