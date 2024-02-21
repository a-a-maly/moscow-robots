from general import piktomir
#211
game1 = piktomir.Game("level_tyagun_1.json")
def razvorot():
    for i in range(2):
        game1.rotate_left()


razvorot()
game1.pull()
#game1.go()
#game1.pull()

game1.main_loop()
