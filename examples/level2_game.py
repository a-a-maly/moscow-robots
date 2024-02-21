from general import piktomir
#210
game1 = piktomir.Game("level2.json")
game1.go()
game1.rotate_right()
for i in range(2):
    game1.go()
for i in range(4):
    game1.draw()
    game1.go()
    game1.rotate_left()
game1.rotate_right()
game1.rotate_right()
game1.go()
game1.draw()
game1.main_loop()
