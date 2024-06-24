import pygame
from moscow_robots.data import get_image
from moscow_robots.game_robot import GameRobot


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


class GamePolzun(GameRobot):

    def __init__(self, json_name):
        GameRobot.__init__(self, json_name)

        self.field = FieldData()
        self.field.load(self.json_data["field"])

        self.tasks = []
        if self.json_data["tasks"]:
            self.tasks = self.json_data["tasks"][::]
        self.ctask = ""
        clabel = self.field.cells[self.robot.y][self.robot.x].label
        if clabel in "0123456789":
            self.ctask += clabel;

        self.textures = Textures(self.robot_kind, self.csize)


    def redraw_all(self):
        self.redraw_field()
        self.redraw_robot()

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
            pygame.time.wait(self.game_speed // (m + 1))
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
            pygame.time.wait(self.game_speed // (m + 1))
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

