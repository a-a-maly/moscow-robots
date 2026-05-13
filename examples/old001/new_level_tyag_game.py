from general import piktomir
#214
game1 = piktomir.Game("new_level_tyag.json")
game1.pull()
game1.rotate_right()
game1.go()

game1.main_loop()
