import pygame
import json
from PIL import Image
import os.path


# 2.1.4

def vertun_level(settings, file_name="", user_textures={}):
    version = 214
    textures = {
        "vertun_surface": "textures/Vertun_2D.png",
        "broken_vertun_surface": "textures/Vertun_2D_obstacle.png",
        "dvigun_surface": "textures/prototype2.png",
        "polzun_surface": "textures/polzun_surface.png",
        "tiagun_surface": "textures/tyagun.png",
        "tolkun_surface": "textures/tolkun_surface.png",
        "train_surface": "textures/train_surface.png",
        "broken_cell_surface": "textures/mapElement_2_2d.png",
        "painted_broken_cell_surface": "textures/mapElement_4_2d.png",
        "painted_cell_surface": "textures/mapElement_3_2d.png",
        "usual_cell_surface": "textures/mapElement_1_2d.png",
        "usual_cell_surface2": "textures/mapElement_5_2d.png",
        "usual_cell_surface3": "textures/mapElement_6_2d.png",
        "_wall_surface": "textures/wall-top_view.png",
        "Iwall_surface": "textures/wall-top_view2.png",
        "end_polzun": "textures/mapElementR.png",
        "end_place": "textures/cross.png",
        "finish_block": 'textures/finish_block.png',
        "finish_block2": 'textures/finish_block2.png',
        "finish_blocku": 'textures/finish_block_u.png',
        "block": "textures/block.png",
        "block2": "textures/block2.png",
        "rblock0": "textures/rblock0.png",
        "rblock1": "textures/rblock1.png",
        "rblock2": "textures/rblock2.png",
        "rblock3": "textures/rblock3.png",
        "rblock4": "textures/rblock4.png",
        "rblock5": "textures/rblock5.png",
        "rblock6": "textures/rblock6.png",
        "rblock7": "textures/rblock7.png",
        "rblock8": "textures/rblock8.png",
        "rblock9": "textures/rblock9.png",
        "mark": "textures/mark.png",
        "base_layer": "textures/base_layer.png",
        "standart_cell_polzun": "textures/mapElement_6_2d.png",
        "division": "textures/division.png",
        "equality": "textures/equality.png",
        "minus": "textures/minus.png",
        "multiply": "textures/multiplication.png",
        "num0": "textures/num0.png",
        "num1": "textures/num1.png",
        "num2": "textures/num2.png",
        "num3": "textures/num3.png",
        "num4": "textures/num4.png",
        "num5": "textures/num5.png",
        "num6": "textures/num6.png",
        "num7": "textures/num7.png",
        "num8": "textures/num8.png",
        "num9": "textures/num9.png",
        "plus": "textures/plus.png"
    }
    if not user_textures == {}:
        for name in textures.keys():
            if name in user_textures.keys():
                textures[name] = user_textures[name]
    pygame.init()
    screen = pygame.display.set_mode(settings["screen_resolution"])

    screen_resolution = [0, 1]
    screen_resolution[0] = settings["screen_resolution"][0] * 0.9
    screen_resolution[1] = settings["screen_resolution"][1] * 0.9

    cell_size = [screen_resolution[0] / settings["max_x"],
                 screen_resolution[1] / settings["max_y"]]
    name_end_place = "end_place"
    if settings["robot"] in [3, 4]:
        name_end_place = "end_polzun"
    end_place_surface = pygame.image.load(textures[name_end_place]).convert_alpha()
    end_place_surface = pygame.transform.scale(end_place_surface, (cell_size[0], cell_size[1]))

    finish_block_surface = pygame.image.load(textures["finish_block"]).convert_alpha()
    finish_block_surface = pygame.transform.scale(finish_block_surface, (cell_size[0], cell_size[1]))

    finish_block2_surface = pygame.image.load(textures["finish_block2"]).convert_alpha()
    finish_block2_surface = pygame.transform.scale(finish_block2_surface, (cell_size[0], cell_size[1]))

    finish_blocku_surface = pygame.image.load(textures["finish_blocku"]).convert_alpha()
    finish_blocku_surface = pygame.transform.scale(finish_blocku_surface, (cell_size[0], cell_size[1]))

    name_usual_cell = textures["usual_cell_surface"]
    if settings["robot"] in [1, 2, 5]:
        name_usual_cell = textures["usual_cell_surface2"]
    if settings["robot"] in [3, 4]:  # polzun tolkun
        name_usual_cell = textures["usual_cell_surface3"]
    usual_cell_surface = pygame.image.load(name_usual_cell).convert()
    usual_cell_surface = pygame.transform.scale(usual_cell_surface,
                                                (cell_size[0], cell_size[1]))
    painted_cell_surface = pygame.image.load(textures["painted_cell_surface"]).convert()
    painted_cell_surface = pygame.transform.scale(painted_cell_surface, (cell_size[0], cell_size[1]))

    broken_cell_surface = pygame.image.load(textures["broken_cell_surface"]).convert()
    broken_cell_surface = pygame.transform.scale(broken_cell_surface, (cell_size[0], cell_size[1]))

    painted_broken_cell_surface = pygame.image.load(textures["painted_broken_cell_surface"]).convert()
    painted_broken_cell_surface = pygame.transform.scale(painted_broken_cell_surface,
                                                         (cell_size[0], cell_size[1]))

    if settings["robot"] in [3, 4]:
        cell_type_surface = [pygame.image.load(textures["standart_cell_polzun"]).convert()]
        for i in range(10):
            name_type_cell = "num" + str(i)
            cell_type_surface.append(pygame.image.load(textures[name_type_cell]).convert())
        cell_type_surface.append(end_place_surface)
        cell_type_surface.append(pygame.image.load(textures["division"]).convert())
        cell_type_surface.append(pygame.image.load(textures["equality"]).convert())
        cell_type_surface.append(pygame.image.load(textures["minus"]).convert())
        cell_type_surface.append(pygame.image.load(textures["multiply"]).convert())
        cell_type_surface.append(pygame.image.load(textures["plus"]).convert())
        for i in range(17):
            cell_type_surface[i] = pygame.transform.scale(cell_type_surface[i],
                                                          (cell_size[0], cell_size[1]))

    _wall_surface = pygame.image.load(textures["_wall_surface"]).convert()
    _wall_surface = pygame.transform.scale(_wall_surface,
                                           (cell_size[0] * 4 / 5, cell_size[1] / 10))
    Iwall_surface = pygame.image.load(textures["Iwall_surface"]).convert()
    Iwall_surface = pygame.transform.scale(Iwall_surface,
                                           (cell_size[0] / 10, cell_size[1] * 4 / 5))

    robots = ["vertun", "dvigun", "tiagun", "polzun", "tolkun", "train"]
    name_robot = robots[settings["robot"]]

    vertun_surface = pygame.image.load(textures[name_robot + "_surface"]).convert_alpha()
    vertun_surface = pygame.transform.scale(vertun_surface,
                                            (min(cell_size) * 0.8, min(cell_size) * 0.8))

    if settings["robot"] in [1, 2, 5]:
        block_surface = pygame.image.load(textures["block"]).convert()
        block_surface = pygame.transform.scale(block_surface, (cell_size[0], cell_size[1]))
        block2_surface = pygame.image.load(textures["block2"]).convert_alpha()
        block2_surface = pygame.transform.scale(block2_surface, (cell_size[0], cell_size[1]))

    blocks_surface = []
    if 3 <= settings["robot"] <= 4:
        for i in range(10):
            name_block = "rblock" + str(i)
            blocks_surface.append(pygame.image.load(textures[name_block]).convert())
            blocks_surface[i] = pygame.transform.scale(blocks_surface[i], (cell_size[0] * 0.4, cell_size[1] * 0.4))

    mark = pygame.image.load(textures["mark"]).convert_alpha()
    mark = pygame.transform.scale(mark, (screen_resolution[1] / 6, screen_resolution[1] / 12))
    screen.blit(mark, (screen_resolution[0] / 100, screen_resolution[1] * (1 + 0.015)))

    base_layer = pygame.image.load(textures["base_layer"]).convert_alpha()
    base_layer = pygame.transform.scale(base_layer, (screen_resolution[1] / 6, screen_resolution[1] / 12))
    # screen.blit(base_layer, (screen_resolution[0] / 100, screen_resolution[1] * (1 + 0.015)))

    pygame.display.flip()
    horizontal_fences = []
    for i in range(settings["max_x"] * (settings["max_y"] + 1)):
        horizontal_fences.append(0)
    vertical_fences = []
    for i in range((settings["max_x"] + 1) * settings["max_y"]):
        vertical_fences.append(0)

    cells = []

    mas_finish = []
    mas_block = []
    for i in range(settings["max_x"] * settings["max_y"]):
        mas_finish.append(0)
        mas_block.append(0)
    strin = ""
    len_str = 0
    for i in range(settings["max_x"] * settings["max_y"]):
        cells.append(
            {
                "broken": False,
                "painted": False,
                "end": 0,
                "blocks": 0,
                "type": 0
            }
        )

    if not file_name == "":
        if os.path.exists(file_name):
            with open(file_name, "r") as json_file:
                initial_data = json.load(json_file)
            if "settings" in initial_data.keys():
                if initial_data["settings"]["max_x"] != settings["max_x"]:
                    print("The max_x in the file is different, it is equal to ", end="")
                    print(initial_data["settings"]["max_x"])
                    return
                if initial_data["settings"]["max_y"] != settings["max_y"]:
                    print("The max_y in the file is different, it is equal to ", end="")
                    print(initial_data["settings"]["max_y"])
                    return
            if "horizontal_fences" in initial_data.keys():
                horizontal_fences = initial_data["horizontal_fences"]
            if "vertical_fences" in initial_data.keys():
                vertical_fences = initial_data["vertical_fences"]
            if "cells" in initial_data.keys():
                cells = initial_data["cells"]
            for i in range(settings["max_x"] * settings["max_y"]):
                if cells[i]["end"] > 0:
                    cells[i]["type"] = 11

        if os.path.exists(file_name.split(".")[0] + "_game.py"):
            with open(file_name.split(".")[0] + "_game.py", "r") as py_file:
                mas = py_file.readlines()
                strin = ''.join(mas)
                len_str = len(mas)
    else:
        file_name = "initial_data.json"

    def rebuild(cells, max_x, max_y, horizontal_fences, vertical_fences, mode):
        pygame.draw.rect(screen, (14, 67, 120),
                         (0, 0, screen_resolution[0] / 0.9, screen_resolution[1] / 0.9))
        if settings["robot"] in [0, 1, 2, 5]:
            for x in range(max_x):
                for y in range(max_y):
                    if not cells[y * max_x + x]["broken"] and not cells[y * max_x + x]["painted"]:
                        screen.blit(usual_cell_surface, (cell_size[0] * x, cell_size[1] * y))
                    elif cells[y * max_x + x]["broken"] and not cells[y * max_x + x]["painted"]:
                        screen.blit(broken_cell_surface, (cell_size[0] * x, cell_size[1] * y))
                    elif cells[y * max_x + x]["broken"] and cells[y * max_x + x]["painted"]:
                        screen.blit(painted_broken_cell_surface, (cell_size[0] * x, cell_size[1] * y))
                    else:
                        screen.blit(painted_cell_surface, (cell_size[0] * x, cell_size[1] * y))

                    if cells[y * max_x + x]["end"] == 1:
                        screen.blit(end_place_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["end"] == 2:
                        screen.blit(finish_block_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["end"] == 3:
                        screen.blit(finish_block2_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["end"] == 4:
                        screen.blit(finish_blocku_surface, (cell_size[0] * x, cell_size[1] * y))

                    if cells[y * max_x + x]["blocks"] == 1:
                        screen.blit(block_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["blocks"] == 2:
                        screen.blit(block2_surface, (cell_size[0] * x, cell_size[1] * y))

            # вертикальные заборы I
            for y in range(settings["max_y"]):
                for x in range(settings["max_x"] + 1):
                    if vertical_fences[y * (settings["max_x"] + 1) + x] == 1:
                        screen.blit(Iwall_surface,
                                    (x * cell_size[0] - cell_size[0] / 20, cell_size[1] * (y + 1 / 10)))
            # горизонтальные заборы _
            for y in range(settings["max_y"] + 1):
                for x in range(settings["max_x"]):
                    if horizontal_fences[y * settings["max_x"] + x] == 1:
                        screen.blit(_wall_surface,
                                    (cell_size[0] * (x + 1 / 10), y * cell_size[1] - cell_size[1] / 20))
        elif settings["robot"] in [3, 4]:
            for y in range(settings["max_y"]):
                for x in range(settings["max_x"]):
                    screen.blit(cell_type_surface[cells[y * max_x + x]["type"]], (cell_size[0] * x, cell_size[1] * y))
                    # if cells[y * max_x + x]["end"] == 1:
                    #     screen.blit(end_place_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["blocks"] != 0:
                        screen.blit(blocks_surface[cells[y * max_x + x]["blocks"] - 1],
                                    (cell_size[0] * (x + 0.3), cell_size[1] * (y + 0.3)))
        # if mode != 0:
        screen.blit(vertun_surface,
                    (cell_size[0] * (0.1 + settings["start_x"]), cell_size[1] * (0.1 + settings["start_y"])))
        if mode == 1:
            screen.blit(mark, (screen_resolution[0] / 100, screen_resolution[1] * (1 + 0.015)))
        if mode == 0:
            screen.blit(base_layer, (screen_resolution[0] / 100, screen_resolution[1] * (1 + 0.015)))
        pygame.display.flip()

    def make_image():
        rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 2)
        pygame.display.update()
        image_name = file_name.split(".")[0] + "_screen.png"
        pil_string_image = pygame.image.tostring(screen, "RGBA", False)
        pil_image = Image.frombytes('RGBA', settings["screen_resolution"], pil_string_image, 'raw')
        pil_image = pil_image.crop((0, 0, screen_resolution[0], screen_resolution[1]))
        pil_image.save(image_name)

    rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 1)

    def is_in_cell(cell_size, local_x, local_y):
        if cell_size[0] / 10 <= local_x <= cell_size[0] * 9 / 10:
            if 0 <= local_y <= cell_size[1] / 20:
                return 3
            if cell_size[1] * 19 / 20 <= local_y <= cell_size[1]:
                return 1
        if cell_size[1] / 10 <= local_y <= cell_size[1] * 9 / 10:
            if 0 <= local_x <= cell_size[0] / 20:
                return 2
            if cell_size[0] * 19 / 20 <= local_x <= cell_size[0]:
                return 0
        else:
            return -1

    flag = 1
    mode = 1

    while flag:
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT:
            make_image()
            pygame.quit()
            flag = 0
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                make_image()
                pygame.quit()
                flag = 0
        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = ev.pos
            if mouse[0] > screen_resolution[0] or mouse[1] > screen_resolution[1]:
                if screen_resolution[1] * (0.01 + 13 / 12) >= mouse[1] >= screen_resolution[1] * (1 + 0.01):
                    if screen_resolution[0] / 100 <= mouse[0] <= screen_resolution[0] / 100 + screen_resolution[1] / 12:
                        mode = 0
                    if screen_resolution[0] / 100 + screen_resolution[1] / 12 <= mouse[0] <= screen_resolution[
                        0] / 100 + screen_resolution[1] / 6:
                        mode = 1
                    if screen_resolution[0] / 100 + screen_resolution[1] / 6 <= mouse[0] <= screen_resolution[
                        0] / 100 + screen_resolution[1] * 3 / 12 and 1 <= settings["robot"] <= 5:
                        mode = 2

            else:
                x = int(mouse[0] // cell_size[0])
                y = int(mouse[1] // cell_size[1])
                loc_x = mouse[0] - cell_size[0] * x
                loc_y = mouse[1] - cell_size[1] * y
                gr = is_in_cell(cell_size, loc_x, loc_y)
                if mouse[0] > screen_resolution[0] or mouse[1] > screen_resolution[1]:
                    continue
                if mode == 1:
                    if gr == 0 and settings["robot"] not in [3, 4]:
                        vertical_fences[y * (settings["max_x"] + 1) + x + 1] = (vertical_fences[y * (
                                settings["max_x"] + 1) + x + 1] + 1) % 2
                    elif gr == 1 and settings["robot"] not in [3, 4]:
                        horizontal_fences[(y + 1) * settings["max_x"] + x] = (horizontal_fences[
                                                                                  (y + 1) * settings[
                                                                                      "max_x"] + x] + 1) % 2
                    elif gr == 2 and settings["robot"] not in [3, 4]:
                        vertical_fences[y * (settings["max_x"] + 1) + x] = (vertical_fences[
                                                                                y * (settings[
                                                                                         "max_x"] + 1) + x] + 1) % 2
                    elif gr == 3 and settings["robot"] not in [3, 4]:
                        horizontal_fences[y * settings["max_x"] + x] = (horizontal_fences[
                                                                            y * settings["max_x"] + x] + 1) % 2
                    else:
                        if settings["robot"] == 0:
                            if not cells[y * settings["max_x"] + x]["broken"] and not cells[y * settings["max_x"] + x][
                                "painted"]:
                                cells[y * settings["max_x"] + x]["broken"] = True
                            elif cells[y * settings["max_x"] + x]["broken"] and not cells[y * settings["max_x"] + x][
                                "painted"]:
                                cells[y * settings["max_x"] + x]["painted"] = True
                            elif cells[y * settings["max_x"] + x]["broken"] and cells[y * settings["max_x"] + x][
                                "painted"]:
                                cells[y * settings["max_x"] + x]["broken"] = False
                            else:
                                cells[y * settings["max_x"] + x]["painted"] = False
                        elif settings["robot"] in [3, 4]:
                            cells[y * settings["max_x"] + x]["type"] = (cells[y * settings["max_x"] + x][
                                                                            "type"] + 1) % 12
                elif mode == 0:
                    i = cells[y * settings["max_x"] + x]["end"]
                    mn = 1
                    if settings["robot"] == 0:
                        mn = 2
                    elif settings["robot"] in [1, 2, 5]:
                        mn = 5
                    cells[y * settings["max_x"] + x]["end"] = (i + 1) % mn

                elif mode == 2:
                    if settings["robot"] in [1, 2, 5]:
                        mmn = 3
                    elif settings["robot"] in [3, 4]:
                        mmn = 11
                    i = cells[y * settings["max_x"] + x]["blocks"]
                    cells[y * settings["max_x"] + x]["blocks"] = (i + 1) % mmn

        if flag != 0:
            mouse = pygame.mouse.get_pos()
            rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode)

    with open(file_name, 'w') as json_file:
        if settings["robot"] in [3, 4]:
            for i in range(settings["max_x"] * settings["max_y"]):
                if cells[i]["type"] == 11:
                    cells[i]["end"] = 1
                else:
                    cells[i]["end"] = 0

        initial_data = {
            "settings": settings,
            "horizontal_fences": horizontal_fences,
            "vertical_fences": vertical_fences,
            "cells": cells
        }

        json.dump(initial_data, json_file, indent=4)

    game_name = file_name.split(".")[0] + "_game.py"

    with open(game_name, 'w') as fp:
        if len_str < 2:
            print("from general import piktomir\n#", file=fp, end="")
            print(version, file=fp)
            print('game1 = piktomir.Game("', file=fp, end="")
            print(file_name, file=fp, end="")
            print('")\n\n\ngame1.main_loop()', file=fp)
        else:
            fp.write(strin)
