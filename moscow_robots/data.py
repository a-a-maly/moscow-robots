import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

texture_names = [
    "block_any_dest",
    "block_circle_dest",
    "block_circle",
    "block_square_dest",
    "block_square",
    "dvigun",
    "dvigun_dead",
    "field_broken_painted",
    "field_broken",
    "field_normal_other",
    "field_normal_painted",
    "field_normal",
    "menu_base_layer",
    "menu_mark",
    "msg_instruction",
    "msg_lose",
    "msg_win",
    "polzun_empty",
    "polzun_loaded",
    "polzun_empty_dead",
    "polzun_loaded_dead",
    "rblock0",
    "rblock1",
    "rblock2",
    "rblock3",
    "rblock4",
    "rblock5",
    "rblock6",
    "rblock7",
    "rblock8",
    "rblock9",
    "rblock",
    "robot_dest",
    "rug_div",
    "rug_eq",
    "rug_green",
    "rug_minus",
    "rug_mul",
    "rug_num0",
    "rug_num1",
    "rug_num2",
    "rug_num3",
    "rug_num4",
    "rug_num5",
    "rug_num6",
    "rug_num7",
    "rug_num8",
    "rug_num9",
    "rug_plus",
    "rug_red",
    "scepka",
    "tolkun_empty_dead",
    "tolkun_empty",
    "tolkun_loaded_dead",
    "tolkun_loaded",
    "tool_bar1",
    "tool_bar2d",
    "tool_bar2",
    "tool_bar3d",
    "tool_bar3",
    "tool_bar4d",
    "tool_bar4",
    "tool_bar5d",
    "tool_bar5",
    "tool_bar6d",
    "tool_bar6",
    "train_dead",
    "train",
    "tyagun",
    "tyagun_dead",
    "vertun",
    "vertun_dead",
    "iskun",
    "iskun_dead",
    "wall_hor",
    "wall_vert"
]

texture_imgs = None

def preload_textures():
	global texture_imgs
	if texture_imgs is not None:
		return

	data_path = os.path.join(os.path.dirname(__file__), 'textures')
	texture_imgs = {}
	for name in texture_names:
		image = pygame.image.load(os.path.join(data_path, name + ".png"))
		texture_imgs[name] = image

def get_image(name):
	preload_textures()
	return texture_imgs[name]

preload_textures()

