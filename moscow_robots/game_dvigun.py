import pygame
from moscow_robots.data import get_image
from moscow_robots.game_robot import GameRobot


class DvigunCellData:
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


class DvigunFieldData:
    def __init__(self):
        self.sx = 1
        self.sy = 1
        self.cells = [[DvigunCellData() for x in range(self.sx)] for y in range(self.sy)]
        self.hfences = [[0 for x in range(self.sx)] for y in range(self.sy - 1)]
        self.vfences = [[0 for x in range(self.sx - 1)] for y in range(self.sy)]

    def load_cells(self, d):
        sx, sy = self.sx, self.sy
        self.cells = [[DvigunCellData() for x in range(sx)] for i in range(sy)]
        cells = d["cells"]
        for y in range(sy):
            for x in range(sx):
                self.cells[y][x].decode(cells[y][x])

    def export_cells(self):
        cs = [[str(self.cells[y][x]) for x in range(self.sx)] for y in range(self.sy)]
        return cs


    def load_fences(self, d):
        sx, sy = self.sx, self.sy
        self.hfences = [[0 for x in range(sx)] for y in range(sy - 1)]
        self.vfences = [[0 for x in range(sx - 1)] for y in range(sy)]
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

    def export_fences(self):
        sx, sy = self.sx, self.sy
        hfs = ["".join([" -"[self.hfences[y][x]] for x in range(sx)]) for y in range(sy - 1)]
        vfs = ["".join([" |"[self.vfences[y][x]] for x in range(sx - 1)]) for y in range(sy)]
        return hfs, vfs

    def load(self, d):
        self.sx = d["sx"]
        self.sy = d["sy"]
        self.load_cells(d)
        self.load_fences(d)

    def export(self):
        res = dict()
        res["sx"] = self.sx
        res["sy"] = self.sy
        cs = self.export_cells()
        if cs:
            res["cells"] = cs
        hfs, vfs = self.export_fences()
        if hfs:
            res["hfences"] = hfs
        if vfs:
            res["vfences"] = vfs
        return res

class DvigunTextures:
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
        self.blocks.append(pygame.transform.scale(t, (csize[0] * 3 // 5, csize[1] * 3 // 5)))
        t = get_image("block_circle").convert_alpha()
        self.blocks.append(pygame.transform.scale(t, (csize[0] * 2 // 3, csize[1] * 2 // 3)))

        t = get_image("wall_hor").convert()
        self.hwall = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] // 10))
        t = get_image("wall_vert").convert()
        self.vwall = pygame.transform.scale(t, (csize[0] // 10, csize[1] * 4 // 5))


class GameDvigun(GameRobot):

    def __init__(self, json_name):
        GameRobot.__init__(self, json_name)

        self.field = DvigunFieldData()
        self.field.load(self.json_data["field"])

        self.textures = DvigunTextures(self.robot_kind, self.csize)

    def redraw_all(self):
        self.redraw_field()
        self.redraw_blocks()
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
                t = self.textures.fields[cell.bdest]
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

    def redraw_blocks(self):
        cx = self.csize[0]
        cy = self.csize[1]
        for y in range(self.field.sy):
            for x in range(self.field.sx):
                block = self.field.cells[y][x].block
                if block:
                    t = self.textures.blocks[block]
                    ax = (cx - t.get_width()) // 2
                    ay = (cy - t.get_height()) // 2
                    bx = cx * x + ax
                    by = cy * y + ay
                    self.screen.blit(t, (bx, by))
        pass
                    
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
        
        ax = (cx - t.get_width()) // 2
        ay = (cy - t.get_height()) // 2
        bx = cx * x + ax
        by = cy * y + ay
        self.screen.blit(t, (bx, by))

    def move_robot(self, k):  # with k blocks ahead
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]

        blocks = [0 for i in range(k)]
        for i in range(k):
            xi, yi = x + dx * (i + 1), y + dy * (i + 1)
            blocks[i] = self.field.cells[yi][xi].block
            assert blocks[i]
            self.field.cells[yi][xi].block = 0

        ts = []
        ts.append(pygame.transform.rotate(self.textures.robot, ((4 - d) % 4) * 90))
        for i in range(k):
            ts.append(self.textures.blocks[blocks[i]])

        self.redraw_field()
        self.redraw_blocks()
        scopy = self.screen.copy()

        m = 8
        for i in range(m + 1):
            self.screen.blit(scopy, (0, 0))
            dxi, dyi = dx * (cx * i // m), dy * (cy * i // m)
            for j in range(k + 1):
                ax = (cx - ts[j].get_width()) // 2
                ay = (cy - ts[j].get_height()) // 2
                bx = cx * (x + j * dx) + ax + dxi
                by = cy * (y + j * dy) + ay + dyi
                self.screen.blit(ts[j], (bx, by))
            
            pygame.display.update()
            pygame.time.wait(self.game_speed // (m + 1))

        for i in range(k):
            xi, yi = x + dx * (i + 2), y + dy * (i + 2)
            self.field.cells[yi][xi].block = blocks[i]
        self.robot.x += dx
        self.robot.y += dy

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
        self.redraw_blocks()
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

    def _can_pass(self, pos, d):
        sx = self.field.sx
        sy = self.field.sy
        x0, y0 = pos
        if not (0 <= x0 < sx):
            return (False, None)
        if not (0 <= y0 < sy):
            return (False, None)

        dx, dy = self.direction_vectors[d % 4]
        x1 = x0 + dx
        y1 = y0 + dy
        if not (0 <= x1 < sx):
            return (False, None)
        if not (0 <= y1 < sy):
            return (False, None)

        if dx and self.field.vfences[y0][min(x0, x1)]:
            return (False, None)
        if dy and self.field.hfences[min(y0, y1)][x0]:
            return (False, None)
        return (True, self.field.cells[y1][x1].block)

    def _can_move(self, k):
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]
        for i in range(0, k + 1):
            ok, block = self._can_pass((x + i * dx, y + i * dy), d)
            if not ok:
                return -1
            if not block:
                return i
        return -1

    def _path_clear(self):
        ok, block = self._can_pass((self.robot.x, self.robot.y), self.robot.dir)
        return ok and not block

    def _step_forward(self):
        if not self.robot_alive:
            return False
        k = self._can_move(2)
        if k < 0:
            self.robot_alive = False
            return True

        self.move_robot(k)
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

    def can_move(self):
        k = self._can_move(2)
        ans = (k >= 0)
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

