import pygame
import time
import json
from moscow_robots import robots as function_robots
from moscow_robots.data import get_image


# 2.1.4

def decode_cells(self, cells):
    if "type_cell" not in cells[0].keys():
        return
    if self.num_robot == 0:
        for i in range(self.max_x * self.max_y):
            broken = False
            if cells[i]["type_cell"] in [1, 2]:
                broken = True
            painted = False
            if cells[i]["type_cell"] in [2, 3]:
                painted = True
            self.cells[i] = {
                "broken": broken,
                "painted": painted,
                "end": cells[i]["sticker"],
                "blocks": cells[i]["blocks"]
            }
    if self.num_robot in [1, 2]:
        for i in range(self.max_x * self.max_y):
            self.cells[i] = {
                "broken": False,
                "painted": False,
                "end": cells[i]["sticker"],
                "blocks": cells[i]["blocks"]
            }
    if self.num_robot in [3, 4]:
        for i in range(self.max_x * self.max_y):
            self.cells[i] = {
                "broken": False,
                "painted": False,
                "end": cells[i]["sticker"],
                "blocks": cells[i]["blocks"],
                "type": cells[i]["type_cell"]
            }
    if self.num_robot == 5:
        for i in range(self.max_x * self.max_y):
            self.cells[i] = {
                "broken": False,
                "painted": False,
                "end": cells[i]["sticker"],
                "blocks": cells[i]["blocks"]
            }

class Pole:
    def __init__(self, screen, textures, settings, cells, robot, vertical_fences, horizontal_fences):
        self.textures = textures
        pygame.init()
        self.screen_resolution = settings["screen_resolution"]
        self.count_of_cells = [settings["max_x"], settings["max_y"]]
        self.cell_size = [settings["screen_resolution"][0] / settings["max_x"],
                          settings["screen_resolution"][1] / settings["max_y"]]
        self.cells = cells
        self.max_x = settings["max_x"]
        # self.needless = []

        self.vertical_fences = vertical_fences
        self.horizontal_fences = horizontal_fences
        self.num_robot = robot
        self.screen = screen
        function_robots.first_field_textures(self)

        self.warning_message = get_image("msg_instruction").convert_alpha()
        self.warning_message = pygame.transform.scale(self.warning_message,
                                                      (3 * self.screen_resolution[0] / 5,
                                                       self.screen_resolution[0] / 5))

        self.robot = robot

    def is_inside(self, x, y):
        return -1 < x < self.count_of_cells[0] and -1 < y < self.count_of_cells[1]

    def warning(self):
        self.screen.blit(self.warning_message,
                         (self.screen_resolution[0] / 5, 2 * self.screen_resolution[1] / 5))

    def make_space(self):
        for x in range(self.count_of_cells[0]):
            for y in range(self.count_of_cells[1]):
                function_robots.rebuild_one_cell(self, self.cells[x + y * self.count_of_cells[0]], x, y)
        function_robots.make_fences(self)


class Game:
    def __init__(self, name_json):
        with open(name_json, "r") as json_file:
            initial_data = json.load(json_file)
        self.array_command = []
        self.textures = {}
        self.name_json = name_json
        self.speed = 550
        settings = initial_data["settings"]
        self.settings = settings
        self.check = 0
        if "max_x" not in settings or "max_y" not in settings or "screen_resolution" not in settings:
            print("Not enough settings")
            self.check = -1
        else:
            self.start_x = 0
            self.start_y = 0
            if "start_x" in settings.keys():
                self.start_x = settings["start_x"]
            if "start_y" in settings.keys():
                self.start_y = settings["start_y"]
            self.num_robot = settings["robot"]
            print("num_robot:", str(self.num_robot))
            pygame.init()
#            if "textures" in initial_data.keys():
#                for texture in self.textures.keys():
#                    if texture in initial_data["textures"].keys():
#                        self.textures[texture] = initial_data["textures"][texture]
            self.screen = pygame.display.set_mode(settings["screen_resolution"])
            self.vertical_fences = []
            if "vertical_fences" in initial_data.keys():
                self.vertical_fences = initial_data["vertical_fences"]
            self.horizontal_fences = []
            if "horizontal_fences" in initial_data.keys():
                self.horizontal_fences = initial_data["horizontal_fences"]
            self.mas_trains = []
            if "mas_trains" in initial_data.keys():
                self.mas_trains = initial_data["mas_trains"]

            self.cells = initial_data["cells"]
            self.pole = Pole(self.screen, self.textures, settings, self.cells, self.num_robot,
                             self.vertical_fences, self.horizontal_fences)
            self.angle = 0
            if "angle" in settings.keys():
                self.angle = settings["angle"]
            self.max_x = settings["max_x"]
            self.max_y = settings["max_y"]

            decode_cells(self, initial_data["cells"])

            if self.num_robot == 0:
                self.robot = function_robots.Vertun(self)
            elif self.num_robot == 1:
                self.robot = function_robots.Dvigun(self)
            elif self.num_robot == 2:
                self.robot = function_robots.Tyagun(self)
            elif self.num_robot == 3:
                self.robot = function_robots.Polzun(self)
            elif self.num_robot == 4:
                self.robot = function_robots.Tolkun(self)
            elif self.num_robot == 5:
                self.robot = function_robots.Train(self)
            self.win_message = get_image("msg_win").convert_alpha()
            self.win_message = pygame.transform.scale(self.win_message, (3 * self.pole.screen_resolution[0] / 5,
                                                                         1.5 * self.pole.screen_resolution[1] / 5))
            self.lose_message = get_image("msg_lose").convert_alpha()
            self.lose_message = pygame.transform.scale(self.lose_message, (3 * self.pole.screen_resolution[0] / 5,
                                                                           1.5 * self.pole.screen_resolution[1] / 5))

    def rotate_left(self):
        self.array_command.append(0)

    def rotate_right(self):
        self.array_command.append(1)

    def draw(self):
        self.array_command.append(2)

    def go(self):
        self.array_command.append(3)

    def pull(self):
        if self.num_robot in [2, 5]:
            self.array_command.append(4)

    def load(self):
        if 3 <= self.num_robot <= 4:
            self.array_command.append(5)

    def unload(self):
        if 3 <= self.num_robot <= 4:
            self.array_command.append(6)

    def link_one(self):
        if self.num_robot == 5:
            self.array_command.append(7)

    def link_all(self):
        if self.num_robot == 5:
            self.array_command.append(8)

    def unlink_one(self):
        if self.num_robot == 5:
            self.array_command.append(9)

    def unlink_all(self):
        if self.num_robot == 5:
            self.array_command.append(10)

    def change_speed(self, speed):
        self.speed = speed

    def main_loop(self):
        if self.check == 0:
            self.pole.make_space()
            function_robots.make_robot(self.robot)
            self.pole.warning()
            pygame.display.update()
            pygame.time.delay(500)
            mode = 0
            while 1:
                for i in pygame.event.get():
                    if i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_1:
                            mode = 1
                        elif i.key == pygame.K_2:
                            mode = 2
                        if i.key == pygame.K_ESCAPE:
                            mode = 3
                if mode != 0:
                    break
            self.pole.make_space()
            function_robots.make_robot(self.robot)
            # self.robot.make_vertun()
            pygame.display.update()
            flag = 0
            end = 1
            if mode != 3:
                for event in self.array_command:
                    start = -1

                    while mode == 2:
                        for i in pygame.event.get():
                            if i.type == pygame.KEYDOWN:
                                if i.key == pygame.K_ESCAPE:
                                    flag = -1
                                    end = 0
                                    start = 0
                                if mode == 2:
                                    if i.key == pygame.K_SPACE:
                                        start = 0
                        if start == 0:
                            break

                    if flag == -1:
                        break
                    if event == 10:
                        self.robot.unlink(True)
                    if event == 9:
                        self.robot.unlink(False)
                    if event == 8:
                        self.robot.link_all()
                    if event == 7:
                        self.robot.link_one()
                    if event == 6:
                        function_robots.unload(self.robot)
                    if event == 5:
                        function_robots.load(self.robot)
                    if event == 4:
                        if self.num_robot == 2:
                            flag = self.robot.pull_block()
                        elif self.num_robot == 5:
                            flag = self.robot.go_with_wagons()
                    if event == 3:
                        if self.num_robot in [1, 4]:
                            # flag = self.robot.go()
                            print("nooooo")
                            flag = function_robots.go2(self.robot)
                        else:
                            flag = function_robots.go(self.robot)
                    if event == 2:
                        self.robot.paint()
                    if event == 1:
                        function_robots.turn_clockwise(self.robot, self.num_robot, 1)  # rotate_right turn_clockwise
                    if event == 0:
                        function_robots.turn_clockwise(self.robot, self.num_robot,
                                                       -1)  # rotate_left turn_counterclockwise
                    pygame.display.update()
                    pygame.time.delay(self.speed)

                # pil_string_image = pygame.image.tostring(self.screen, "RGBA", False)
                # pil_image = Image.frombytes('RGBA', self.settings["screen_resolution"], pil_string_image, 'raw')
                # name_final_img = self.name_json.split('.')[0] + '_final_screen.png'
                # pil_image.save(name_final_img)
                function_robots.make_report(self)
                # self.robot.make_report(self.name_json.split('.')[0])

                while end:
                    for i in pygame.event.get():
                        if i.type == pygame.KEYDOWN:
                            if i.key == pygame.K_ESCAPE:
                                end = 0
                                pygame.quit()
