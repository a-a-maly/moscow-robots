import pygame
from moscow_robots.data import get_image
from moscow_robots.game_robot import GameRobot

class CellData:
    def __init__(self):
        self.broken = False
        self.painted = False
        self.t = 0

    def __str__(self):
        res = ""
        if self.broken:
            res += "b"
        if self.painted:
            res += "p"
        if self.t:
            res += "t" + str(int(self.t))
        return res

    def decode(self, s):
        self.broken = False
        self.painted = False
        self.t = 0
        for i in range(len(s)):
            c = s[i]
            if c == 'b':
                self.broken = True
            elif c == 'p':
                self.painted = True
            elif c == ' t':
                self.t = int(s[i+1:].strip())
                break;


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
            for y in range(min(sy, len(vfences))):
                for x in range(min(sx - 1, len(vfences[y]))):
                    self.vfences[y][x] = (vfences[y][x] not in ' 0')
        hfences = d.get("hfences")
        if hfences:
            for y in range(min(sy - 1, len(hfences))):
                for x in range(min(sx, len(hfences[y]))):
                    self.hfences[y][x] = (hfences[y][x] not in ' 0')

class Textures:
    def __init__(self, robot_kind, csize):
        t = get_image("vertun").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        self.robot = pygame.transform.rotate(t, 90)
        t = get_image("vertun_dead").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        self.robot_dead = pygame.transform.rotate(t, 90)

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


class GameVertun(GameRobot):

    def __init__(self, json_name):
        GameRobot.__init__(self, json_name)

        self.field = FieldData()
        self.field.load(self.json_data["field"])

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

        for y in range(self.field.sy):
            for x in range(self.field.sx):
                if self.field.cells[y][x].broken != self.field.cells[y][x].painted:
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
        t = pygame.transform.rotate(t, ((4 - d) % 4) * 90)

        self.redraw_field()
        scopy = self.screen.copy()

        m = 8
        for i in range(m + 1):
            self.screen.blit(scopy, (0, 0))
            dxi, dyi = dx * i // m, dy * i // m
            bx = cx * x + cx // 10 + dxi
            by = cy * y + cy // 10 + dyi
            self.screen.blit(t, (bx, by))
            pygame.display.update()
            pygame.time.wait(self.game_speed // (m + 1))


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

        m = 8
        for i in range(m + 1):
            ti = pygame.transform.rotate(t, -90 * dd * i // m)
            tsize = ti.get_size()
            self.screen.blit(scopy, (0, 0))
            dbx = (cx - tsize[0]) // 2
            dby = (cy - tsize[1]) // 2
            self.screen.blit(ti, (bx + dbx, by + dby))
            pygame.display.update()
            pygame.time.wait(self.game_speed // (m + 1))


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
        if dx and self.field.vfences[y][min(x, x1)]:
            return False
        if dy and self.field.hfences[min(y, y1)][x]:
            return False
        return True

    def _cell_normal(self):
        c = self.field.cells[self.robot.y][self.robot.x]
        return not c.broken

    def _cell_broken(self):
        c = self.field.cells[self.robot.y][self.robot.x]
        return c.broken and not c.painted

    def _cell_fixed(self):
        c = self.field.cells[self.robot.y][self.robot.x]
        return c.painted

    def _fix_cell(self):
        if not self.robot_alive:
            return False
        self.field.cells[self.robot.y][self.robot.x].painted = 1
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

    def cell_normal(self):
        ans = self._cell_normal()
        self.finish_step(False, True)
        return ans

    def cell_broken(self):
        ans = self._cell_broken()
        self.finish_step(False, True)
        return ans

    def cell_fixed(self):
        ans = self._cell_fixed()
        self.finish_step(False, True)
        return ans

    def fix_cell(self):
        ans = self._fix_cell()
        self.finish_step(ans, True)

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

