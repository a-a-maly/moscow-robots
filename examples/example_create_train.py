from general import create_level
# 2.1.4
settings = {
    "max_x": 6,
    "max_y": 4,
    "screen_resolution": (600, 400),
    "start_x": 1,
    "start_y": 0,
    "robot": 5
}
create_level.vertun_level(settings, "level_train.json")
