import math
import pygame
import time
import json
from PIL import Image
from moscow_robots.data import get_image


# 2.1.4

def make_robot(self):
    self.screen.blit(self.robot_surface,
                     (self.cell_size[0] * (0.1 + self.x), self.cell_size[1] * (0.1 + self.y)))
    if self.num_robot == 5:
        self.blit_sostavs()


def blit_object(self, x, y, surface):
    self.screen.blit(surface, (self.cell_size[0] * x, self.cell_size[1] * y))


def make_fences(self):
    # вертикальные заборы I

    for y in range(self.count_of_cells[1]):
        for x in range(self.count_of_cells[0] + 1):
            # if x == 0 or x == self.count_of_cells[0]:
            #     self.vertical_fences[y * (self.count_of_cells[0] + 1) + x] = 1
            if self.vertical_fences[y * (self.count_of_cells[0] + 1) + x] == 1:
                self.screen.blit(self.vwall_surface,
                                 (x * self.cell_size[0] - self.cell_size[0] / 20, self.cell_size[1] * (y + 1 / 10)))

    # горизонтальные заборы _
    for y in range(self.count_of_cells[1] + 1):
        for x in range(self.count_of_cells[0]):
            # if y == 0 or y == self.count_of_cells[0]:
            #     self.horizontal_fences[y * self.count_of_cells[0] + x] = 1
            if self.horizontal_fences[y * self.count_of_cells[0] + x] == 1:
                self.screen.blit(self.hwall_surface,
                                 (self.cell_size[0] * (x + 1 / 10), y * self.cell_size[1] - self.cell_size[1] / 20))
    #pygame.display.update()


def rebuild_one_cell(self, cell, x, y):
    if self.num_robot in [3, 4]:
        self.screen.blit(self.cell_type_surface[self.cells[y * self.max_x + x]["type"]],
                         (x * self.cell_size[0], y * self.cell_size[1]))
        if cell["end"] == 1:
            self.screen.blit(self.end_place_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        if cell["blocks"] > 0:
            self.screen.blit(self.blocks_surface[cell["blocks"] - 1],
                             ((x + 0.3) * self.cell_size[0], (y + 0.3) * self.cell_size[1]))
    else:
        if cell["broken"] and cell["painted"]:
            self.screen.blit(self.painted_broken_cell_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        elif cell["broken"]:
            self.screen.blit(self.broken_cell_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        elif cell["painted"]:
            self.screen.blit(self.painted_cell_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        else:
            if self.num_robot == 0:
                self.screen.blit(self.usual_cell_surface, (x * self.cell_size[0], y * self.cell_size[1]))
            else:
                self.screen.blit(self.usual_cell_surface, (x * self.cell_size[0], y * self.cell_size[1]))

        if cell["end"] == 1:
            self.screen.blit(self.end_place_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        elif cell["end"] == 2:
            self.screen.blit(self.finish_block_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        elif cell["end"] == 3:
            self.screen.blit(self.finish_block2_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        elif cell["end"] == 4:
            self.screen.blit(self.finish_blocku_surface, (x * self.cell_size[0], y * self.cell_size[1]))
        if self.num_robot > 0 and not self.num_robot == 5:
            if cell["blocks"] == 1:
                self.screen.blit(self.block_surface, ((0.1 + x) * self.cell_size[0], (0.1 + y) * self.cell_size[1]))
            elif cell["blocks"] == 2:
                self.screen.blit(self.block2_surface, ((0.1 + x) * self.cell_size[0], (0.1 + y) * self.cell_size[1]))


def rebuild_cell_first(self, x=0, y=0):
    rebuild_one_cell(self, self.cells[self.max_x * self.y + self.x], self.x, self.y)

    if x != 0 or y != 0:
        rebuild_one_cell(self, self.cells[self.max_x * (self.y + y) + self.x + x], self.x + x, self.y + y)
    make_fences(self)


def rebuild_cell_second(self, radius):
    start_x = max(self.x - radius, 0)
    start_y = max(self.y - radius, 0)
    fin_x = min(self.x + radius + 1, self.max_x)
    fin_y = min(self.y + radius + 1, self.max_y)
    for x in range(start_x, fin_x):
        for y in range(start_y, fin_y):
            rebuild_one_cell(self, self.cells[self.max_x * y + x], x, y)

    make_fences(self)


def turn_clockwise(self, type_robot, ratio):
    if type_robot in [0, 3, 4]:
        rebuild_cell_first(self)
    elif type_robot in [1, 2, 5]:
        rebuild_cell_second(self, 1)

    mas = []
    elem1 = {}
    elem2 = {}
    if self.num_robot == 5:
        act_num = self.active_sostav()
        if len(self.mas_trains[act_num]["mas_elem"]) > 1:
            mas = self.mas_trains[act_num]["mas_elem"]
            elem1 = self.mas_trains[act_num]["mas_elem"][0]
            elem2 = self.mas_trains[act_num]["mas_elem"][1]
            # print(self.mas_trains[act_num]["mas_elem"])

            self.mas_trains.pop(act_num)
            self.mas_trains.append({
                "type": "passive",
                "mas_elem": mas[1:]
            })
            #self.blit_sostav(self.mas_trains[-1])
        elif len(self.mas_trains[act_num]["mas_elem"]) == 1:
            mas = self.mas_trains[act_num]["mas_elem"]
            self.mas_trains.pop(act_num)
        self.blit_sostavs()

    #time.sleep(1 * self.speed / 200)
    self.screen.blit(pygame.transform.rotate(self.robot_surface, -45 * ratio), (
        self.cell_size[0] * (self.x + 1 - math.sqrt(2) + 0.25 * math.sqrt(2)),
        self.cell_size[1] * (self.y + 1 - math.sqrt(2) + 0.25 * math.sqrt(2))))

    if self.num_robot == 5 and len(mas) > 1:  # отображение сцепки при повернутом на 45 градусов паровозе
        old_pos = self.x + self.y * self.max_x
        pos = mas[1]["pos"]
        self.display_scepka(old_pos, pos)
        pygame.display.update()
    #time.sleep(1 * self.speed / 200)

    if self.num_robot in [3, 4] and self.cargo_number > 0:
        coor_x = (1 - 0.4 * math.sqrt(2)) / 2 + self.x
        coor_y = (1 - 0.4 * math.sqrt(2)) / 2 + self.y
        blit_object(self, coor_x, coor_y,
                    pygame.transform.rotate(self.blocks_surface[self.cargo_number - 1], -45 * ratio))

    pygame.display.update()
    #time.sleep(1 * self.speed / 200)
    #time.sleep(1 * self.speed / 200)
    time.sleep(0.15 * self.speed / 200)
    if type_robot in [0, 3, 4]:
        rebuild_cell_first(self)
    elif type_robot in [1, 2, 5]:
        rebuild_cell_second(self, 1)

    self.robot_surface = pygame.transform.rotate(self.robot_surface, -90 * ratio)
    if type_robot != 5:
        self.screen.blit(self.robot_surface,
                     (self.cell_size[0] * (0.1 + self.x), self.cell_size[1] * (0.1 + self.y)))
    if self.num_robot in [3, 4] and self.cargo_number > 0:
        self.blocks_surface[self.cargo_number - 1] = pygame.transform.rotate(self.blocks_surface[self.cargo_number - 1],
                                                                             -90 * ratio)
        blit_object(self, self.x + 0.3, self.y + 0.3, self.blocks_surface[self.cargo_number - 1])
    self.angle = (self.angle + 1 * ratio)

    if type_robot == 5:
        if len(mas) == 1:
            self.mas_trains.append({
                "type": "active",
                "mas_elem": mas
            })
        else:
            if self.active_sostav() == -2:
                ang1 = self.angle_wagon(elem1["pos"], elem2["pos"])
                #print(ang1, self.angle, ratio)
                if (ang1 + self.angle) % 4 == 0:
                    self.mas_trains.append({
                        "type": "active",
                        "mas_elem": [{
                            "type": 0,
                            "pos": self.x + self.y * self.max_x
                        }]
                    })
                else:
                    self.mas_trains.pop(-1)
                    self.mas_trains.append({
                        "type": "active",
                        "mas_elem": mas
                    })

        #time.sleep(1 * self.speed / 200)
        self.blit_sostavs()
        print("povorot")
        #print(self.angle)
        print(self.mas_trains)


def is_available(self, x, y):
    if x < 0 or y < 0 or x > self.max_x or y > self.max_y:
        return False
    if x - self.x == 1 and self.vertical_fences[self.y * (self.count_of_cells[0] + 1) + self.x + 1] == 1:
        return False
    if x - self.x == -1 and self.vertical_fences[self.y * (self.count_of_cells[0] + 1) + self.x] == 1:
        return False
    if y - self.y == 1 and self.horizontal_fences[(self.y + 1) * self.count_of_cells[0] + self.x] == 1:
        return False
    if y - self.y == -1 and self.horizontal_fences[self.y * self.count_of_cells[0] + self.x] == 1:
        return False
    if self.num_robot == 5:
        #print(self.sostav_with(x+y*self.max_x))
        if self.sostav_with(x+y*self.max_x) != -2:
            return False

    return True


def is_available_from_to(self, start_x, start_y, x, y):
    if x < 0 or y < 0 or y > self.max_y or x > self.max_x:
        return False
    if x - start_x == 1 and self.vertical_fences[start_y * (self.count_of_cells[0] + 1) + start_x + 1] == 1:
        return False
    if x - start_x == -1 and self.vertical_fences[start_y * (self.count_of_cells[0] + 1) + start_x] == 1:
        return False
    if y - start_y == 1 and self.horizontal_fences[(start_y + 1) * self.count_of_cells[0] + start_x] == 1:
        return False
    if y - start_y == -1 and self.horizontal_fences[start_y * self.count_of_cells[0] + start_x] == 1:
        return False

    return True


def coordinate_from_angle(angle):
    change_x = 0
    change_y = 0

    if angle % 4 == 0:
        change_x = 1
    if angle % 4 == 1:
        change_y = 1
    if angle % 4 == 2:
        change_x = -1
    if angle % 4 == 3:
        change_y = -1
    return change_x, change_y


def go(self):
    rebuild_cell_first(self)
    change_x, change_y = coordinate_from_angle(self.angle)
    if self.x + change_x >= self.max_x or self.y + change_y >= self.max_y \
            or self.x + change_x < 0 or self.y + change_y < 0:
        robot_dead(self, change_x, change_y)
        return -1
    block_ahead = self.cells[self.x + change_x + self.max_x * (self.y + change_y)]["blocks"] == 0

    len_poezd = 0
    if self.num_robot == 5:
        act_num = self.active_sostav()
        len_poezd = len(self.mas_trains[act_num]["mas_elem"])
        if len_poezd>1:
            mas = self.mas_trains[act_num]["mas_elem"][1:]  # хвост без трактора
            self.mas_trains.append(
                {
                    "type": "passive",
                    "mas_elem": mas
                }
            )
            self.mas_trains.pop(act_num)
            # ]["mas_elem"] = self.mas_trains[act_num]["mas_elem"][0:1] # только трактор
            self.blit_sostavs()
            print(self.mas_trains)

    if is_available(self, self.x + change_x, self.y + change_y) and block_ahead:
        self.screen.blit(self.robot_surface, (
            self.cell_size[0] * (0.1 + self.x + change_x * 0.5),
            self.cell_size[1] * (0.1 + self.y + change_y * 0.5)))

        if self.num_robot in [3, 4] and self.cargo_number > 0:
            blit_object(self, self.x + 0.3 + change_x * 0.5, self.y + 0.3 + change_y * 0.5,
                        self.blocks_surface[self.cargo_number - 1])

        pygame.display.update()
        time.sleep(0.15 * self.speed / 200)
        rebuild_cell_first(self, change_x, change_y)
        self.x += change_x
        self.y += change_y
        if self.num_robot == 5 and len_poezd > 1:
            self.mas_trains.append({
                "type": "active",
                "mas_elem": [
                    {
                        "type": 0,
                        "pos": self.x + self.y * self.max_x
                    }
                ]
            })
            # [act_num]["mas_elem"][0]["pos"] = self.x + self.y * self.max_x
            self.blit_sostavs()

        self.screen.blit(self.robot_surface,
                         (self.cell_size[0] * (0.1 + self.x), self.cell_size[1] * (0.1 + self.y)))
        if self.num_robot in [3, 4] and self.cargo_number > 0:
            blit_object(self, self.x + 0.3, self.y + 0.3, self.blocks_surface[self.cargo_number - 1])

        pygame.display.update()
        if self.num_robot == 3:
            if 11 > self.cells[self.x + self.max_x * self.y]["type"] > 0:
                self.traveled.append(self.cells[self.x + self.max_x * self.y]["type"] - 1)
        return 0
    else:
        robot_dead(self, change_x, change_y)
        return -1


def checking_conditions(self):
    if self.num_robot == 0:  # vertun
        is_win = False
        if ([self.x, self.y] in self.end_cells or self.end_cells == []) and self.needless == [] and self.needed == []:
            is_win = True
        self.final_data = {
            "settings": self.settings,
            "cells": self.cells,
            "horizontal_fences": self.horizontal_fences,
            "vertical_fences": self.vertical_fences,
            "end_position": [self.x, self.y],
            "is_win": is_win,
            "needed": self.needed,
            "needless": self.needless
        }
        return is_win and self.alive
    elif self.num_robot in [1,2,5]:  # dvigun i tyagun i train
        is_win = True
        end = False

        if self.num_robot == 5:
            for wagons in self.mas_trains:
                for elem in wagons["mas_elem"]:
                    if elem["type"] > 0:
                        self.cells[elem["pos"]]["blocks"] = elem["type"]

        for coor in range(self.max_x * self.max_y):
            if self.cells[coor]["end"] == 1:
                end = True
            if self.cells[coor]["end"] > 1 and self.cells[coor]["blocks"] == 0:
                is_win = False
        if end and self.cells[self.x + self.y * self.max_x]["end"] != 1:
            is_win = False

        self.final_data = {
            "settings": self.settings,
            "horizontal_fences": self.horizontal_fences,
            "vertical_fences": self.vertical_fences,
            "cells": self.cells,
            "end_position": [self.x, self.y],
            "is_win": is_win
        }
        return is_win and self.alive
    elif self.num_robot in [3, 4]:

        robot_right_place = self.alive

        if self.end_cells:
            robot_right_place = robot_right_place and [self.x, self.y] in self.end_cells

        zadacha_vip = True
        if self.blocks_on_pole:
            for i in range(self.max_x * self.max_y):
                if self.cells[i]["blocks"]:
                    if self.cells[i]["type"] != self.cells[i]["blocks"]:
                        zadacha_vip = False
        else:
            zadacha_vip = self.needed == self.traveled or self.traveled == sorted(self.needed, reverse=True)
        self.final_data = {
            "settings": self.settings,
            "horizontal_fences": self.horizontal_fences,
            "vertical_fences": self.vertical_fences,
            "cells": self.cells,
            "end_position": [self.x, self.y],
            "block_on_pole": self.blocks_on_pole,
            "traveled": self.traveled,
            "needed": self.traveled,
            "is_win": robot_right_place and zadacha_vip
        }
        return robot_right_place and zadacha_vip


def make_report(self):
    pil_string_image = pygame.image.tostring(self.screen, "RGBA", False)
    pil_image = Image.frombytes('RGBA', self.settings["screen_resolution"], pil_string_image, 'raw')
    name_final_img = self.name_json.split('.')[0] + '_final_screen.png'
    pil_image.save(name_final_img)

    is_win = checking_conditions(self.robot)
    self.name_final_data = self.name_json.split('.')[0] + '_final_data.json'
    with open(self.name_final_data, 'w') as json_file:
        json.dump(self.robot.final_data, json_file, indent=4)
    if is_win:
        self.screen.blit(self.win_message, (self.pole.screen_resolution[0] / 5, 2 * self.pole.screen_resolution[1] / 5))
    else:
        self.screen.blit(self.lose_message,
                         (self.pole.screen_resolution[0] / 5, 2 * self.pole.screen_resolution[1] / 5))
    pygame.display.update()


def robot_dead(self, change_x, change_y):
    rebuild_one_cell(self, self.cells[self.x + self.y * self.max_x], self.x, self.y)
    coef = 0.2
    if self.num_robot in [3, 4]:
        change_x, change_y = coordinate_from_angle(self.angle)
        if is_available(self, self.x + change_x, self.y + change_y):
            coef = 0.4
        if self.cargo_number != -1:
            self.broken_robot_surface = self.robot_loaded_dead

    self.broken_robot_surface = pygame.transform.rotate(self.broken_robot_surface, -90 * (self.angle))
    self.screen.blit(self.broken_robot_surface, (
        self.cell_size[0] * (0.1 + self.x + change_x * coef),
        self.cell_size[1] * (0.1 + self.y + change_y * coef)))
    if self.num_robot in [3, 4]:
        if self.cargo_number != -1:
            blit_object(self, 0.3 + self.x + change_x * coef, 0.3 + self.y + change_y * coef,
                        self.blocks_surface[self.cargo_number - 1])
    make_fences(self)
    self.alive = False


def first_field_textures(self):
    name_usual_cell = "field_normal"
    if self.num_robot in [1, 2, 5]:
        name_usual_cell = "field_normal_other"
    if self.num_robot in [3, 4]:
        name_usual_cell = "rug_green"

    self.usual_cell_surface = get_image(name_usual_cell).convert()
    self.usual_cell_surface = pygame.transform.scale(self.usual_cell_surface,
                                                     (self.cell_size[0], self.cell_size[1]))

    self.broken_cell_surface = get_image("field_broken").convert()
    self.broken_cell_surface = pygame.transform.scale(self.broken_cell_surface,
                                                      (self.cell_size[0], self.cell_size[1]))


    self.painted_cell_surface = get_image("field_normal_painted").convert()
    self.painted_cell_surface = pygame.transform.scale(self.painted_cell_surface,
                                                       (self.cell_size[0], self.cell_size[1]))

    self.painted_broken_cell_surface = get_image("field_broken_painted").convert()
    self.painted_broken_cell_surface = pygame.transform.scale(self.painted_broken_cell_surface,
                                                              (self.cell_size[0], self.cell_size[1]))

    name_end_place = "robot_dest"
    if self.num_robot in [3, 4]:
        name_end_place = "rug_red"
    self.end_place_surface = get_image(name_end_place).convert_alpha()
    self.end_place_surface = pygame.transform.scale(self.end_place_surface, (self.cell_size[0], self.cell_size[1]))

    self.block_surface = get_image("block_square").convert()
    self.block_surface = pygame.transform.scale(self.block_surface,
                                                (self.cell_size[0] * 0.8, self.cell_size[1] * 0.8))
    self.block2_surface = get_image("block_circle").convert_alpha()
    self.block2_surface = pygame.transform.scale(self.block2_surface,
                                                 (self.cell_size[0] * 0.8, self.cell_size[1] * 0.8))

    self.finish_block_surface = get_image("block_square_dest").convert_alpha()
    self.finish_block_surface = pygame.transform.scale(self.finish_block_surface,
                                                       (self.cell_size[0], self.cell_size[1]))
    self.finish_block2_surface = get_image("block_circle_dest").convert_alpha()
    self.finish_block2_surface = pygame.transform.scale(self.finish_block2_surface,
                                                        (self.cell_size[0], self.cell_size[1]))
    self.finish_blocku_surface = get_image("block_any_dest").convert_alpha()
    self.finish_blocku_surface = pygame.transform.scale(self.finish_blocku_surface,
                                                        (self.cell_size[0], self.cell_size[1]))

    self.hwall_surface = get_image("wall_hor").convert()
    self.hwall_surface = pygame.transform.scale(self.hwall_surface,
                                                (self.cell_size[0] * 4 / 5, self.cell_size[1] / 10))
    self.vwall_surface = get_image("wall_vert").convert()
    self.vwall_surface = pygame.transform.scale(self.vwall_surface,
                                                (self.cell_size[0] / 10, self.cell_size[1] * 4 / 5))
    if 3 <= self.num_robot <= 4:
        self.cell_type_surface = []
        self.cell_type_surface.append(get_image("rug_green").convert())
        for i in range(10):
            name_type_cell = "rug_num" + str(i)
            self.cell_type_surface.append(get_image(name_type_cell).convert())
        self.cell_type_surface.append(get_image("rug_div").convert())
        self.cell_type_surface.append(get_image("rug_eq").convert())
        self.cell_type_surface.append(get_image("rug_minus").convert())
        self.cell_type_surface.append(get_image("rug_mul").convert())
        self.cell_type_surface.append(get_image("rug_plus").convert())

        for i in range(16):
            self.cell_type_surface[i] = pygame.transform.scale(self.cell_type_surface[i],
                                                               (self.cell_size[0], self.cell_size[1]))
        self.blocks_surface = []
        for i in range(10):
            name_block = "rblock" + str(i)
            self.blocks_surface.append(get_image(name_block).convert_alpha())
            self.blocks_surface[i] = pygame.transform.scale(self.blocks_surface[i],
                                                            (self.cell_size[0] * 0.4, self.cell_size[1] * 0.4))
        name_loaded_robot = "polzun_loaded"
        if self.num_robot == 4:
            name_loaded_robot = "tolkun_loaded"

        self.robot_loaded = get_image(name_loaded_robot).convert_alpha()
        self.robot_loaded = pygame.transform.scale(self.robot_loaded,
                                                   (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.robot_loaded_dead = get_image(name_loaded_robot + "_dead").convert_alpha()
        self.robot_loaded_dead = pygame.transform.scale(self.robot_loaded_dead,
                                                        (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))


class Vertun:
    def __init__(self, game):
        self.num_robot = 0
        self.final_data = None
        self.textures = game.textures
        self.cells = game.cells
        self.end_cells = []
        self.screen = game.pole.screen
        self.needed = []
        self.needless = []
        self.angle = game.angle# 0 -> 0, 1 -> 90, 2 -> 180, 3 -> 270
        print(self.angle)
        self.x = game.start_x
        self.y = game.start_y
        self.speed = game.speed
        self.settings = game.settings
        self.screen_resolution = game.pole.screen_resolution
        self.cell_size = [game.pole.screen_resolution[0] / game.pole.count_of_cells[0],
                          game.pole.screen_resolution[1] / game.pole.count_of_cells[1]]
        self.count_of_cells = game.pole.count_of_cells
        self.vertical_fences = game.pole.vertical_fences
        self.horizontal_fences = game.pole.horizontal_fences
        self.max_x = game.pole.count_of_cells[0]
        self.max_y = game.pole.count_of_cells[1]
        self.alive = True
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.cells[x + self.max_x * y]["broken"]:
                    self.needed.append([x, y])
                if self.cells[x + self.max_x * y]["end"] == 1:
                    self.end_cells.append([x, y])
        for i in range(game.pole.count_of_cells[0]):
            self.horizontal_fences[i] = 1
            self.horizontal_fences[i + game.pole.count_of_cells[1] * game.pole.count_of_cells[0]] = 1

        for i in range(game.pole.count_of_cells[1]):
            self.vertical_fences[i * (game.pole.count_of_cells[0] + 1)] = 1
            self.vertical_fences[game.pole.count_of_cells[0] + i * (game.pole.count_of_cells[0] + 1)] = 1

        first_field_textures(self)

        self.robot_surface = get_image("vertun").convert_alpha()
        self.robot_surface = pygame.transform.scale(self.robot_surface,
                                                    (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.robot_surface = pygame.transform.rotate(self.robot_surface, -90 * self.angle)

        self.broken_robot_surface = get_image("vertun_dead").convert_alpha()
        self.broken_robot_surface.set_colorkey((255, 255, 255))
        self.broken_robot_surface = pygame.transform.scale(self.broken_robot_surface,
                                                           (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))


        #self.angle = 0

    def paint(self):
        if self.cells[self.x + self.max_x * self.y]["broken"]:
            self.needed.remove([self.x, self.y])
        elif not self.cells[self.x + self.max_x * self.y]["painted"]:
            self.needless.append([self.x, self.y])

        self.cells[self.x + self.y * self.max_x]["painted"] = True
        rebuild_cell_first(self)

        self.screen.blit(self.robot_surface, (self.cell_size[0] * (0.1 + self.x), self.cell_size[1] * (0.1 + self.y)))

        pygame.display.update()


def go_with_block(self, num, change_x, change_y):
    if is_available(self, self.x + change_x * (num + 1), self.y + change_y * (num + 1)):
        pos = self.x + self.max_x * self.y
        sdvig = change_x + self.max_x * change_y
        self.podvin_block["klass_blocks"] = []
        for i in range(num):
            self.podvin_block["klass_blocks"].append(self.cells[pos + sdvig * (i + 1)]["blocks"])
            self.cells[pos + sdvig * (i + 1)]["blocks"] = 0
        rebuild_cell_second(self, 2)
        self.blit(0.1 + change_x * 0.5, 0.1 + change_y * 0.5, self.robot_surface)
        if self.num_robot in [3, 4] and self.cargo_number > 0:
            blit_object(self, self.x + 0.3 + change_x * 0.5, self.y + 0.3 + change_y * 0.5,
                        self.blocks_surface[self.cargo_number - 1])
        if self.num_robot == 4:
            for i in range(num):
                self.blit(0.3 + change_x * (i + 1.1), 0.3 + change_y * (i + 1.1),
                          self.blocks_surface[self.podvin_block["klass_blocks"][i] - 1])
            pygame.display.update()
            time.sleep(0.15 * self.speed / 200)
            rebuild_cell_second(self, 2)
            self.blit(0.1 + change_x * 0.75, 0.1 + change_y * 0.75, self.robot_surface)
            blit_object(self, self.x + 0.3 + change_x * 0.75, self.y + 0.3 + change_y * 0.75,
                        self.blocks_surface[self.cargo_number - 1])
        for i in range(num):
            if self.num_robot == 1:
                if self.podvin_block["klass_blocks"][i] == 1:
                    self.blit(0.1 + change_x * (i + 1.5), 0.1 + change_y * (i + 1.5), self.block_surface)
                else:
                    self.blit(0.1 + change_x * (i + 1.5), 0.1 + change_y * (i + 1.5), self.block2_surface)
            elif self.num_robot == 4:
                if self.podvin_block["klass_blocks"][i] > 0:
                    # self.blit(0.1 + change_x * 0.75, 0.1 + change_y * 0.75, self.robot_surface)
                    self.blit(0.3 + change_x * (i + 1.35), 0.3 + change_y * (i + 1.35),
                              self.blocks_surface[self.podvin_block["klass_blocks"][i] - 1])
                    # blit_object(self, self.x + 0.3 + change_x * 0.35, self.y + 0.3 + change_y * 0.35,
                    #             self.blocks_surface[self.cargo_number - 1])
        pygame.display.update()
        time.sleep(0.15 * self.speed / 200)

        rebuild_cell_second(self, 2)

        self.x += change_x
        self.y += change_y

        for i in range(num):
            self.cells[pos + sdvig * (i + 2)]["blocks"] = self.podvin_block["klass_blocks"][i]
            # self.blocks.append([self.x + change_x * (i + 1), self.y + change_y * (i + 1)])
        rebuild_cell_second(self, 2)
        if self.num_robot == 4:
            self.blit(0.1 + change_x * (i + 0.4), 0.1 + change_y * (i + 0.4),
                      self.robot_surface)
            blit_object(self, self.x + 0.3 + change_x * (i + 0.4), self.y + 0.3 + change_y * (i + 0.4),
                        self.blocks_surface[self.cargo_number - 1])
            pygame.display.update()
            time.sleep(0.15 * self.speed / 200)
            rebuild_cell_second(self, 2)

        self.blit(0.1, 0.1, self.robot_surface)
        if self.num_robot == 4:
            blit_object(self, self.x + 0.3, self.y + 0.3, self.blocks_surface[self.cargo_number - 1])
        pygame.display.update()
        return 0
    else:
        robot_dead(self, change_x, change_y)
        return -1


def go2(self):
    change_x, change_y = coordinate_from_angle(self.angle)
    pos = self.x + self.max_x * self.y
    sdvig = change_x + self.max_x * change_y

    if pos + sdvig < self.max_x * self.max_y and self.cells[pos + sdvig]["blocks"] == 0:
        return go(self)
    elif pos + sdvig * 2 < self.max_x * self.max_y and self.cells[pos + sdvig * 2]["blocks"] == 0 and \
            self.cells[pos + sdvig]["blocks"] != 0:  # odin block
        return go_with_block(self, 1, change_x, change_y)
    elif pos + sdvig * 3 < self.max_x * self.max_y and self.cells[pos + sdvig * 3]["blocks"] == 0 and \
            self.cells[pos + sdvig * 2]["blocks"] != 0 and \
            self.cells[pos + sdvig]["blocks"] != 0:  # dva block
        return go_with_block(self, 2, change_x, change_y)
    else:
        robot_dead(self, change_x, change_y)
        return -1


class Dvigun:
    def __init__(self, game):
        self.num_robot = 1
        self.final_data = None
        self.textures = game.textures
        # self.painted_cells = painted_cells
        # self.end_cells = end_cells
        # self.finish_block_cells = finish_block_cells
        # self.blocks = blocks
        self.screen = game.pole.screen
        # self.broken_cells = broken_cells
        # self.needed = broken_cells
        self.cells = game.cells
        self.x = game.start_x
        self.y = game.start_y
        self.speed = game.speed
        self.settings = game.settings
        pole = game.pole
        self.screen_resolution = pole.screen_resolution
        self.cell_size = [pole.screen_resolution[0] / pole.count_of_cells[0],
                          pole.screen_resolution[1] / pole.count_of_cells[1]]
        self.count_of_cells = pole.count_of_cells
        self.max_x, self.max_y = pole.count_of_cells
        self.vertical_fences = pole.vertical_fences
        self.horizontal_fences = pole.horizontal_fences
        self.podvin_block = {}
        self.alive = True


        for i in range(pole.count_of_cells[0]):
            self.horizontal_fences[i] = 1
            self.horizontal_fences[i + pole.count_of_cells[1] * pole.count_of_cells[0]] = 1

        for i in range(pole.count_of_cells[1]):
            self.vertical_fences[i * (pole.count_of_cells[0] + 1)] = 1
            self.vertical_fences[pole.count_of_cells[0] + i * (pole.count_of_cells[0] + 1)] = 1

        first_field_textures(self)

        self.robot_surface = get_image("dvigun").convert_alpha()
        self.robot_surface = pygame.transform.scale(self.robot_surface,
                                                    (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

		# FIXME dvigun_dead.png needed
        self.broken_robot_surface = get_image("vertun_dead").convert_alpha()
        self.broken_robot_surface.set_colorkey((255, 255, 255))
        self.broken_robot_surface = pygame.transform.scale(self.broken_robot_surface,
                                                           (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.angle = game.angle # 0 -> 0, 1 -> 90, 2 -> 180, 3 -> 270
        self.robot_surface = pygame.transform.rotate(self.robot_surface, -90 * self.angle)

    def blit(self, change_x, change_y, surface):
        self.screen.blit(surface, (
            self.cell_size[0] * (self.x + change_x),
            self.cell_size[1] * (self.y + change_y)))


class Tyagun:
    def __init__(self, game):
        self.num_robot = 2
        self.final_data = None
        self.textures = game.textures
        # self.painted_cells = painted_cells
        # self.end_cells = end_cells
        # self.finish_block_cells = finish_block_cells
        # self.blocks = blocks
        pole = game.pole
        self.screen = pole.screen
        # self.broken_cells = broken_cells
        # self.needed = broken_cells
        self.cells = game.cells
        self.x = game.start_x
        self.y = game.start_y
        self.speed = game.speed
        self.settings = game.settings
        self.screen_resolution = pole.screen_resolution
        self.cell_size = [pole.screen_resolution[0] / pole.count_of_cells[0],
                          pole.screen_resolution[1] / pole.count_of_cells[1]]
        self.count_of_cells = pole.count_of_cells
        self.max_x, self.max_y = pole.count_of_cells
        self.vertical_fences = pole.vertical_fences
        self.horizontal_fences = pole.horizontal_fences
        self.podvin_block = {}
        self.alive = True

        for i in range(pole.count_of_cells[0]):
            self.horizontal_fences[i] = 1
            self.horizontal_fences[i + pole.count_of_cells[1] * pole.count_of_cells[0]] = 1

        for i in range(pole.count_of_cells[1]):
            self.vertical_fences[i * (pole.count_of_cells[0] + 1)] = 1
            self.vertical_fences[pole.count_of_cells[0] + i * (pole.count_of_cells[0] + 1)] = 1

        first_field_textures(self)

        self.robot_surface = get_image("tyagun").convert_alpha()
        self.robot_surface = pygame.transform.scale(self.robot_surface,
                                                    (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

		# FIXME  tyagun_dead.png neaded
        self.broken_robot_surface = get_image("vertun_dead").convert_alpha()
        self.broken_robot_surface.set_colorkey((255, 255, 255))
        self.broken_robot_surface = pygame.transform.scale(self.broken_robot_surface,
                                                           (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.angle = 0  # 0 -> 0, 1 -> 90, 2 -> 180, 3 -> 270

    def blit(self, change_x, change_y, surface):
        self.screen.blit(surface, (
            self.cell_size[0] * (self.x + change_x),
            self.cell_size[1] * (self.y + change_y)))

    def pull_block(self):
        change_x, change_y = coordinate_from_angle(self.angle)
        if is_available(self, self.x + change_x, self.y + change_y * 1):
            pos = self.x + self.max_x * self.y
            sdvig = change_x + self.max_x * change_y
            self.podvin_block["klass_blocks"] = self.cells[pos - sdvig]["blocks"]
            self.cells[pos - sdvig]["blocks"] = 0
            rebuild_cell_second(self, 1)
            self.blit(0.1 + change_x * 0.5, 0.1 + change_y * 0.5, self.robot_surface)
            if self.podvin_block["klass_blocks"] == 1:
                self.blit(0.1 - change_x * 0.5, 0.1 - change_y * 0.5, self.block_surface)
            else:
                self.blit(0.1 - change_x * 0.5, 0.1 - change_y * 0.5, self.block2_surface)

            pygame.display.update()
            time.sleep(0.15 * self.speed / 200)

            rebuild_cell_second(self, 2)

            self.x += change_x
            self.y += change_y

            self.cells[pos]["blocks"] = self.podvin_block["klass_blocks"]
            # self.blocks.append([self.x + change_x * (i + 1), self.y + change_y * (i + 1)])
            rebuild_cell_second(self, 2)
            self.blit(0.1, 0.1, self.robot_surface)

            pygame.display.update()
            return 0
        else:
            robot_dead(self, change_x, change_y)
            return -1


def load(self):
    change_x, change_y = coordinate_from_angle(self.angle)
    if self.cells[(self.y + change_y) * self.max_x + self.x + change_x]["blocks"] > 0 and self.cargo_number == -1:
        self.robot_surface = pygame.transform.rotate(self.robot_loaded, -90 * self.angle)

        self.cargo_number = self.cells[(self.y + change_y) * self.max_x + self.x + change_x]["blocks"]
        self.cells[(self.y + change_y) * self.max_x + self.x + change_x]["blocks"] = 0
        rebuild_cell_second(self, 1)
        blit_object(self, 0.1 + self.x, 0.1 + self.y, self.robot_surface)
        blit_object(self, self.x + 0.3, self.y + 0.3, self.blocks_surface[self.cargo_number - 1])
        pygame.display.update()
        self.old_angle = self.angle


def unload(self):
    change_x, change_y = coordinate_from_angle(self.angle)
    if self.cells[(self.y + change_y) * self.max_x + self.x + change_x]["blocks"] == 0 and self.cargo_number != -1:
        robot_name = "polzun"
        if self.num_robot == 4:
            robot_name = "tolkun"
        self.robot_surface = get_image(robot_name + "_empty").convert_alpha()
        self.robot_surface = pygame.transform.scale(self.robot_surface,
                                                    (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.robot_surface = pygame.transform.rotate(self.robot_surface, -90 * self.angle)

        self.cells[(self.y + change_y) * self.max_x + self.x + change_x]["blocks"] = self.cargo_number
        self.cargo_number = -1
        rebuild_cell_second(self, 1)
        blit_object(self, 0.1 + self.x, 0.1 + self.y, self.robot_surface)
        pygame.display.update()


class Polzun:
    def __init__(self, game):
        self.num_robot = 3
        self.final_data = None
        self.textures = game.textures
        self.cells = game.cells
        self.end_cells = []
        pole = game.pole
        self.screen = pole.screen
        self.traveled = []
        self.x = game.start_x
        self.y = game.start_y
        self.speed = game.speed
        self.settings = game.settings
        self.screen_resolution = pole.screen_resolution
        self.cell_size = [pole.screen_resolution[0] / pole.count_of_cells[0],
                          pole.screen_resolution[1] / pole.count_of_cells[1]]
        self.count_of_cells = pole.count_of_cells
        self.vertical_fences = pole.vertical_fences
        self.horizontal_fences = pole.horizontal_fences
        self.max_x = pole.count_of_cells[0]
        self.max_y = pole.count_of_cells[1]
        self.alive = True
        self.needed = []
        self.blocks_on_pole = False
        self.cargo_number = -1
        self.old_angle = 0

        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.cells[x + self.max_x * y]["end"] == 1:
                    self.end_cells.append([x, y])
                if 11 > self.cells[x + self.max_x * y]["type"] > 0:
                    self.needed.append(self.cells[x + self.max_x * y]["type"] - 1)
                if self.cells[x + self.max_x * y]["blocks"] > 0:
                    self.blocks_on_pole = True

        if 11 > self.cells[self.x + self.max_x * self.y]["type"] > 0:
            self.traveled.append(self.cells[self.x + self.max_x * self.y]["type"] - 1)

        for item in self.needed:
            count = self.needed.count(item)
            for i in range(count - 1):
                self.needed.remove(item)
        self.needed.sort()

        for i in range(pole.count_of_cells[0]):
            self.horizontal_fences[i] = 1
            self.horizontal_fences[i + pole.count_of_cells[1] * pole.count_of_cells[0]] = 1

        for i in range(pole.count_of_cells[1]):
            self.vertical_fences[i * (pole.count_of_cells[0] + 1)] = 1
            self.vertical_fences[pole.count_of_cells[0] + i * (pole.count_of_cells[0] + 1)] = 1

        first_field_textures(self)

        self.robot_surface = get_image("polzun_empty").convert_alpha()
        self.robot_surface = pygame.transform.scale(self.robot_surface,
                                                    (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.broken_robot_surface = get_image("polzun_empty_dead").convert_alpha()
        self.broken_robot_surface.set_colorkey((255, 255, 255))
        self.broken_robot_surface = pygame.transform.scale(self.broken_robot_surface,
                                                           (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))
        self.robot_loaded
        self.angle = game.angle  # 0 -> 0, 1 -> 90, 2 -> 180, 3 -> 270

        self.robot_surface = pygame.transform.rotate(self.robot_surface, -90 * self.angle)


class Tolkun:
    def __init__(self, game):
        self.num_robot = 4
        self.final_data = None
        self.textures = game.textures
        self.cells = game.cells
        self.end_cells = []
        pole = game.pole
        self.screen = game.pole.screen
        self.traveled = []
        self.x = game.start_x
        self.y = game.start_y
        self.speed = game.speed
        self.settings = game.settings
        self.screen_resolution = pole.screen_resolution
        self.cell_size = [pole.screen_resolution[0] / pole.count_of_cells[0],
                          pole.screen_resolution[1] / pole.count_of_cells[1]]
        self.count_of_cells = pole.count_of_cells
        self.vertical_fences = pole.vertical_fences
        self.horizontal_fences = pole.horizontal_fences
        self.max_x = pole.count_of_cells[0]
        self.max_y = pole.count_of_cells[1]
        self.alive = True
        self.needed = []
        self.blocks_on_pole = False
        self.cargo_number = -1
        self.podvin_block = {}

        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.cells[x + self.max_x * y]["end"] == 1:
                    self.end_cells.append([x, y])
                if 11 > self.cells[x + self.max_x * y]["type"] > 0:
                    self.needed.append(self.cells[x + self.max_x * y]["type"] - 1)
                if self.cells[x + self.max_x * y]["blocks"] > 0:
                    self.blocks_on_pole = True

        if 11 > self.cells[self.x + self.max_x * self.y]["type"] > 0:
            self.traveled.append(self.cells[self.x + self.max_x * self.y]["type"] - 1)

        for item in self.needed:
            count = self.needed.count(item)
            for i in range(count - 1):
                self.needed.remove(item)
        self.needed.sort()

        for i in range(pole.count_of_cells[0]):
            self.horizontal_fences[i] = 1
            self.horizontal_fences[i + pole.count_of_cells[1] * pole.count_of_cells[0]] = 1

        for i in range(pole.count_of_cells[1]):
            self.vertical_fences[i * (pole.count_of_cells[0] + 1)] = 1
            self.vertical_fences[pole.count_of_cells[0] + i * (pole.count_of_cells[0] + 1)] = 1

        first_field_textures(self)

        self.robot_surface = get_image("tolkun_empty").convert_alpha()
        self.robot_surface = pygame.transform.scale(self.robot_surface,
                                                    (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.broken_robot_surface = get_image("tolkun_empty_dead").convert_alpha()
        self.broken_robot_surface.set_colorkey((255, 255, 255))
        self.broken_robot_surface = pygame.transform.scale(self.broken_robot_surface,
                                                           (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.angle = game.angle # 0 -> 0, 1 -> 90, 2 -> 180, 3 -> 270

        self.robot_surface = pygame.transform.rotate(self.robot_surface, -90 * self.angle)

    def blit(self, change_x, change_y, surface):
        self.screen.blit(surface, (
            self.cell_size[0] * (self.x + change_x),
            self.cell_size[1] * (self.y + change_y)))


def make_trains(self, cells):
    mass = [
        {
            "type": "active",
            "mas_elem": [
                {
                    "type": 0,  # 0 - tractor, 1 - block1, 2 - block2
                    "pos": self.x + self.y * self.max_x
                }
            ]
        }
    ]
    for i in range(self.max_x * self.max_y):
        if cells[i]["blocks"] != 0:
            mass.append(
                {
                    "type": "passive",
                    "mas_elem": [
                        {
                            "type": cells[i]["blocks"],
                            "pos": i
                        }
                    ]
                }
            )
            cells[i]["blocks"] = 0
    return mass


class Train:
    def __init__(self, game):
        self.num_robot = 5
        self.final_data = None
        self.textures = game.textures
        pole = game.pole
        self.screen = pole.screen
        self.cells = game.cells
        self.x = game.start_x
        self.y = game.start_y
        self.speed = game.speed
        self.settings = game.settings
        self.screen_resolution = pole.screen_resolution
        self.cell_size = [pole.screen_resolution[0] / pole.count_of_cells[0],
                          pole.screen_resolution[1] / pole.count_of_cells[1]]
        self.count_of_cells = pole.count_of_cells
        self.max_x, self.max_y = pole.count_of_cells
        self.vertical_fences = pole.vertical_fences
        self.horizontal_fences = pole.horizontal_fences
        # self.podvin_block = []

        if not game.mas_trains:
            self.mas_trains = make_trains(self, game.cells)
        else:
            self.mas_trains = game.mas_trains

        self.alive = True
        self.pole = pole

        for i in range(pole.count_of_cells[0]):
            self.horizontal_fences[i] = 1
            self.horizontal_fences[i + pole.count_of_cells[1] * pole.count_of_cells[0]] = 1

        for i in range(pole.count_of_cells[1]):
            self.vertical_fences[i * (pole.count_of_cells[0] + 1)] = 1
            self.vertical_fences[pole.count_of_cells[0] + i * (pole.count_of_cells[0] + 1)] = 1

        first_field_textures(self)

        self.robot_surface = get_image("train").convert_alpha()
        self.robot_surface = pygame.transform.scale(self.robot_surface,
                                                    (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.broken_robot_surface = get_image("train_dead").convert_alpha()
        self.broken_robot_surface.set_colorkey((255, 255, 255))
        self.broken_robot_surface = pygame.transform.scale(self.broken_robot_surface,
                                                           (min(self.cell_size) * 0.8, min(self.cell_size) * 0.8))

        self.scepka_surface = get_image("scepka").convert()
        self.scepka_surface = pygame.transform.scale(self.scepka_surface,
                                                     (self.cell_size[0] * 0.6, self.cell_size[1] * 0.2))

        self.scepka1_surface = pygame.transform.rotate(self.scepka_surface, 90)

        self.angle = 0  # 0 -> 0, 1 -> 90, 2 -> 180, 3 -> 270

    def blit(self, change_x, change_y, surface, pos):
        x = pos % self.max_x
        y = int(pos / self.max_x)
        self.screen.blit(surface, (
            self.cell_size[0] * (x + change_x),
            self.cell_size[1] * (y + change_y)))

    def blit_sostavs(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                rebuild_one_cell(self, self.cells[self.max_x * y + x], x, y)
        for elems in self.mas_trains:
            #print(elems)
            self.display_train(elems)
        make_fences(self.pole)

    def blit_sostav(self, sostav):
        mas = sostav["mas_elem"]
        for elem in mas:
            x = elem["pos"] % self.max_x
            y = int(elem["pos"] / self.max_x)
            rebuild_one_cell(self, self.cells[self.max_x * y + x], x, y)
        self.display_train(sostav)

    def display_train(self, elems):
        if elems["type"] == "active":
            old_pos = self.x + self.y * self.max_x
            self.blit(0.1, 0.1, self.robot_surface, old_pos)
        else:
            old_pos = elems["mas_elem"][0]["pos"]
            if elems["mas_elem"][0]["type"] == 1:
                surface = self.block_surface
            else:
                surface = self.block2_surface
            self.blit(0.1, 0.1, surface, old_pos)
        i = 0
        for elem in elems["mas_elem"]:
            i += 1
            if elems["type"] == "passive" and i == 1:
                continue
            pos = elem["pos"]
            x, y = self.pos_to_coor(pos)
            if elem["type"] == 1:
                self.screen.blit(self.block_surface, ((0.1 + x) * self.cell_size[0], (0.1 + y) * self.cell_size[1]))
            elif elem["type"] == 2:
                self.screen.blit(self.block2_surface, ((0.1 + x) * self.cell_size[0], (0.1 + y) * self.cell_size[1]))
            self.display_scepka(old_pos, pos)
            old_pos = pos
        #pygame.display.update()

    def display_scepka(self, old_pos, pos, sdvig=None):
        if sdvig is None:
            sdvig = [0, 0]
        #print(sdvig)
        if pos - old_pos in [-1, 1]:
            if pos - old_pos == 1:
                x, y = self.pos_to_coor(old_pos)
            else:
                x, y = self.pos_to_coor(pos)
            self.screen.blit(self.scepka_surface, (
                self.cell_size[0] * (x+sdvig[0]*0.5 + 0.7),
                self.cell_size[1] * (y+sdvig[1]*0.5 + 0.4)))
        if pos - old_pos in [self.max_x, -self.max_x]:
            if pos - old_pos == self.max_x:
                x, y = self.pos_to_coor(old_pos)
            else:
                x, y = self.pos_to_coor(pos)
            self.screen.blit(self.scepka1_surface, (
                self.cell_size[0] * (x+sdvig[0]*0.5 + 0.4),
                self.cell_size[1] * (y+sdvig[1]*0.5 + 0.7)))

    def sostav_with(self, pos):  # возвращает номер (в массиве) состава с вагоном на позиции pos
        for i in range(len(self.mas_trains)):
            if self.mas_trains[i]["mas_elem"][0]["pos"] == pos:
                return i
            elif self.mas_trains[i]["mas_elem"][-1]["pos"] == pos:
                self.mas_trains[i]["mas_elem"] = list(reversed(self.mas_trains[i]["mas_elem"]))
                return i
        return -2  # не нашли составов с pos

    def active_sostav(self):  # возвращает номер (в массиве) активного состава
        for i in range(len(self.mas_trains)):
            if self.mas_trains[i]["type"] == "active":
                return i
        return -2

    def block_around(self, start_pos, act_num):
        itr_mas = [0, -1, 1]
        if self.x+self.y*self.max_x != start_pos:
            itr_mas = [0, -1, 1, 2]
        for i in itr_mas:
            change_x, change_y = coordinate_from_angle(self.angle + i)
            pos = start_pos - self.max_x * change_y - change_x
            avai = is_available_from_to(self, start_pos % self.max_x, int(start_pos / self.max_x), pos % self.max_x,
                                        int(pos / self.max_x))
            if avai:
                num = self.sostav_with(pos)
                if num != -2 and num != act_num:
                    #print("i="+str(i))
                    return num
        return -2  # не нашли вообще

    def pos_to_coor(self, pos):
        return pos % self.max_x, int(pos / self.max_x)

    def link_one(self):
        act_num = self.active_sostav()

        act_sost = self.mas_trains[act_num]
        old_pos = act_sost["mas_elem"][-1]["pos"]
        pris_num = self.block_around(old_pos, act_num)
        if pris_num == -2:
            return -2
        self.mas_trains[act_num]["mas_elem"] = self.mas_trains[act_num]["mas_elem"] + self.mas_trains[pris_num][
            "mas_elem"]
        self.mas_trains.pop(pris_num)
        self.blit_sostavs()
        #print("link_one")
        #print(self.mas_trains)

    def link_all(self):
        act_num = self.active_sostav()
        act_mas = self.mas_trains[act_num]["mas_elem"]
        len_old = 0
        #print("link_all start")
        while self.link_one() != -2:
            len_old+=1
        print(self.mas_trains)
        print("link_all end")

    def unlink(self, every):
        if every:
            act_num = self.active_sostav()
            act_sost = self.mas_trains[act_num]
            for elem in act_sost["mas_elem"]:
                if elem["type"] == 0:
                    typesos = "active"
                else:
                    typesos = "passive"

                self.mas_trains.append(
                    {
                        "type": typesos,
                        "mas_elem": [elem]
                    }
                )
            self.mas_trains.pop(act_num)
            print("unlink_all")
            print(self.mas_trains)
        else:
            act_num = self.active_sostav()
            act_sost = self.mas_trains[act_num]
            if len(act_sost["mas_elem"]) > 1:
                elem = act_sost["mas_elem"][-1]
                self.mas_trains[act_num]["mas_elem"].pop(-1)
                self.mas_trains.append(
                    {
                        "type": "passive",
                        "mas_elem": [elem]
                    }
                )
            print("unlink_one")
            print(self.mas_trains)
        self.blit_sostavs()
        # print(self.podvin_block)

    def angle_wagon(self, pos1, pos2):
        if pos2 - pos1 in [-1, 1]:
            if pos2 - pos1 == 1:
                return 0
            else:
                return 2
        if pos2 - pos1 in [self.max_x, -self.max_x]:
            if pos2 - pos1 == self.max_x:
                return 1
            else:
                return 3

    def angle_to_change(self, angle):
        if angle%4 == 0:
            return [1, 0]
        elif angle%4 == 1:
            return [0, 1]
        elif angle%4 == 2:
            return [-1, 0]
        elif angle%4 == 3:
            return [0, -1]

    def make_lines_of_wagons(self):
        lines = []
        line = [
            {
                "xy": [self.x, self.y],
                "c_xy": self.angle_to_change(self.angle),
                "type": 0
            }
        ]
        pos1 = self.x + self.y * self.max_x
        angle1 = self.angle
        act_num = self.active_sostav()
        act_sost = self.mas_trains[act_num]["mas_elem"]
        for elem in act_sost[1:]:
            pos2 = elem["pos"]
            angle2 = (self.angle_wagon(pos1, pos2)+2)%4
            #print("angle")
            #print(pos1, pos2, angle2, angle1)
            if (angle1 - angle2) % 4 == 0:
                line.append(
                    {
                        "xy": self.pos_to_coor(pos2),
                        "c_xy": self.angle_to_change(angle2),
                        "type": elem["type"]
                    }
                )
            else:
                lines.append(line)
                line = [
                    {
                        "xy": self.pos_to_coor(pos2),
                        "c_xy": self.angle_to_change(angle2),
                        "type": elem["type"]
                    }
                ]
            pos1 = pos2
            angle1 = angle2
        lines.append(line)
        # print(lines)
        return lines

    def display_sdvig_line(self, elems):
        train_wagon = elems[0]
        surface = self.robot_surface
        if train_wagon["type"] == 1:
            surface = self.block_surface
        elif train_wagon["type"] == 2:
            surface = self.block2_surface
        old_pos = train_wagon["xy"][0] + train_wagon["xy"][1] * self.max_x
        self.blit(0.1 + train_wagon["c_xy"][0]*0.5, 0.1 + train_wagon["c_xy"][1]*0.5, surface, old_pos)
        for elem in elems[1:]:
            x, y = elem["xy"]
            pos = x + y * self.max_x
            if elem["type"] == 1:
                surface = self.block_surface
            elif elem["type"] == 2:
                surface = self.block2_surface
            self.blit(0.1 + elem["c_xy"][0]*0.5, 0.1 + elem["c_xy"][1]*0.5, surface, pos)
            #print(old_pos, pos)
            self.display_scepka(old_pos, pos, train_wagon["c_xy"])
            old_pos = pos

    def line_to_train(self, line):
        mas = []
        for elem in line:
            mas.append({
                "type": elem["type"],
                "pos": elem["xy"][0]+elem["c_xy"][0]+(elem["xy"][1]+elem["c_xy"][1])*self.max_x
            })
        return mas

    def go_with_wagons(self):
        change_x, change_y = coordinate_from_angle(self.angle)
        if not is_available(self, self.x + change_x, self.y + change_y * 1):
            act_num = self.active_sostav()
            self.mas_trains[act_num]["type"] = "passive"
            self.mas_trains[act_num]["mas_elem"] = self.mas_trains[act_num]["mas_elem"][1:]
            print(self.mas_trains[act_num]["mas_elem"])
            self.blit_sostavs()
            pygame.display.update()
            robot_dead(self, change_x, change_y)
            return -1
        else:
            lines = self.make_lines_of_wagons()
            vstali = 0
            act_num = self.active_sostav()
            act_sost = self.mas_trains[act_num]["mas_elem"]
            self.mas_trains.pop(act_num)

            self.mas_trains.append({
                "type": "passive",
                "mas_elem": act_sost
            })
            j = 0
            num_l = len(self.mas_trains)
            # start_pos = self.x + self.y * self.max_x
            #print(lines)
            for line in lines:
                len_line = len(line)
                #print("helo")
                #print(self.mas_trains[num_l-1]["mas_elem"], len_line)
                self.mas_trains[num_l-1]["mas_elem"] = self.mas_trains[num_l-1]["mas_elem"][len_line:]
                if len(self.mas_trains[num_l-1]["mas_elem"]) == 0:
                    self.mas_trains.pop(num_l - 1)
                    act_num -=1
                #print(self.mas_trains[num_l-1]["mas_elem"], len_line)
                self.blit_sostavs()
                self.display_sdvig_line(line)

                #print(line)
                pygame.display.update()
                #time.sleep(1 * self.speed / 200)
                time.sleep(0.15 * self.speed / 200)
                if j == 0:
                    self.mas_trains.append(
                        {
                            "type": "active",
                            "mas_elem": self.line_to_train(line)
                        }
                    )
                    self.x = line[0]["xy"][0] + line[0]["c_xy"][0]
                    self.y = line[0]["xy"][1] + line[0]["c_xy"][1]
                    #print(self.line_to_train(line))
                    act_num = self.active_sostav()
                    j=1
                else:
                    self.mas_trains[act_num]["mas_elem"] = self.mas_trains[act_num]["mas_elem"] + self.line_to_train(line)
                pygame.display.update()
                time.sleep(0.15 * self.speed / 200)

            self.blit_sostavs()
            # print(self.podvin_block)
            print(self.mas_trains[act_num]["mas_elem"])
            pygame.display.update()

            return 0
