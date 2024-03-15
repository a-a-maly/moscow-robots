import pygame
import json
from moscow_robots.data import get_image


class Robot:
    def __init__(self):
        self.kind = 0
        self.x = 0
        self.y = 0
        self.dir = 0
        self.fpos = None
        
    def load(self, d):
        self.kind = d["kind"]
        self.x = d["x"]
        self.y = d["y"]
        self.dir = d["dir"]
        self.fpos = d.get("fpos")

class Cell:
    def __init__(self):
        self.broken = False
        self.painted = False

class Field:
    def __init__(self):
        self.sx = 1
        self.sy = 1
        self.cells = [[Cell() for x in range(self.sx)] for y in range(self.sy)]
        self.hfences = [[0 for x in range(self.sx)] for y in range(self.sy - 1)]
        self.vfences = [[0 for x in range(self.sx - 1)] for y in range(self.sy)]

    def load(self, d):
        sx = d["sx"]
        sy = d["sy"]
        self.sx = sx
        self.sy = sy
        self.cells = [[Cell() for x in range(sx)] for i in range(sy)]
        self.hfences = [[0 for x in range(sx)] for y in range(sy - 1)]
        self.vfences = [[0 for x in range(sx - 1)] for y in range(sy)]
        _cells = d["cells"]
        for y in range(sy):
            for x in range(sx):
                self.cells[y][x].broken = _cells[y][x].get("broken", 0) 
                self.cells[y][x].painted = _cells[y][x].get("painted", 0) 
        _vfences = d.get("vfences")
        if _vfences:
            for y in range(sy):
                for x in range(sx - 1):
                    self.vfences[y][x] = _vfences[y][x]
        _hfences = d.get("hfences")
        if _hfences:
            for y in range(sy - 1):
                for x in range(sx):
                    self.hfences[y][x] = _hfences[y][x]

class Textures:
    def __init__(self, robot_kind, csize):
        t = get_image("vertun").convert_alpha()
        self.robot = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        t = get_image("vertun_dead").convert_alpha()
        self.robot_dead = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        t = get_image("robot_dest").convert_alpha()
        self.robot_dest = pygame.transform.scale(t, csize)

        t = get_image("field_normal").convert_alpha()
        self.field_normal = pygame.transform.scale(t, csize)
        t = get_image("field_normal_painted").convert_alpha()
        self.field_normal_painted = pygame.transform.scale(t, csize)
        t = get_image("field_broken").convert_alpha()
        self.field_broken = pygame.transform.scale(t, csize)
        t = get_image("field_broken_painted").convert_alpha()
        self.field_broken_painted = pygame.transform.scale(t, csize)

        t = get_image("wall_hor").convert()
        self.hwall = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] // 10))
        t = get_image("wall_vert").convert()
        self.vwall = pygame.transform.scale(t, (csize[0] // 10, csize[1] * 4 // 5))

        t = get_image("msg_instruction").convert_alpha()
        self.msg_intro = pygame.transform.scale(t, (3 * csize[0], csize[1]))
        t = get_image("msg_win").convert_alpha()
        self.msg_win = pygame.transform.scale(t, (3 * csize[0], 3 * csize[1] // 2))
        t = get_image("msg_lose").convert_alpha()
        self.msg_lose = pygame.transform.scale(t, (3 * csize[0], 3 * csize[1] // 2))


class GameRobot:
    def __init__(self, json_name):
        self.base_name = json_name.split(".")[:-1]
        with open(json_name, "r") as json_file:
            self.json_data = json.load(json_file)

        self.robot = Robot()
        self.robot.load(self.json_data["robot"])
        self.robot_kind = self.robot.kind

        self.field = Field()
        self.field.load(self.json_data["field"])
        self.fsize = (self.field.sx, self.field.sy)

        ssize = (800, 800)
        csize_x = ssize[0] // max(3, self.fsize[0])
        csize_y = ssize[1] // max(2, self.fsize[1])
        csize = min(csize_x, csize_y)
        self.csize = (csize, csize)
        self.ssize = (self.csize[0] * max(3, self.fsize[0]), self.csize[1] * max(2, self.fsize[1]))    
   
        pygame.init()
        self.screen = pygame.display.set_mode(self.ssize)
        self.textures = Textures(self.robot_kind, self.csize)

        self.speed = 500
        self.game_mode = 0
        self.robot_alive = True
        self.background = None


    def __enter__(self):
        self.robot_alive = True
        self.game_mode = 0
        self.redraw_field()
        self.redraw_robot()
        #self.screen.blit(self.textures.msg_intro, self.csize)
        pygame.display.update() 
  
        while self.game_mode == 0:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_1:
                        self.game_mode = 1
                    elif ev.key == pygame.K_2:
                        self.game_mode = 2
                    elif ev.key == pygame.K_ESCAPE:
                        self.game_mode = 3

    def __exit__(self, t, v, tb):
        self.game_mode = 4

    def redraw_field(self):
        self.screen.fill((255, 0, 255)) 
        sx = self.field.sx
        sy = self.field.sy
        cx = self.csize[0]
        cy = self.csize[1]

        for y in range(sy):
            for x in range(sx):
                cell = self.field.cells[y][x]
                t = None
                if cell.broken:
                    if cell.painted: t = self.textures.field_broken_painted
                    else: t = self.textures.field_broken
                else: # normal
                    if cell.painted: t = self.textures.field_normal_painted
                    else: t = self.textures.field_normal
                self.screen.blit(t, (x * cx, y * cy))

        t = self.textures.vwall
        for y in range(sy): # vertical fences
            for x in range(sx - 1):
                if self.field.vfences[y][x]:
                    bx = cx * (x + 1) - cx // 20
                    by = cy * y + cy // 10
                    self.screen.blit(t, (bx, by))

        t = self.textures.hwall
        for y in range(sy - 1): # horizontal fences
            for x in range(sx):
                if self.field.hfences[y][x]:
                    bx = cx * x + cx // 10
                    by = cy * (y + 1) - cy // 20
                    self.screen.blit(t, (bx, by))
        fpos = self.robot.fpos
        if fpos is not None:
            t = self.textures.robot_dest
            bx = fpos[0] * cx
            by = fpos[1] * cy
            self.screen.blit(t, (bx, by))

        self.background = self.screen.copy()

    def redraw_robot(self):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = (5 - self.robot.dir) % 4
        t = self.textures.robot
        if not self.robot_alive:
            t = self.textures.robot_dead
        t = pygame.transform.rotate(t, d * 90)
        bx = cx * x + cx // 10
        by = cy * y + cy // 10
        self.screen.blit(t, (bx, by))

