import pygame
import json
from moscow_robots.data import get_image
import sys


class RobotData:
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


class CellData:
    def __init__(self):
        self.label = ' '

    def __str__(self):
        return self.label

    def decode(self, s):
        self.label = ' '
        for i in range(len(s)):
            c = s[i]
            if c in " 0123456789":
                assert self.label ==  ' '
                self.label = c


class FieldData:
    def __init__(self):
        self.sx = 1
        self.sy = 1
        self.cells = [[CellData() for x in range(self.sx)] for y in range(self.sy)]

    def load(self, d):
        sx = d["sx"]
        sy = d["sy"]
        self.sx = sx
        self.sy = sy
        self.cells = [[CellData() for x in range(sx)] for i in range(sy)]
        cells = d["cells"]
        for y in range(sy):
            for x in range(sx):
                self.cells[y][x].decode(cells[y][x])

class Textures:
    def __init__(self, robot_kind, csize):
        t = get_image("polzun_empty").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        self.robot = pygame.transform.rotate(t, 90)
        t = get_image("polzun_empty_dead").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        self.robot_dead = pygame.transform.rotate(t, 90)

        rsize = (csize[0] * 11 // 10, csize[1] * 11 // 10)

        t = get_image("rug_red").convert_alpha()
        self.robot_dest = pygame.transform.scale(t, rsize)

        self.cells = {}

        t = get_image("rug_green").convert_alpha()
        self.cells[' '] = pygame.transform.scale(t, rsize)

        for i in range(10):
            t = get_image("rug_num" + str(i)).convert_alpha()
            self.cells[str(i)] = pygame.transform.scale(t, rsize)


class GamePolzun:

    def __init__(self, json_name):
        self.direction_vectors = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        self.base_name = "".join(json_name.split(".")[:-1])
        print("base_name", self.base_name)
        with open(json_name, "r") as json_file:
            self.json_data = json.load(json_file)

        self.robot = RobotData()
        self.robot.load(self.json_data["robot"])
        self.robot_kind = self.robot.kind
        rx = self.robot.x
        ry = self.robot.y

        self.field = FieldData()
        self.field.load(self.json_data["field"])
        self.fsize = (self.field.sx, self.field.sy)

        self.tasks = []
        if self.json_data["tasks"]:
            self.tasks = self.json_data["tasks"][::]
        self.ctask = ""
        clabel = self.field.cells[ry][rx].label
        if clabel in "0123456789":
            self.ctask += clabel;

        ssize = (800, 800)
        csize_x = ssize[0] // max(3, self.fsize[0])
        csize_y = ssize[1] // max(2, self.fsize[1])
        csize = min(csize_x, csize_y)
        self.csize = (csize, csize)
        self.ssize = (self.csize[0] * max(3, self.fsize[0]), self.csize[1] * max(2, self.fsize[1]))    

        pygame.display.init()
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.event.set_blocked(pygame.WINDOWMOVED)

        self.screen = pygame.display.set_mode(self.ssize)
        self.textures = Textures(self.robot_kind, self.csize)

        self.speed = 100
        self.game_mode = 0
        self.robot_alive = True
        self.background = None


    def __enter__(self):
        self.robot_alive = True
        self.game_mode = 2 # step by step
        self.finish_step(True, False)
        return self

    def __exit__(self, t, v, tb):
        pygame.image.save(self.screen, self.base_name + ".final.png")
        ok = self.task_complete()
        print("ok:", ok)
        self.game_mode = 2 # step by step
        self.finish_step(True, False, False)
        if not self.robot_alive:
            return True

    def finish_step(self, need_redraw=True, need_wait=True, need_raise=True):
        if need_redraw or not self.robot_alive:
            self.redraw_field()
            self.redraw_robot()
        pygame.display.update()

        if need_wait:
            pygame.time.wait(self.speed)

        flag = ((self.game_mode == 2) or (not self.robot_alive)) and need_raise
        while True:
            pygame.event.pump()
            for ev in pygame.event.get():
                if ev.type == pygame.WINDOWSHOWN:
                    pygame.display.flip()
                    continue
                if ev.type == pygame.QUIT:
                    sys.exit("Closed by user ")
                    flag = False
                    continue
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_TAB:
                        flag = False
                        self.game_mode = 1
                    elif ev.key == pygame.K_SPACE:
                        flag = False
                        self.game_mode = 2
                    continue

            if not flag:
                break
            pygame.time.wait(10)

        if need_raise and not self.robot_alive:
            raise RuntimeError("Robot is dead")


    def task_complete(self):
        if not self.robot_alive:
            return False
        if self.robot.fpos is not None:
            if self.robot.x != self.robot.fpos[0]:
                return False
            if self.robot.y != self.robot.fpos[1]:
                return False

        if not self.tasks:
            return True

        for t in self.tasks:
            if t == self.ctask:
                return True
        return False

    def redraw_field(self):
        self.screen.fill((255, 0, 255)) 
        sx = self.field.sx
        sy = self.field.sy
        cx = self.csize[0]
        cy = self.csize[1]

        for y in range(sy):
            for x in range(sx):
                cell = self.field.cells[y][x]
                t = self.textures.cells[cell.label]
                tsize = t.get_size()
                bx = x * cx + (cx - tsize[0]) // 2
                by = y * cy + (cy - tsize[1]) // 2
                self.screen.blit(t, (bx, by))

        fpos = self.robot.fpos
        if fpos is not None:
            t = self.textures.robot_dest
            tsize = t.get_size()
            bx = fpos[0] * cx + (cx - tsize[0]) // 2
            by = fpos[1] * cy + (cy - tsize[1]) // 2
            self.screen.blit(t, (bx, by))

        self.background = self.screen.copy()

    def redraw_robot(self):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        t = self.textures.robot
        if not self.robot_alive:
            t = self.textures.robot_dead
        t = pygame.transform.rotate(t, -d * 90)
        tsize = t.get_size()
        bx = cx * x + (cx - tsize[0]) // 2
        by = cy * y + (cy - tsize[1]) // 2
        self.screen.blit(t, (bx, by))

    def move_robot(self):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]

        t = self.textures.robot
        t = pygame.transform.rotate(t, - d * 90)
        tsize = t.get_size()
        bx = cx * x + (cx - tsize[0]) // 2
        by = cy * y + (cy - tsize[1]) // 2

        self.redraw_field()
        scopy = self.screen.copy()

        m = 8
        for i in range(m + 1):
            self.screen.blit(scopy, (0, 0))
            dxi, dyi = (cx * dx * i + m // 2) // m, (cy * dy * i + m // 2) // m
            self.screen.blit(t, (bx + dxi, by + dyi))
            pygame.display.update()
            pygame.time.wait(self.speed // (m + 1))
        x += dx
        y += dy
        self.robot.x = x
        self.robot.y = y
        clabel = self.field.cells[y][x].label
        if clabel in "0123456789":
            self.ctask += clabel;

    def rotate_robot(self, dd):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4

        t = self.textures.robot
        t = pygame.transform.rotate(t, - d * 90)

        self.redraw_field()
        scopy = self.screen.copy()

        m = 8
        for i in range(m + 1):
            ti = pygame.transform.rotate(t, -((90 * dd * i + m // 2) // m))
            tsize = ti.get_size()
            self.screen.blit(scopy, (0, 0))
            dbx = (cx - tsize[0]) // 2
            dby = (cy - tsize[1]) // 2
            self.screen.blit(ti, (cx * x + dbx, cy * y + dby))
            pygame.display.update()
            pygame.time.wait(self.speed // (m + 1))
        self.robot.dir = (d + dd) % 4

    def _path_clear(self):
        sx = self.field.sx
        sy = self.field.sy
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]
        x1 = x + dx
        y1 = y + dy
        if (x1 < 0) or (x1 >= sx) or (y1 < 0) or (y1 >= sy):
            return False
        return True


    def _step_forward(self):
        if not self.robot_alive:
            return False
        if not self._path_clear():
            self.robot_alive = False
            return True
        self.move_robot()
        return False

    def _turn_right(self): 
        if not self.robot_alive:
            return False
        self.rotate_robot(1)
        return False
        
    def _turn_left(self): 
        if not self.robot_alive:
            return False
        self.rotate_robot(-1)
        return False

    def path_clear(self):
        ans = self._path_clear()
        self.finish_step(False, True)
        return ans

    def step_forward(self):
        ans = self._step_forward()
        self.finish_step(ans, ans)

    def turn_right(self): 
        ans = self._turn_right()
        self.finish_step(ans, ans)

    def turn_left(self): 
        ans = self._turn_left()
        self.finish_step(ans, ans)

