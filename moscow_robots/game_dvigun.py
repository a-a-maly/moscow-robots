import pygame
import json
from moscow_robots.data import get_image
from moscow_robots.game_vertun import RobotData
import sys


class CellData:
    def __init__(self):
        self.block = 0
        self.bdest = 0

    def __str__(self):
        res = ""
        if self.block == 1:
            res += "x"
        elif self.block == 2:
            res += "o"
        if self.bdest & 1:
            res += "X"
        if self.bdest & 2:
            res += "O"
        return res

    def decode(self, s):
        self.block = 0
        self.bdest = 0
        for i in range(len(s)):
            c = s[i]
            if c == 'x':
                assert self.block == 0
                self.block = 1
            elif c == 'o':
                assert self.block == 0
                self.block = 2
            elif c == 'X':
                self.bdest |= 1
            elif c == 'O':
                self.bdest |= 2


class FieldData:
    def __init__(self):
        self.sx = 1
        self.sy = 1
        self.cells = [[CellData() for x in range(self.sx)] for y in range(self.sy)]
        self.hfences = [[0 for x in range(self.sx)] for y in range(self.sy - 1)]
        self.vfences = [[0 for x in range(self.sx - 1)] for y in range(self.sy)]

    def load(self, d):
        sx = d["sx"]
        sy = d["sy"]
        self.sx = sx
        self.sy = sy
        self.cells = [[CellData() for x in range(sx)] for i in range(sy)]
        self.hfences = [[0 for x in range(sx)] for y in range(sy - 1)]
        self.vfences = [[0 for x in range(sx - 1)] for y in range(sy)]
        cells = d["cells"]
        for y in range(sy):
            for x in range(sx):
                self.cells[y][x].decode(cells[y][x])
        vfences = d.get("vfences")
        if vfences:
            for y in range(sy):
                for x in range(sx - 1):
                    self.vfences[y][x] = vfences[y][x]
        hfences = d.get("hfences")
        if hfences:
            for y in range(sy - 1):
                for x in range(sx):
                    self.hfences[y][x] = hfences[y][x]

class Textures:
    def __init__(self, robot_kind, csize):
        t = get_image("dvigun").convert_alpha()
        self.robot = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        t = get_image("dvigun_dead").convert_alpha()
        self.robot_dead = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        t = get_image("robot_dest").convert_alpha()
        self.robot_dest = pygame.transform.scale(t, csize)

        self.fields = []
        t = get_image("field_normal_other").convert_alpha()
        self.fields.append(pygame.transform.scale(t, csize))
        t = get_image("block_square_dest").convert_alpha()
        self.fields.append(pygame.transform.scale(t, csize))
        t = get_image("block_circle_dest").convert_alpha()
        self.fields.append(pygame.transform.scale(t, csize))
        t = get_image("block_any_dest").convert_alpha()
        self.fields.append(pygame.transform.scale(t, csize))

        self.blocks = [None]
        t = get_image("block_square").convert_alpha()
        self.blocks.append(pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        t = get_image("block_circle").convert_alpha()
        self.blocks.append(pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))

        t = get_image("wall_hor").convert()
        self.hwall = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] // 10))
        t = get_image("wall_vert").convert()
        self.vwall = pygame.transform.scale(t, (csize[0] // 10, csize[1] * 4 // 5))


class GameDvigun:

    def __init__(self, json_name):
        self.direction_vectors = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        self.base_name = "".join(json_name.split(".")[:-1])
        print("base_name", self.base_name)
        with open(json_name, "r") as json_file:
            self.json_data = json.load(json_file)

        self.robot = RobotData()
        self.robot.load(self.json_data["robot"])
        self.robot_kind = self.robot.kind

        self.field = FieldData()
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

        self.speed = 100
        self.game_mode = 0
        self.robot_alive = True


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
        #print("t", t)
        #print("v", v)
        #print("tb", tb)
        if not self.robot_alive:
            #print(type(v), len(v))
            return True

    def task_complete(self):
        if not self.robot_alive:
            return False
        if self.robot.fpos is not None:
            if self.robot.x != self.robot.fpos[0]:
                return False
            if self.robot.y != self.robot.fpos[1]:
                return False

        for y in range(self.field.sy):
            for x in range(self.field.sx):
                c = self.field.cells[y][x]
                if c.block & ~c.bdest:
                    return False
        return True

    def redraw_field(self):
        self.screen.fill((255, 0, 255)) 
        sx = self.field.sx
        sy = self.field.sy
        cx = self.csize[0]
        cy = self.csize[1]

        for y in range(sy):
            for x in range(sx):
                cell = self.field.cells[y][x]
                t = self.textures.fields[cell.target]
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

    def redraw_robot(self):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = (4 - self.robot.dir) % 4
        t = self.textures.robot
        if not self.robot_alive:
            t = self.textures.robot_dead
        t = pygame.transform.rotate(t, d * 90)
        
        bx = cx * x + cx // 10
        by = cy * y + cy // 10
        self.screen.blit(t, (bx, by))

    def move_robot(self):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]
        dx, dy = dx * cx, dy * cy


        t = self.textures.robot
        t = pygame.transform.rotate(t, ((5 - d) % 4) * 90)

        self.redraw_field()
        scopy = self.screen.copy()

        m = 4
        for i in range(m + 1):
            self.screen.blit(scopy, (0, 0))
            dxi, dyi = dx * i // m, dy * i // m
            bx = cx * x + cx // 10 + dxi
            by = cy * y + cy // 10 + dyi
            self.screen.blit(t, (bx, by))
            pygame.display.update()
            pygame.time.wait(self.speed // (m + 1))

    def rotate_robot(self, dd):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4

        bx = cx * x
        by = cy * y

        t = self.textures.robot
        t = pygame.transform.rotate(t, ((4 - d) % 4) * 90)

        self.redraw_field()
        scopy = self.screen.copy()

        m = 4
        for i in range(m + 1):
            ti = pygame.transform.rotate(t, -90 * dd * i // m)
            tsize = ti.get_size()
            self.screen.blit(scopy, (0, 0))
            dbx = (cx - tsize[0]) // 2
            dby = (cy - tsize[1]) // 2
            self.screen.blit(ti, (bx + dbx, by + dby))
            pygame.display.update()
            pygame.time.wait(self.speed // (m + 1))

    def finish_step(self, need_redraw=True, need_wait=True, need_raise=True):
        if need_redraw or not self.robot_alive:
            self.redraw_field()
            self.redraw_robot()
        pygame.display.update()

        if need_wait:
            pygame.time.wait(self.speed)

        flag = ((self.game_mode == 2) or (not self.robot_alive)) and need_raise
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit("Closed by user ")
                    flag = False
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_TAB:
                        flag = False
                        self.game_mode = 1
                    elif ev.key == pygame.K_SPACE:
                        flag = False
                        self.game_mode = 2
            if not flag:
                break
        if need_raise and not self.robot_alive:
            raise RuntimeError("Robot is dead")


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
        if self.cells[y1][x1].block:
            return False
        if dx > 0 and self.field.vfences[y][x]:
            return False
        if dx < 0 and self.field.vfences[y][x - 1]:
            return Flase
        if dy > 0 and self.field.hfences[y][x]:
            return False
        if dy < 0 and self.field.hfences[y - 1][x]:
            return False
        return True

    def _step_forward(self):
        if not self.robot_alive:
            return False
        if not self._path_clear():
            self.robot_alive = False
            return True
        self.move_robot()
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]
        self.robot.x += dx
        self.robot.y += dy
        return False

    def _turn_right(self): 
        if not self.robot_alive:
            return False
        self.rotate_robot(1)
        d = (self.robot.dir + 1) % 4
        self.robot.dir = d
        return False
        
    def _turn_left(self): 
        if not self.robot_alive:
            return False
        self.rotate_robot(-1)
        d = (self.robot.dir + 3) % 4
        self.robot.dir = d
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

