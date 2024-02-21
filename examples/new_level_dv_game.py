from general import piktomir
#214
game1 = piktomir.Game("new_level_dv.json")
game1.rotate_right()
game1.go()
game1.rotate_right()
game1.rotate_right()
for i in range(3):
    game1.go()
game1.rotate_left()
for i in range(2):
    game1.go()
game1.rotate_left()
for i in range(3):
    game1.go()
game1.rotate_left()
game1.go()
game1.main_loop()
