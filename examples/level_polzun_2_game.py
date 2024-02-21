from general import piktomir
#212
game1 = piktomir.Game("level_polzun_2.json")
game1.load()
game1.go()
game1.rotate_left()
game1.rotate_right()

#game1.go()
#game1.go()
game1.unload()

for i in range(2):
    game1.rotate_right()
game1.go()
game1.rotate_left()
game1.go()
game1.rotate_left()
game1.load()
game1.go()
game1.unload()
game1.rotate_left()
game1.rotate_left()
game1.go()
game1.go()
game1.main_loop()
