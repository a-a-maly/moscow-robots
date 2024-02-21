from general import create_level
# 2.1.4
textures = {
    "broken_cell_surface": "cell.png",
}
settings = {
    "max_x": 4,
    "max_y": 4,
    "screen_resolution": (800, 800),
    "start_x": 1,
    "start_y": 0,
    "robot": 0
}
create_level.vertun_level(settings, "level2.json")
