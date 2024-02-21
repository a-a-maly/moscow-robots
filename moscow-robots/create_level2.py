import pygame
from general import function_robots as fr
import json
from PIL import Image
import os.path
import math


def vertun_level(settings, file_name="", user_textures={}):
    version = 214
    # 0 вертун 1 двигун 2 тягун 3 ползун 4 толкун 5 поезд
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
        "plus": "textures/plus.png",
        "num_tool_bar1": "textures/tool_bar1.png",
        "num_tool_bar2": "textures/tool_bar2.png",
        "num_tool_bar3": "textures/tool_bar3.png",
        "num_tool_bar4": "textures/tool_bar4.png",
        "num_tool_bar5": "textures/tool_bar5.png",
        "num_tool_bar6": "textures/tool_bar6.png",
        "num_tool_bar2d": "textures/tool_bar2d.png",
        "num_tool_bar3d": "textures/tool_bar3d.png",
        "num_tool_bar4d": "textures/tool_bar4d.png",
        "num_tool_bar5d": "textures/tool_bar5d.png",
        "num_tool_bar6d": "textures/tool_bar6d.png",
        "scepka": "textures/scepka.png",
    }
    if not user_textures == {}:
        for name in textures.keys():
            if name in user_textures.keys():
                textures[name] = user_textures[name]
    pygame.init()
    robot_pos = [settings["start_x"], settings["start_y"]]
    cell_size = [settings["screen_resolution"][0] / settings["max_x"],
                 settings["screen_resolution"][1] / settings["max_y"]]
    razmer_y = max(settings["screen_resolution"][1], 6 * cell_size[1]/2)
    screen_resolution = [math.ceil(settings["screen_resolution"][0]+cell_size[0]), math.ceil(razmer_y)]
    screen = pygame.display.set_mode(screen_resolution)
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

    if settings["robot"] == 5:
        scepka_surface = pygame.image.load(textures["scepka"]).convert()
        scepka_surface = pygame.transform.scale(scepka_surface,
                                                (cell_size[0] * 0.6, cell_size[1] * 0.2))
        scepka1_surface = pygame.transform.rotate(scepka_surface, 90)

    if settings["robot"] in [3, 4]:
        cell_type_surface = [pygame.image.load(textures["standart_cell_polzun"]).convert_alpha()]
        for i in range(10):
            name_type_cell = "num" + str(i)
            cell_type_surface.append(pygame.image.load(textures[name_type_cell]).convert_alpha())
            cell_type_surface[i] = pygame.transform.scale(cell_type_surface[i],
                                                          (cell_size[0], cell_size[1]))
        cell_type_surface.append(end_place_surface)
    else:
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
        block_surface = pygame.transform.scale(block_surface, (cell_size[0]*0.8, cell_size[1]*0.8))
        block2_surface = pygame.image.load(textures["block2"]).convert_alpha()
        block2_surface = pygame.transform.scale(block2_surface, (cell_size[0]*0.8, cell_size[1]*0.8))
    elif settings["robot"] in [3, 4]:
        blocks_surface = []
        for i in range(10):
            name_block = "rblock" + str(i)
            blocks_surface.append(pygame.image.load(textures[name_block]).convert())
            blocks_surface[i] = pygame.transform.scale(blocks_surface[i], (cell_size[0] * 0.4, cell_size[1] * 0.4))

    tool_bar_surface = []
    d_tool_bar_surface = [0]
    for i in range(6):
        name_tool_bar = "num_tool_bar" + str(i+1)
        tool_bar_surface.append(pygame.image.load(textures[name_tool_bar]).convert_alpha())
        tool_bar_surface[i] = pygame.transform.scale(tool_bar_surface[i], (cell_size[0], cell_size[0] * 0.5))
        if i > 0:
            name_tool_bar = name_tool_bar + "d"
            d_tool_bar_surface.append(pygame.image.load(textures[name_tool_bar]).convert_alpha())
            d_tool_bar_surface[i] = pygame.transform.scale(d_tool_bar_surface[i], (cell_size[0], cell_size[0] * 0.5))

    pygame.display.flip()

    horizontal_fences = []
    for i in range(settings["max_x"] * (settings["max_y"] + 1)):
        horizontal_fences.append(0)
    vertical_fences = []
    for i in range((settings["max_x"] + 1) * settings["max_y"]):
        vertical_fences.append(0)

    cells = []
    for i in range(settings["max_x"] * settings["max_y"]):
        cells.append(
            {
                "pos": i,
                "blocks": 0,
                "sticker": 0,
                "type_cell": 0
            }
        )
    angle = settings["angle"]
    len_str = 0
    mas_trains = []
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
                robot_pos = [initial_data["settings"]["start_x"], initial_data["settings"]["start_y"]]
            if "horizontal_fences" in initial_data.keys():
                horizontal_fences = initial_data["horizontal_fences"]
            if "vertical_fences" in initial_data.keys():
                vertical_fences = initial_data["vertical_fences"]
            if "cells" in initial_data.keys():
                cells = initial_data["cells"]
            for i in range(settings["max_x"] * settings["max_y"]):
                if cells[i]["sticker"] > 0 and name_robot in ["polzun", "tolkun"]:
                    cells[i]["type_cell"] = 11
            print(angle)
            if "angle" in initial_data["settings"].keys():
                angle = initial_data["settings"]["angle"]
            print(angle)
            if "mas_trains" in initial_data.keys():
                mas_trains = initial_data["mas_trains"]


        if os.path.exists(file_name.split(".")[0] + "_game.py"):
            with open(file_name.split(".")[0] + "_game.py", "r") as py_file:
                mas = py_file.readlines()
                strin = ''.join(mas)
                len_str = len(mas)
    else:
        file_name = "initial_data.json"

    def sostav_neglav_with(pos, mas_trains):
        for i in range(len(mas_trains)):
            for j in range(len(mas_trains[i]["mas_elem"])):
                if mas_trains[i]["mas_elem"][j]["pos"] == pos:
                    return i
        return -2  # не нашли составов с pos\

    def make_trains(mas_trains, cells):
        for x in range(settings["max_x"]):
            for y in range(settings["max_y"]):
                pos = x + y * settings["max_x"]
                if cells[pos]["blocks"] != 0 and sostav_neglav_with(pos, mas_trains) == -2:
                    mas_trains.append(
                        {
                            "type": "passive",
                            "mas_elem": [
                                {
                                    "type": cells[pos]["blocks"],
                                    "pos": pos
                                }
                            ]
                        }
                    )
                cells[pos]["blocks"] = 0
        if sostav_neglav_with(robot_pos[0]+settings["max_x"]*robot_pos[1], mas_trains) == -2:
            mas_trains.append(
                {
                    "type": "active",
                    "mas_elem": [
                        {
                            "type": 0,
                            "pos": robot_pos[0]+settings["max_x"]*robot_pos[1]
                        }
                    ]
                }
            )

    def blocks_from_sostavs(mas_trains):
        for i in range(len(mas_trains)):
            for j in range(len(mas_trains[i]["mas_elem"])):
                if mas_trains[i]["mas_elem"][j]["type"] != 0:
                    cells[mas_trains[i]["mas_elem"][j]["pos"]]["blocks"] = mas_trains[i]["mas_elem"][j]["type"]

    make_trains(mas_trains, cells)
    vertun_surface = pygame.transform.rotate(vertun_surface, -90*angle)

    def make_fences(max_x, max_y):
        # вертикальные заборы I
        for y in range(max_y):
            for x in range(max_x + 1):
                # if x == 0 or x == self.count_of_cells[0]:
                #     self.vertical_fences[y * (self.count_of_cells[0] + 1) + x] = 1
                if vertical_fences[y * (max_x + 1) + x] == 1:
                    screen.blit(Iwall_surface,
                                (x * max_x - max_x / 20, max_y * (y + 1 / 10)))

        # горизонтальные заборы _
        for y in range(max_y + 1):
            for x in range(max_x):
                # if y == 0 or y == self.count_of_cells[0]:
                #     self.horizontal_fences[y * self.count_of_cells[0] + x] = 1
                if horizontal_fences[y * max_x + x] == 1:
                    screen.blit(_wall_surface,
                                (max_x * (x + 1 / 10), y * max_y - max_y / 20))

    def blit(change_x, change_y, surface, pos, max_x):
        x = pos % max_x
        y = int(pos / max_x)
        screen.blit(surface, (
            cell_size[0] * (x + change_x),
            cell_size[1] * (y + change_y)))

    def pos_to_coor(pos, max_x):
        return pos % max_x, int(pos / max_x)

    def display_scepka(max_x, old_pos, pos, sdvig=None):
        if sdvig is None:
            sdvig = [0, 0]
        if pos - old_pos in [-1, 1]:
            if pos - old_pos == 1:
                x, y = pos_to_coor(old_pos, max_x)
            else:
                x, y = pos_to_coor(pos, max_x)
            screen.blit(scepka_surface, (
                cell_size[0] * (x + sdvig[0] * 0.5 + 0.7),
                cell_size[1] * (y + sdvig[1] * 0.5 + 0.4)))
        if pos - old_pos in [max_x, -max_x]:
            if pos - old_pos == max_x:
                x, y = pos_to_coor(old_pos, max_x)
            else:
                x, y = pos_to_coor(pos, max_x)
            screen.blit(scepka1_surface, (
                cell_size[0] * (x + sdvig[0] * 0.5 + 0.4),
                cell_size[1] * (y + sdvig[1] * 0.5 + 0.7)))

    def display_train(elems, max_x):
        if elems["type"] == "active":
            elem = elems["mas_elem"][0]
            old_pos = elem["pos"]
            blit(0.1, 0.1, vertun_surface, old_pos, max_x)
        else:
            old_pos = elems["mas_elem"][0]["pos"]
            if elems["mas_elem"][0]["type"] == 1:
                surface = block_surface
            else:
                surface = block2_surface
            blit(0.1, 0.1, surface, old_pos, max_x)
        i = 0
        for elem in elems["mas_elem"]:
            i += 1
            if elems["type"] == "passive" and i == 1:
                continue
            pos = elem["pos"]
            x, y = pos_to_coor(pos, max_x)
            if elem["type"] == 1:
                screen.blit(block_surface, ((0.1 + x) * cell_size[0], (0.1 + y) * cell_size[1]))
            elif elem["type"] == 2:
                screen.blit(block2_surface, ((0.1 + x) * cell_size[0], (0.1 + y) * cell_size[1]))
            display_scepka(max_x, old_pos, pos)
            old_pos = pos
        pygame.display.flip()

    def blit_sostavs(cells, max_x, max_y, horizontal_fences, vertical_fences, mode, mas_trains):
        for x in range(max_x):
            for y in range(max_y):
                rebuild(cells, max_x, max_y, horizontal_fences, vertical_fences, mode)
        # print(mas_trains)
        for elems in mas_trains:
            # print(elems)
            display_train(elems, max_x)
        make_fences(max_x, max_y)

    def rebuild(cells, max_x, max_y, horizontal_fences, vertical_fences, mode):
        pygame.draw.rect(screen, (14, 67, 120),
                         (0, 0, screen_resolution[0], screen_resolution[1]))
        if settings["robot"] in [0, 1, 2, 5]:
            for x in range(max_x):
                for y in range(max_y):
                    if cells[y * max_x + x]["type_cell"] == 0:
                        screen.blit(usual_cell_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["type_cell"] == 1:
                        screen.blit(broken_cell_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["type_cell"] == 2:
                        screen.blit(painted_broken_cell_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["type_cell"] == 3:
                        screen.blit(painted_cell_surface, (cell_size[0] * x, cell_size[1] * y))

                    if cells[y * max_x + x]["sticker"] == 1:
                        screen.blit(end_place_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["sticker"] == 2:
                        screen.blit(finish_block_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["sticker"] == 3:
                        screen.blit(finish_block2_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["sticker"] == 4:
                        screen.blit(finish_blocku_surface, (cell_size[0] * x, cell_size[1] * y))

                    if cells[y * max_x + x]["blocks"] == 1:
                        screen.blit(block_surface, (cell_size[0] * (x+0.1), cell_size[1] * (y+0.1)))
                    if cells[y * max_x + x]["blocks"] == 2:
                        screen.blit(block2_surface, (cell_size[0] * (x+0.1), cell_size[1] * (y+0.1)))

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
                    screen.blit(cell_type_surface[cells[y * max_x + x]["type_cell"]], (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["blocks"] != 0:
                        screen.blit(blocks_surface[cells[y * max_x + x]["blocks"] - 1],
                                    (cell_size[0] * (x + 0.3), cell_size[1] * (y + 0.3)))
        # if mode != 0:
        screen.blit(vertun_surface,
                    (cell_size[0] * (0.1 + robot_pos[0]), cell_size[1] * (0.1 + robot_pos[1])))
        for i in range(6):
            #print(d_tool_bar_surface)
            #print(mode, i)
            if mode != i and i !=0:
                screen.blit(d_tool_bar_surface[i], (screen_resolution[0] - cell_size[0], cell_size[1]/2*i))
            else:
                screen.blit(tool_bar_surface[i], (screen_resolution[0] - cell_size[0], cell_size[1]/2*i))
        pygame.display.flip()

    mode = 1 # 1 2 3 4
    def make_image():
        rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 2)
        if settings["robot"] == 5:
            blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 1, mas_trains)
        pygame.display.update()
        image_name = file_name.split(".")[0] + "_screen.png"
        pil_string_image = pygame.image.tostring(screen, "RGBA", False)
        pil_image = Image.frombytes('RGBA', screen_resolution, pil_string_image, 'raw')
        pil_image = pil_image.crop((0, 0, settings["screen_resolution"][0], settings["screen_resolution"][1]))
        pil_image.save(image_name)

    # def make_image():
    #     rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 2)
    #     pygame.display.update()
    #     image_name = file_name.split(".")[0] + "_screen.png"
    #     pil_string_image = pygame.image.tostring(screen, "RGBA", False)
    #     pil_image = Image.frombytes('RGBA', settings["screen_resolution"], pil_string_image, 'raw')
    #     pil_image = pil_image.crop((0, 0, screen_resolution[0], screen_resolution[1]))
    #     pil_image.save(image_name)

    rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 1)
    if settings["robot"] == 5:
        blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 1, mas_trains)

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
    perenos = 0
    nazh = 0
    mode = 1
    rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode)
    if settings["robot"] == 5:
        blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode, mas_trains)

    def index_in_train(train, pos):
        i = 0
        for elem in train:
            #print(elem)
            if elem["pos"] == pos:
                return i
            i += 1
        return -2

    while flag:
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT:
            nazh = 1
            make_image()
            pygame.quit()
            flag = 0
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                nazh = 1
                make_image()
                pygame.quit()
                flag = 0
        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
            nazh = 1
            perenos = 0
            vertun_surface.set_alpha(255)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mouse = ev.pos
            nazh = 1
            #print(mouse[0], screen_resolution[0], cell_size[0])
            if mouse[0] > screen_resolution[0] - cell_size[0] and perenos != 1:
                if cell_size[1]/2 * 2 >= mouse[1] >= cell_size[1]/2 * 1:
                    mode = 1
                if cell_size[1] / 2 * 3 >= mouse[1] >= cell_size[1] / 2 * 2:
                    mode = 2
                if cell_size[1]/2 * 4 >= mouse[1] >= cell_size[1]/2 * 3:
                    mode = 3
                if cell_size[1] / 2 * 5 >= mouse[1] >= cell_size[1] / 2 * 4:
                    mode = 4
                if cell_size[1] / 2 * 6 >= mouse[1] >= cell_size[1] / 2 * 5 and settings["robot"] == 5:
                    mode = 5
                print(mode)
            else:
                x = int(mouse[0] // cell_size[0])
                y = int(mouse[1] // cell_size[1])
                loc_x = mouse[0] - cell_size[0] * x
                loc_y = mouse[1] - cell_size[1] * y
                gr = is_in_cell(cell_size, loc_x, loc_y)

                nazh = 1
                if mode == 1:
                    mmn = 1
                    if settings["robot"] in [1, 2, 5]:
                        mmn = 3
                    elif settings["robot"] in [3, 4]:
                        mmn = 11
                    if robot_pos != [x,y]:
                        if settings["robot"] != 5:
                            i = cells[y * settings["max_x"] + x]["blocks"]
                            cells[y * settings["max_x"] + x]["blocks"] = (i + 1) % mmn
                        else:
                            pos = y * settings["max_x"] + x
                            num_s1 = sostav_neglav_with(pos, mas_trains)
                            if num_s1 != -2:
                                ind1 = index_in_train(mas_trains[num_s1]["mas_elem"], pos)
                                if mas_trains[num_s1]["mas_elem"][ind1]["type"]==1:
                                    mas_trains[num_s1]["mas_elem"][ind1]["type"]=2
                                    continue
                                len1 = len(mas_trains[num_s1]["mas_elem"])
                                if len1 == 1:
                                    mas_trains.pop(num_s1)
                                else:
                                    mas1 = mas_trains[num_s1]["mas_elem"][:ind1]
                                    mas2 = mas_trains[num_s1]["mas_elem"][ind1+1:]
                                    mas_trains.pop(num_s1)
                                    if len(mas1) != 0:
                                        type_tr1 = "passive"
                                        if mas1[0]["type"]==0:
                                            type_tr1 = "active"
                                        mas_trains.append({
                                            "type": type_tr1,
                                            "mas_elem": mas1
                                        })
                                    if len(mas2) != 0:
                                        type_tr2 = "passive"
                                        if mas2[-1]["type"]==0:
                                            type_tr2 = "active"
                                        mas_trains.append({
                                            "type": type_tr2,
                                            "mas_elem": mas2
                                        })
                            else:
                                mas_trains.append({
                                    "type": "passive",
                                    "mas_elem": [{"type":1, "pos": pos}]
                                })
                if mode == 2:
                    i = cells[y * settings["max_x"] + x]["sticker"]
                    mn = 1
                    if settings["robot"] == 0:
                        mn = 2
                    elif settings["robot"] in [1, 2, 5]:
                        mn = 5
                    cells[y * settings["max_x"] + x]["sticker"] = (i + 1) % mn
                if mode == 3:
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
                            cells[y * settings["max_x"] + x]["type_cell"] = (cells[y * settings["max_x"] + x]["type_cell"] + 1) % 4
                        elif settings["robot"] in [3, 4]:
                            cells[y * settings["max_x"] + x]["type_cell"] = (cells[y * settings["max_x"] + x]["type_cell"] + 1) % 12
                if mode == 4:
                    if perenos == 0 and robot_pos == [x,y]:

                        if settings["robot"] == 5:
                            pos = y * settings["max_x"] + x
                            num_s1 = sostav_neglav_with(pos, mas_trains)
                            if num_s1 != -2:
                                ind1 = index_in_train(mas_trains[num_s1]["mas_elem"], pos)
                                len1 = len(mas_trains[num_s1]["mas_elem"])
                                if len1 != 1:
                                    mas1 = mas_trains[num_s1]["mas_elem"][ind1+1:]
                                    mas_trains[num_s1]["mas_elem"] = mas_trains[num_s1]["mas_elem"][:ind1+1]

                                    mas_trains.append({
                                        "type": "passive",
                                        "mas_elem": mas1
                                    })

                        perenos = 1
                        vertun_surface.set_alpha(100)
                    elif perenos == 1:
                        perenos = 0
                        if robot_pos == [x,y]:
                            angle = (angle + 1) % 4  # 0 -> 0, 1 -> 90 вниз, 2 -> 180, 3 -> 270
                            vertun_surface = pygame.transform.rotate(vertun_surface, -90)
                        if settings["robot"] == 5:
                            pos = robot_pos[1] * settings["max_x"] + robot_pos[0]
                            num_s1 = sostav_neglav_with(pos, mas_trains)
                            ind1 = index_in_train(mas_trains[num_s1]["mas_elem"], pos)
                            mas_trains[num_s1]["mas_elem"][ind1]["pos"] = y * settings["max_x"] + x
                        robot_pos = [x, y]

                        vertun_surface.set_alpha(255)
                if mode == 5 and settings["robot"] == 5:
                    print("ererw34324r")
                    pos = y * settings["max_x"] + x
                    if gr == 0 and vertical_fences[y * (settings["max_x"] + 1) + x + 1] != 1:
                        new_pos = pos + 1
                    elif gr == 1 and horizontal_fences[(y + 1) * settings["max_x"] + x] != 1:
                        new_pos = pos + settings["max_x"]
                    elif gr == 2 and vertical_fences[y * (settings["max_x"] + 1) + x] != 1:
                        new_pos = pos - 1
                    elif gr == 3 and horizontal_fences[y * settings["max_x"] + x] != 1:
                        new_pos = pos - settings["max_x"]
                    else:
                        continue
                    num_s1 = sostav_neglav_with(pos, mas_trains)
                    num_s2 = sostav_neglav_with(new_pos, mas_trains)
                    if num_s2 != -2 and num_s1 != -2:
                        ind1 = index_in_train(mas_trains[num_s1]["mas_elem"], pos)
                        len1 = len(mas_trains[num_s1]["mas_elem"])
                        ind2 = index_in_train(mas_trains[num_s2]["mas_elem"], new_pos)
                        len2 = len(mas_trains[num_s2]["mas_elem"])

                        print("sostav")
                        print(num_s2, num_s1)
                        if num_s1 == num_s2:
                            print("ind")
                            print(ind1, ind2)
                            if ind2 == ind1 - 1 or ind1 == ind2 - 1:
                                if ind2 == ind1 - 1:
                                    ind1, ind2 = ind2, ind1
                                mas1 = mas_trains[num_s2]["mas_elem"][:ind2]
                                mas2 = mas_trains[num_s2]["mas_elem"][ind2:]
                                type_tr1 = "passive"
                                type_tr2 = "passive"
                                if mas1[0]["type"] == 0:
                                    type_tr1 = "active"
                                if mas2[-1]["type"] == 0:
                                    type_tr1 = "active"
                                mas_trains[num_s1] = {
                                    "type": type_tr1,
                                    "mas_elem": mas1
                                }
                                mas_trains.append({
                                    "type": type_tr2,
                                    "mas_elem": mas2
                                })
                            else:
                                continue

                        elif (ind1 == 0 or ind1 == len1 - 1) and (ind2 == 0 or ind2 == len2 - 1):
                            if mas_trains[num_s2]["mas_elem"][ind2]["type"] == 0 and len2 != 1:
                                continue
                            if mas_trains[num_s1]["mas_elem"][ind1]["type"] == 0 and len1 != 1:
                                continue
                            mas1 = mas_trains[num_s1]["mas_elem"]
                            mas2 = mas_trains[num_s2]["mas_elem"]
                            if ind1 != 0:
                                mas1 = list(reversed(mas_trains[num_s1]["mas_elem"]))
                            if ind2 != len2 - 1:
                                mas2 = list(reversed(mas_trains[num_s2]["mas_elem"]))
                            mas1 = mas2 + mas1
                            type_tr = "passive"
                            if mas_trains[num_s2]["type"] == "active" or mas_trains[num_s1]["type"] == "active":
                                type_tr = "active"
                            mas_trains[num_s1] = {
                                "type": type_tr,
                                "mas_elem": mas1
                            }
                            if type_tr == "active" and mas1[0]["type"] != 0:
                                mas_trains[num_s1]["mas_elem"] = list(reversed(mas1))
                            mas_trains.pop(num_s2)





        if flag != 0 and nazh == 1:
            mouse = pygame.mouse.get_pos()
            rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode)
            if settings["robot"] == 5:
                blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode, mas_trains)
            nazh = 0

    settings["start_x"] = robot_pos[0]
    settings["start_y"] = robot_pos[1]
    settings["angle"] = angle
    print(settings)

    with open(file_name, 'w') as json_file:
        if settings["robot"] in [3, 4]:
            for i in range(settings["max_x"] * settings["max_y"]):
                if cells[i]["type_cell"] == 11:
                    cells[i]["sticker"] = 1
                else:
                    cells[i]["sticker"] = 0

        initial_data = {
            "settings": settings,
            "horizontal_fences": horizontal_fences,
            "vertical_fences": vertical_fences,
            "cells": cells,
            "mas_trains": mas_trains
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


def scepka_level(settings, file_name="", user_textures={}):
    if settings["robot"] != 5:
        return
    textures = {
        "broken_vertun_surface": "textures/Vertun_2D_obstacle.png",
        "train_surface": "textures/train_surface.png",
        "usual_cell_surface2": "textures/mapElement_5_2d.png",
        "_wall_surface": "textures/wall-top_view.png",
        "Iwall_surface": "textures/wall-top_view2.png",
        "end_place": "textures/cross.png",
        "finish_block": 'textures/finish_block.png',
        "finish_block2": 'textures/finish_block2.png',
        "finish_blocku": 'textures/finish_block_u.png',
        "block": "textures/block.png",
        "scepka": "textures/scepka.png",
        "block2": "textures/block2.png"
    }
    if not user_textures == {}:
        for name in textures.keys():
            if name in user_textures.keys():
                textures[name] = user_textures[name]
    pygame.init()
    robot_pos = [settings["start_x"], settings["start_y"]]
    cell_size = [settings["screen_resolution"][0] / settings["max_x"],
                 settings["screen_resolution"][1] / settings["max_y"]]
    screen_resolution = settings["screen_resolution"]
    screen = pygame.display.set_mode(screen_resolution)
    name_end_place = "end_place"
    end_place_surface = pygame.image.load(textures[name_end_place]).convert_alpha()
    end_place_surface = pygame.transform.scale(end_place_surface, (cell_size[0], cell_size[1]))

    finish_block_surface = pygame.image.load(textures["finish_block"]).convert_alpha()
    finish_block_surface = pygame.transform.scale(finish_block_surface, (cell_size[0], cell_size[1]))

    finish_block2_surface = pygame.image.load(textures["finish_block2"]).convert_alpha()
    finish_block2_surface = pygame.transform.scale(finish_block2_surface, (cell_size[0], cell_size[1]))

    finish_blocku_surface = pygame.image.load(textures["finish_blocku"]).convert_alpha()
    finish_blocku_surface = pygame.transform.scale(finish_blocku_surface, (cell_size[0], cell_size[1]))

    name_usual_cell = textures["usual_cell_surface2"]
    usual_cell_surface = pygame.image.load(name_usual_cell).convert()
    usual_cell_surface = pygame.transform.scale(usual_cell_surface,
                                                (cell_size[0], cell_size[1]))

    scepka_surface = pygame.image.load(textures["scepka"]).convert()
    scepka_surface = pygame.transform.scale(scepka_surface,
                                            (cell_size[0] * 0.6, cell_size[1] * 0.2))
    scepka1_surface = pygame.transform.rotate(scepka_surface, 90)

    _wall_surface = pygame.image.load(textures["_wall_surface"]).convert()
    _wall_surface = pygame.transform.scale(_wall_surface,
                                           (cell_size[0] * 4 / 5, cell_size[1] / 10))
    Iwall_surface = pygame.image.load(textures["Iwall_surface"]).convert()
    Iwall_surface = pygame.transform.scale(Iwall_surface,
                                           (cell_size[0] / 10, cell_size[1] * 4 / 5))

    vertun_surface = pygame.image.load(textures["train_surface"]).convert_alpha()
    vertun_surface = pygame.transform.scale(vertun_surface,
                                            (min(cell_size) * 0.8, min(cell_size) * 0.8))

    block_surface = pygame.image.load(textures["block"]).convert()
    block_surface = pygame.transform.scale(block_surface, (cell_size[0] * 0.8, cell_size[1] * 0.8))
    block2_surface = pygame.image.load(textures["block2"]).convert_alpha()
    block2_surface = pygame.transform.scale(block2_surface, (cell_size[0] * 0.8, cell_size[1] * 0.8))
    pygame.display.flip()

    horizontal_fences = []
    for i in range(settings["max_x"] * (settings["max_y"] + 1)):
        horizontal_fences.append(0)
    vertical_fences = []
    for i in range((settings["max_x"] + 1) * settings["max_y"]):
        vertical_fences.append(0)

    cells = []
    mas_trains = []
    for i in range(settings["max_x"] * settings["max_y"]):
        cells.append(
            {
                "pos": i,
                "blocks": 0,
                "sticker": 0,
                "type_cell": 0
            }
        )
    angle = settings["angle"]
    len_str = 0
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
                robot_pos = [initial_data["settings"]["start_x"], initial_data["settings"]["start_y"]]
            if "horizontal_fences" in initial_data.keys():
                horizontal_fences = initial_data["horizontal_fences"]
            if "vertical_fences" in initial_data.keys():
                vertical_fences = initial_data["vertical_fences"]
            if "cells" in initial_data.keys():
                cells = initial_data["cells"]
            if "mas_trains" in initial_data.keys():
                mas_trains = initial_data["mas_trains"]

            print(angle)
            if "angle" in initial_data["settings"].keys():
                angle = initial_data["settings"]["angle"]
            print(angle)

        if os.path.exists(file_name.split(".")[0] + "_game.py"):
            with open(file_name.split(".")[0] + "_game.py", "r") as py_file:
                mas = py_file.readlines()
                strin = ''.join(mas)
                len_str = len(mas)
    else:
        return

    vertun_surface = pygame.transform.rotate(vertun_surface, -90 * angle)


    def make_fences(max_x, max_y):
        # вертикальные заборы I
        for y in range(max_y):
            for x in range(max_x + 1):
                # if x == 0 or x == self.count_of_cells[0]:
                #     self.vertical_fences[y * (self.count_of_cells[0] + 1) + x] = 1
                if vertical_fences[y * (max_x + 1) + x] == 1:
                    screen.blit(Iwall_surface,
                                (x * max_x - max_x / 20, max_y * (y + 1 / 10)))

        # горизонтальные заборы _
        for y in range(max_y + 1):
            for x in range(max_x):
                # if y == 0 or y == self.count_of_cells[0]:
                #     self.horizontal_fences[y * self.count_of_cells[0] + x] = 1
                if horizontal_fences[y * max_x + x] == 1:
                    screen.blit(_wall_surface,
                                (max_x * (x + 1 / 10), y * max_y - max_y / 20))

    def blit(change_x, change_y, surface, pos, max_x):
        x = pos % max_x
        y = int(pos / max_x)
        screen.blit(surface, (
            cell_size[0] * (x + change_x),
            cell_size[1] * (y + change_y)))

    def pos_to_coor(pos, max_x):
        return pos % max_x, int(pos / max_x)

    def display_scepka(max_x, old_pos, pos, sdvig=None):
        if sdvig is None:
            sdvig = [0, 0]
        if pos - old_pos in [-1, 1]:
            if pos - old_pos == 1:
                x, y = pos_to_coor(old_pos, max_x)
            else:
                x, y = pos_to_coor(pos, max_x)
            screen.blit(scepka_surface, (
                cell_size[0] * (x + sdvig[0] * 0.5 + 0.7),
                cell_size[1] * (y + sdvig[1] * 0.5 + 0.4)))
        if pos - old_pos in [max_x, -max_x]:
            if pos - old_pos == max_x:
                x, y = pos_to_coor(old_pos, max_x)
            else:
                x, y = pos_to_coor(pos, max_x)
            screen.blit(scepka1_surface, (
                cell_size[0] * (x + sdvig[0] * 0.5 + 0.4),
                cell_size[1] * (y + sdvig[1] * 0.5 + 0.7)))

    def display_train(elems, max_x):
        if elems["type"] == "active":
            elem = elems["mas_elem"][0]
            old_pos = elem["pos"]
            blit(0.1, 0.1, vertun_surface, old_pos, max_x)
        else:
            old_pos = elems["mas_elem"][0]["pos"]
            if elems["mas_elem"][0]["type"] == 1:
                surface = block_surface
            else:
                surface = block2_surface
            blit(0.1, 0.1, surface, old_pos, max_x)
        i = 0
        for elem in elems["mas_elem"]:
            i += 1
            if elems["type"] == "passive" and i == 1:
                continue
            pos = elem["pos"]
            x, y = pos_to_coor(pos, max_x)
            if elem["type"] == 1:
                screen.blit(block_surface, ((0.1 + x) * cell_size[0], (0.1 + y) * cell_size[1]))
            elif elem["type"] == 2:
                screen.blit(block2_surface, ((0.1 + x) * cell_size[0], (0.1 + y) * cell_size[1]))
            display_scepka(max_x, old_pos, pos)
            old_pos = pos
        pygame.display.flip()

    def blit_sostavs(cells, max_x, max_y, horizontal_fences, vertical_fences, mode, mas_trains):
        for x in range(max_x):
            for y in range(max_y):
                rebuild(cells, max_x, max_y, horizontal_fences, vertical_fences, mode)
        # print(mas_trains)
        for elems in mas_trains:
            # print(elems)
            display_train(elems, max_x)
        make_fences(max_x, max_y)

    def rebuild(cells, max_x, max_y, horizontal_fences, vertical_fences, mode):
        pygame.draw.rect(screen, (14, 67, 120),
                         (0, 0, screen_resolution[0], screen_resolution[1]))
        if settings["robot"] in [0, 1, 2, 5]:
            for x in range(max_x):
                for y in range(max_y):
                    if cells[y * max_x + x]["type_cell"] == 0:
                        screen.blit(usual_cell_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["sticker"] == 1:
                        screen.blit(end_place_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["sticker"] == 2:
                        screen.blit(finish_block_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["sticker"] == 3:
                        screen.blit(finish_block2_surface, (cell_size[0] * x, cell_size[1] * y))
                    if cells[y * max_x + x]["sticker"] == 4:
                        screen.blit(finish_blocku_surface, (cell_size[0] * x, cell_size[1] * y))

                    if cells[y * max_x + x]["blocks"] == 1:
                        screen.blit(block_surface, (cell_size[0] * (x+0.1), cell_size[1] * (y+0.1)))
                    if cells[y * max_x + x]["blocks"] == 2:
                        screen.blit(block2_surface, (cell_size[0] * (x+0.1), cell_size[1] * (y+0.1)))

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
        # if mode != 0:
        screen.blit(vertun_surface,
                    (cell_size[0] * (0.1 + robot_pos[0]), cell_size[1] * (0.1 + robot_pos[1])))
        pygame.display.flip()

    mode = 1  # 1 2 3 4

    def make_image():
        rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 2)
        blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 1, mas_trains)
        pygame.display.update()
        image_name = file_name.split(".")[0] + "_screen.png"
        pil_string_image = pygame.image.tostring(screen, "RGBA", False)
        pil_image = Image.frombytes('RGBA', settings["screen_resolution"], pil_string_image, 'raw')
        pil_image = pil_image.crop((0, 0, screen_resolution[0], screen_resolution[1]))
        pil_image.save(image_name)

    def sostav_with(pos, mas_trains):  # возвращает номер (в массиве) состава с вагоном на позиции pos
        for i in range(len(mas_trains)):
            if mas_trains[i]["mas_elem"][0]["pos"] == pos:
                return i
            elif mas_trains[i]["mas_elem"][-1]["pos"] == pos:
                mas_trains[i]["mas_elem"] = list(reversed(mas_trains[i]["mas_elem"]))
                return i
        return -2  # не нашли составов с pos\

    def sostav_neglav_with(pos, mas_trains):
        for i in range(len(mas_trains)):
            for j in range(len(mas_trains[i]["mas_elem"])):
                if mas_trains[i]["mas_elem"][j]["pos"] == pos:
                    return i
        return -2  # не нашли составов с pos\

    def make_trains(mas_trains, cells):
        for x in range(settings["max_x"]):
            for y in range(settings["max_y"]):
                pos = x + y * settings["max_x"]
                if cells[pos]["blocks"] != 0 and sostav_neglav_with(pos, mas_trains) == -2:
                    mas_trains.append(
                        {
                            "type": "passive",
                            "mas_elem": [
                                {
                                    "type": cells[pos]["blocks"],
                                    "pos": pos
                                }
                            ]
                        }
                    )
                cells[pos]["blocks"] = 0
        if sostav_neglav_with(robot_pos[0]+settings["max_x"]*robot_pos[1], mas_trains) == -2:
            mas_trains.append(
                {
                    "type": "active",
                    "mas_elem": [
                        {
                            "type": 0,
                            "pos": robot_pos[0]+settings["max_x"]*robot_pos[1]
                        }
                    ]
                }
            )


    make_trains(mas_trains, cells)
    rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 1)
    blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, 1, mas_trains)

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
    nazh = 0
    mode = 1
    rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode)
    blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode, mas_trains)
    print("Nach")
    print(mas_trains)


    def index_in_train(train, pos):
        i = 0
        for elem in train:
            #print(elem)
            if elem["pos"] == pos:
                return i
            i += 1
        return -2

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
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mouse = ev.pos
            nazh = 1
            # print(mouse[0], screen_resolution[0], cell_size[0])
            x = int(mouse[0] // cell_size[0])
            y = int(mouse[1] // cell_size[1])
            loc_x = mouse[0] - cell_size[0] * x
            loc_y = mouse[1] - cell_size[1] * y
            gr = is_in_cell(cell_size, loc_x, loc_y)
            pos = y * settings["max_x"] + x
            if gr == 0 and vertical_fences[y * (settings["max_x"] + 1) + x + 1] != 1:
                new_pos = pos + 1
            elif gr == 1 and horizontal_fences[(y + 1) * settings["max_x"] + x] != 1:
                new_pos = pos + settings["max_x"]
            elif gr == 2 and vertical_fences[y * (settings["max_x"] + 1) + x] != 1:
                new_pos = pos - 1
            elif gr == 3 and horizontal_fences[y * settings["max_x"] + x] != 1:
                new_pos = pos - settings["max_x"]
            else:
                continue
            num_s1 = sostav_neglav_with(pos, mas_trains)
            num_s2 = sostav_neglav_with(new_pos, mas_trains)
            if num_s2 != -2 and num_s1 != -2:
                ind1 = index_in_train(mas_trains[num_s1]["mas_elem"], pos)
                len1 = len(mas_trains[num_s1]["mas_elem"])
                ind2 = index_in_train(mas_trains[num_s2]["mas_elem"], new_pos)
                len2 = len(mas_trains[num_s2]["mas_elem"])

                print("sostav")
                print(num_s2, num_s1)
                if num_s1 == num_s2:
                    print("ind")
                    print(ind1, ind2)
                    if ind2 == ind1 - 1 or ind1 == ind2 - 1:
                        if ind2 == ind1 - 1:
                            ind1, ind2 = ind2, ind1
                        mas1 = mas_trains[num_s2]["mas_elem"][:ind2]
                        mas2 = mas_trains[num_s2]["mas_elem"][ind2:]
                        type_tr1 = "passive"
                        type_tr2 = "passive"
                        if mas1[0]["type"] == 0:
                            type_tr1 = "active"
                        if mas2[-1]["type"] == 0:
                            type_tr1 = "active"
                        mas_trains[num_s1] = {
                            "type": type_tr1,
                            "mas_elem": mas1
                        }
                        mas_trains.append({
                            "type": type_tr2,
                            "mas_elem": mas2
                        })
                    else:
                        continue

                elif (ind1 == 0 or ind1 == len1 - 1) and (ind2 == 0 or ind2 == len2 - 1):
                    if mas_trains[num_s2]["mas_elem"][ind2]["type"] == 0 and len2 != 1:
                        continue
                    if mas_trains[num_s1]["mas_elem"][ind1]["type"] == 0 and len1 != 1:
                        continue
                    mas1 = mas_trains[num_s1]["mas_elem"]
                    mas2 = mas_trains[num_s2]["mas_elem"]
                    if ind1 != 0:
                        mas1 = list(reversed(mas_trains[num_s1]["mas_elem"]))
                    if ind2 != len2 - 1:
                        mas2 = list(reversed(mas_trains[num_s2]["mas_elem"]))
                    mas1 = mas2+mas1
                    type_tr = "passive"
                    if mas_trains[num_s2]["type"] == "active" or mas_trains[num_s1]["type"] == "active":
                        type_tr = "active"
                    mas_trains[num_s1] = {
                        "type": type_tr,
                        "mas_elem": mas1
                    }
                    if type_tr == "active" and mas1[0]["type"]!=0:
                        mas_trains[num_s1]["mas_elem"] = list(reversed(mas1))
                    mas_trains.pop(num_s2)


        if flag != 0 and nazh!=0:
            mouse = pygame.mouse.get_pos()
            rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode)
            blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode, mas_trains)
            nazh = 0

    settings["start_x"] = robot_pos[0]
    settings["start_y"] = robot_pos[1]
    settings["angle"] = angle

    with open(file_name, 'w') as json_file:
        initial_data = {
            "settings": settings,
            "horizontal_fences": horizontal_fences,
            "vertical_fences": vertical_fences,
            "cells": cells,
            "mas_trains": mas_trains
        }

        json.dump(initial_data, json_file, indent=4)

    game_name = file_name.split(".")[0] + "_game.py"
