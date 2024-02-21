from general import create_level2
# 2.1.4

settings = {
    "max_x": 4,
    "max_y": 4,
    "screen_resolution": (800, 800),
    "start_x": 1,
    "start_y": 0,
    "angle": 3,
    "robot": 5
}
create_level2.vertun_level(settings, "new_level_train.json")
#create_level2.scepka_level(settings, "new_level_train.json")
