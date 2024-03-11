import pygame
import json
from PIL import Image
import os.path
import math
from moscow_robots.data import get_image


# 0 вертун 1 двигун 2 тягун 3 ползун 4 толкун 5 поезд
robot_names = ["vertun", "dvigun", "tyagun", "polzun", "tolkun", "train"]

def edit_level(file_name=None, settings=None):
    if settings is None:
        settings = {}

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

    def blocks_from_sostavs(mas_trains, cells): # unused
        for i in range(len(mas_trains)):
            for j in range(len(mas_trains[i]["mas_elem"])):
                if mas_trains[i]["mas_elem"][j]["type"] != 0:
                    cells[mas_trains[i]["mas_elem"][j]["pos"]]["blocks"] = mas_trains[i]["mas_elem"][j]["type"]


    def make_fences(max_x, max_y):
        # вертикальные заборы I
        for y in range(max_y):
            for x in range(max_x + 1):
                # if x == 0 or x == self.count_of_cells[0]:
                #     self.vertical_fences[y * (self.count_of_cells[0] + 1) + x] = 1
                if vertical_fences[y * (max_x + 1) + x] == 1:
                    screen.blit(vwall_surface,
                                (x * max_x - max_x / 20, max_y * (y + 1 / 10)))

        # горизонтальные заборы _
        for y in range(max_y + 1):
            for x in range(max_x):
                # if y == 0 or y == self.count_of_cells[0]:
                #     self.horizontal_fences[y * self.count_of_cells[0] + x] = 1
                if horizontal_fences[y * max_x + x] == 1:
                    screen.blit(hwall_surface,
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
                        screen.blit(vwall_surface,
                                    (x * cell_size[0] - cell_size[0] / 20, cell_size[1] * (y + 1 / 10)))
            # горизонтальные заборы _
            for y in range(settings["max_y"] + 1):
                for x in range(settings["max_x"]):
                    if horizontal_fences[y * settings["max_x"] + x] == 1:
                        screen.blit(hwall_surface,
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

    def index_in_train(train, pos):
        i = 0
        for elem in train:
            #print(elem)
            if elem["pos"] == pos:
                return i
            i += 1
        return -2


    if not file_name:
        file_name = "mr-level.json"
        print("No file name given, using", file_name)

    file_name_base = file_name.split(".")[0]

    if os.path.exists(file_name):
        print("Found saved file, ignoring most passed settings")
        with open(file_name, "r") as json_file:
            initial_data = json.load(json_file)

        if "settings" in initial_data.keys():
            isettings = initial_data["settings"]
            settings["max_x"] = isettings["max_x"]
            settings["max_y"] = isettings["max_y"]
            settings["robot"] = isettings["robot"]
            settings["start_x"] = isettings["start_x"]
            settings["start_y"] = isettings["start_y"]
            settings["angle"] = isettings["angle"]

        if "horizontal_fences" in initial_data.keys():
            horizontal_fences = initial_data["horizontal_fences"]

        if "vertical_fences" in initial_data.keys():
            vertical_fences = initial_data["vertical_fences"]

        if "cells" in initial_data.keys():
            cells = initial_data["cells"]

        for i in range(settings["max_x"] * settings["max_y"]):
            if cells[i]["sticker"] > 0 and name_robot in ["polzun", "tolkun"]:
                cells[i]["type_cell"] = 11

        if "mas_trains" in initial_data.keys():
            mas_trains = initial_data["mas_trains"]

    else:  # No saved file found
        horizontal_fences = []
        vertical_fences = []
        cells = []
        mas_trains = []

    robot_kind = settings["robot"]
    name_robot = robot_names[settings["robot"]]
    robot_pos = [settings["start_x"], settings["start_y"]]
    angle = settings["angle"]
    cell_size = [settings["screen_resolution"][0] / settings["max_x"],
                 settings["screen_resolution"][1] / settings["max_y"]]
    razmer_y = max(settings["screen_resolution"][1], 6 * cell_size[1]/2)
    screen_resolution = [math.ceil(settings["screen_resolution"][0]+cell_size[0]), math.ceil(razmer_y)]

    pygame.init()
    screen = pygame.display.set_mode(screen_resolution)

    name_end_place = "robot_dest"
    if settings["robot"] in [3, 4]:
        name_end_place = "rug_red"
    end_place_surface = get_image(name_end_place).convert_alpha()
    end_place_surface = pygame.transform.scale(end_place_surface, (cell_size[0], cell_size[1]))

    block_surface = get_image("block_square").convert()
    block_surface = pygame.transform.scale(block_surface, (cell_size[0]*0.8, cell_size[1]*0.8))

    block2_surface = get_image("block_circle").convert_alpha()
    block2_surface = pygame.transform.scale(block2_surface, (cell_size[0]*0.8, cell_size[1]*0.8))

    finish_block_surface = get_image("block_square_dest").convert_alpha()
    finish_block_surface = pygame.transform.scale(finish_block_surface, (cell_size[0], cell_size[1]))

    finish_block2_surface = get_image("block_circle_dest").convert_alpha()
    finish_block2_surface = pygame.transform.scale(finish_block2_surface, (cell_size[0], cell_size[1]))

    finish_blocku_surface = get_image("block_any_dest").convert_alpha()
    finish_blocku_surface = pygame.transform.scale(finish_blocku_surface, (cell_size[0], cell_size[1]))

    name_usual_cell = "field_normal"
    if settings["robot"] in [1, 2, 5]:
        name_usual_cell = "field_normal_other"
    if settings["robot"] in [3, 4]:  # polzun tolkun
        name_usual_cell = "rug_green"
    usual_cell_surface = get_image(name_usual_cell).convert()
    usual_cell_surface = pygame.transform.scale(usual_cell_surface, (cell_size[0], cell_size[1]))
    painted_cell_surface = get_image("field_normal_painted").convert()
    painted_cell_surface = pygame.transform.scale(painted_cell_surface, (cell_size[0], cell_size[1]))

    broken_cell_surface = get_image("field_broken").convert()
    broken_cell_surface = pygame.transform.scale(broken_cell_surface, (cell_size[0], cell_size[1]))

    painted_broken_cell_surface = get_image("field_broken_painted").convert()
    painted_broken_cell_surface = pygame.transform.scale(painted_broken_cell_surface,
                                                         (cell_size[0], cell_size[1]))

    if settings["robot"] == 5:
        scepka_surface = get_image("scepka").convert()
        scepka_surface = pygame.transform.scale(scepka_surface,
                                                (cell_size[0] * 0.6, cell_size[1] * 0.2))
        scepka1_surface = pygame.transform.rotate(scepka_surface, 90)

    if settings["robot"] in [3, 4]:
        cell_type_surface = []
        cell_type_surface.append(get_image("rug_green").convert_alpha())

        for i in range(10):
            name_type_cell = "num" + str(i)
            cell_type_surface.append(get_image(name_type_cell).convert_alpha())

        cell_type_surface.append(end_place_surface)

        for i in range(len(cell_type_surface)):
            cell_type_surface[i] = pygame.transform.scale(cell_type_surface[i], (cell_size[0], cell_size[1]))

        blocks_surface = []
        for i in range(10):
            name_block = "rblock" + str(i)
            blocks_surface.append(get_image(name_block).convert())
            blocks_surface[i] = pygame.transform.scale(blocks_surface[i], (cell_size[0] * 0.4, cell_size[1] * 0.4))


    hwall_surface = get_image("wall_hor").convert()
    hwall_surface = pygame.transform.scale(hwall_surface, (cell_size[0] * 4 / 5, cell_size[1] / 10))
    vwall_surface = get_image("wall_vert").convert()
    vwall_surface = pygame.transform.scale(vwall_surface, (cell_size[0] / 10, cell_size[1] * 4 / 5))

    surface_name = name_robot
    if settings["robot"] in [3, 4]:
        surface_name += "_empty"
    vertun_surface = get_image(surface_name).convert_alpha()
    vertun_surface = pygame.transform.scale(vertun_surface, (min(cell_size) * 0.8, min(cell_size) * 0.8))

    tool_bar_surface = []
    d_tool_bar_surface = [0]
    for i in range(6):
        name_tool_bar = "tool_bar" + str(i + 1)
        tool_bar_surface.append(get_image(name_tool_bar).convert_alpha())
        tool_bar_surface[i] = pygame.transform.scale(tool_bar_surface[i], (cell_size[0], cell_size[0] * 0.5))
        if i > 0:
            name_tool_bar = name_tool_bar + "d"
            d_tool_bar_surface.append(get_image(name_tool_bar).convert_alpha())
            d_tool_bar_surface[i] = pygame.transform.scale(d_tool_bar_surface[i], (cell_size[0], cell_size[0] * 0.5))

    pygame.display.flip()

    if not horizontal_fences:
        for i in range(settings["max_x"] * (settings["max_y"] + 1)):
            horizontal_fences.append(0)
    if not vertical_fences:
        for i in range((settings["max_x"] + 1) * settings["max_y"]):
           vertical_fences.append(0)

    if not cells:
        for i in range(settings["max_x"] * settings["max_y"]):
            cells.append(
                {
                    "pos": i,
                    "blocks": 0,
                    "sticker": 0,
                    "type_cell": 0
                }
            )

    if not mas_trains:
        make_trains(mas_trains, cells)

    vertun_surface = pygame.transform.rotate(vertun_surface, -90*angle)

    flag = 1
    perenos = 0
    mode = 1
    rebuild(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode)
    if settings["robot"] == 5:
        blit_sostavs(cells, settings["max_x"], settings["max_y"], horizontal_fences, vertical_fences, mode, mas_trains)

    while flag:
        nazh = 0
        ev = pygame.event.wait()
        if ev.type == pygame.QUIT:
            break
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                break
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


    # main loop finished

    make_image()
    pygame.quit()
    flag = 0

    settings["start_x"] = robot_pos[0]
    settings["start_y"] = robot_pos[1]
    settings["angle"] = angle
    print(settings)

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

    with open(file_name, 'w') as json_file:
        json.dump(initial_data, json_file, indent=4)

    game_name = file_name_base + "_game.py"
    if not os.path.exists(game_name):
        with open(game_name, 'w') as fp:
            print("from moscow_robots import Game", file=fp)
            print("mg = Game(\"" + file_name + "\")", file=fp)
            print("mg.main_loop()", file=fp)

