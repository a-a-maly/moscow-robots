import pygame
from moscow_robots.data import get_image
from moscow_robots.game_robot import GameRobot


class CellData:
    def __init__(self):
        self.block = 0
        self.bdest = 0
        self.gear = 0

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


class GearData:
    def __init__(self):
        self.edges = [None, None]
        self.dirs = []

    def reverse(self):
        self.edges[0], self.edges[1] = self.edges[1], self.edges[0]
        self.dirs[:] = [x ^ 2 for x in self.dirs[::-1]]

    def export(self):
        res = dict()
        res["edges"] = self.edges[:]
        res["dirs"] = self.dirs[:]
        return res


class FieldData:
    def __init__(self):
        self.sx = 1
        self.sy = 1
        self.cells = [[CellData() for x in range(self.sx)] for y in range(self.sy)]
        self.hfences = [[0 for x in range(self.sx)] for y in range(self.sy - 1)]
        self.vfences = [[0 for x in range(self.sx - 1)] for y in range(self.sy)]
        self.gears = []


    def load_fences(self, d):
        self.hfences = [[0 for x in range(self.sx)] for y in range(self.sy - 1)]
        self.vfences = [[0 for x in range(self.sx - 1)] for y in range(self.sy)]
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

    def load_gears(self, d, r):
        sx = self.sx
        sy = self.sy

        ngears = 0
        gmap = [[None for x in range(self.sx)] for y in range(self.sy)] 
        gears = d.get("gears")
        if gears:
            ngears = len(gears)
            for i in range(ngears):
                gi = gears[i]
                gdi = GearData()
                x, y = gi["head"]
                assert 0 <= x < sx
                assert 0 <= y < sy
                assert gmap[y][x] is None 
                hblock = self.cells[y][x].block
                assert (hblock > 0) or (x == r.x and y == r.y)
                gmap[y][x] = i
                gdi.edges[0] = (x, y)
                for c in gi["dirs"]:
                    ci = int(ci)
                    assert 0 <= ci < 4
                    assert self._can_pass((x, y), ci)
                    dx, dy = GameRobot.direction_vectors[ci]
                    x += dx
                    y += dy
                    assert 0 <= x < sx
                    assert 0 <= y < sy
                    assert gmap[y][x] is None 
                    hblock = self.cells[y][x].block
                    assert (hblock > 0) or (x == r.x and y == r.y)
                    gmap[y][x] = i
                    gdi.dirs.append(ci)
                gdi.edges[1] = (x, y)
                self.gears.append(gdi)

        for y in range(sy):
            for x in range(sx):
                if gmap[y][x] is None:
                    if (self.cells[y][x].block > 0) or (x == r.x and y == r.y):
                        gmap[y][x] = ngears
                        ngears += 1
                        gdi = GearData()
                        gdi.edges[0] = (x, y)
                        gdi.edges[1] = (x, y)
                        self.gears.append(gdi)

        ri = gmap[r.y][r.x]
        assert ri is not None
        # robot's gear should always have number 0
        self.gears[0], self.gears[ri] = self.gears[ri], self.gears[0]
        g0 = self.gears[0]
        
        if not (r.x == g0.edges[0][0] and r.y == g0.edges[0][1]):
            assert (r.x == g0.edges[1][0] and r.y == g0.edges[1][1])
            # robot should always be the head of its gear
            g0.reverse()
            # robot should not see its first load
            assert (len(g0.dirs) == 0) or (r.dir != g0.dirs[0])

    def dump_gears(self):
        gs = self.gears
        for i in range(len(gs)):
            print(i, gs[i].edges, gs[i].dirs)


    def load(self, d, r):
        self.sx = d["sx"]
        self.sy = d["sy"]
        self.cells = [[CellData() for x in range(self.sx)] for i in range(self.sy)]
        cells = d["cells"]
        for y in range(self.sy):
            for x in range(self.sx):
                self.cells[y][x].decode(cells[y][x])

        assert self.cells[r.y][r.x].block == 0

        self.load_fences(d)
        self.load_gears(d, r)

    def export_cells(self):
        cs = [[str(self.cells[y][x]) for x in range(self.sx)] for y in range(self.sy)]
        return cs

    def export_fences(self):
        hfs = ["".join([" -"[self.hfences[y][x]] for x in range(self.sx)]) for y in range(self.sy - 1)]
        vfs = ["".join([" |"[self.vfences[y][x]] for x in range(self.sx - 1)]) for y in range(self.sy)]
        return hfs, vfs

    def export_gears(self):
        res = list()
        for g in self.gears:
            if g.dirs:
                res.append(g.export())
        return res

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
        gs = self.export_gears()
        if gs:
            res["gears"] = gs
        return res


    def _can_pass(self, pos, d):
        sx = self.sx
        sy = self.sy
        x0, y0 = pos
        if not (0 <= x0 < sx):
            return False
        if not (0 <= y0 < sy):
            return False
        dx, dy = GameRobot.direction_vectors[d % 4]
        x1 = x0 + dx
        y1 = y0 + dy
        if not (0 <= x1 < sx):
            return False
        if not (0 <= y1 < sy):
            return False

        if dx and self.vfences[y0][min(x0, x1)]:
            return False
        if dy and self.hfences[min(y0, y1)][x0]:
            return False
        return True

    def can_pass(self, pos, d):
        if not self._can_pass(pos, d):
            return False
        x, y = pos
        dx, dy = GameRobot.direction_vectors[d % 4]
        return self.cells[y + dy][x + dx].block == 0


class Textures:
    def __init__(self, robot_kind, csize):
        t = get_image("train").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        self.robot = pygame.transform.rotate(t, 90)

        t = get_image("train_dead").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        self.robot_dead = pygame.transform.rotate(t, 90)

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

        t = get_image("wall_hor").convert_alpha()
        self.hwall = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] // 10))
        t = get_image("wall_vert").convert_alpha()
        self.vwall = pygame.transform.scale(t, (csize[0] // 10, csize[1] * 4 // 5))

        t = get_image("scepka").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 3 // 5, csize[1] // 5))
        self.gear = pygame.transform.rotate(t, 90)


class GameTrain(GameRobot):

    def __init__(self, json_name):
        GameRobot.__init__(self, json_name)

        self.field = FieldData()
        self.field.load(self.json_data["field"], self.robot)

        self.textures = Textures(self.robot_kind, self.csize)


    def redraw_all(self):
        self.redraw_field()
        self.redraw_blocks()
        self.redraw_robot()
        self.redraw_gears()


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
        d = self.robot.dir % 4
        t = self.textures.robot
        if not self.robot_alive:
            t = self.textures.robot_dead
        t = pygame.transform.rotate(t, -d * 90)
        
        ax = (cx - t.get_width()) // 2
        ay = (cy - t.get_height()) // 2
        bx = cx * x + ax
        by = cy * y + ay
        self.screen.blit(t, (bx, by))

    def redraw_gears(self):
        cx = self.csize[0]
        cy = self.csize[1]
        for g in self.field.gears:
            x, y = g.edges[0]
            for d in g.dirs:
                dx, dy = self.direction_vectors[d]
                t = pygame.transform.rotate(self.textures.gear, -90 * d)
                ax = (cx * (1 + dx) - t.get_width()) // 2
                ay = (cx * (1 + dy) - t.get_height()) // 2
                self.screen.blit(t, (cx * x + ax, cy * y + ay))
                x += dx
                y += dy


    def move_robot(self):
        cx = self.csize[0]
        cy = self.csize[1]
        rx = self.robot.x
        ry = self.robot.y
        rd = self.robot.dir % 4
        rdx, rdy = self.direction_vectors[rd]

        g0 = self.field.gears[0]
        #print((rx, ry), g0.edges[0])
        assert ((rx, ry) == g0.edges[0])
        px, py = rx + rdx, ry + rdy

        self.robot.x, self.robot.y = px, py
        g0.edges[0] = (px, py)
        d = rd ^ 2
        x, y = rx, ry
        for i in range(len(g0.dirs)):
            od = g0.dirs[i]
            ox, oy = GameRobot.next_pos((x, y), od)
            self.field.cells[y][x].block = self.field.cells[oy][ox].block
            #self.field.cells[oy][ox].block = 0
            g0.dirs[i] = d
            d = od
            px, py = x, y
            x, y = ox, oy
        self.field.cells[y][x].block = 0
        g0.edges[1] = (px, py)


    def rotate_robot(self, dd):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4

        bx = cx * x
        by = cy * y

        t = self.textures.robot
        t = pygame.transform.rotate(t, -d * 90)

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
            self.redraw_gears()
            pygame.display.update()
            pygame.time.wait(self.game_speed // (m + 1))

        d = (d + dd) % 4
        self.robot.dir = d
        g0 = self.field.gears[0]
        if g0.dirs and (d == g0.dirs[0]):
            self._drop_tail()

    def _has_to_drop(self):
        g0 = self.field.gears[0]
        return len(g0.dirs) > 0

    def _drop_one(self):
        if not self.robot_alive:
            return False
        g0 = self.field.gears[0]
        l0 = len(g0.dirs)
        if l0 == 0:
            self.robot_alive = False
            return True

        g1 = GearData()
        g1.edges[0] = g0.edges[1]
        g1.edges[1] = g0.edges[1]
        g0.edges[1] = GameRobot.prev_pos(g0.edges[1], g0.dirs[-1])
        g0.dirs.pop()
        self.field.gears.append(g1)

        return True

    def _drop_all(self):
        if not self.robot_alive:
            return False
        while self._has_to_drop():
            self._drop_one()
        return True

    def _drop_tail(self):
        if not self.robot_alive:
            return False
        g0 = self.field.gears[0]
        l0 = len(g0.dirs)
        if l0 == 0:
            return False

        g1 = GearData()
        g1.edges[0] = GameRobot.next_pos(g0.edges[0], g0.dirs[0])
        g1.edges[1] = g0.edges[1]
        g1.dirs[:] = g0.dirs[1:]
        g0.edges[1] = g0.edges[0]
        g0.dirs.clear()
        self.field.gears.append(g1)

        return True

    def _has_to_add(self):
        gs = self.field.gears
        g0 = gs[0]
        l0 = len(g0.dirs)
        d = (self.robot.dir % 4) ^ 2
        (x, y) = g0.edges[1]
        if l0 > 0:
            d = g0.dirs[-1]
        #print(l0, (x, y), d)

        for dd in [0, -1, 1]:
            d1 = (d + dd) % 4
            if not self.field._can_pass((x, y), d1):
                continue
            (x1, y1) = GameRobot.next_pos((x, y), d1)
            #print(dd, d1, (x1, y1))

            for i in range(1, len(gs)):
                #print(i)
                gi = self.field.gears[i]
                for k in range(2):
                    if gi.edges[k] == (x1, y1):
                        return (i, d1, k)

        return (0, 0, 0)

    def _add_one(self):
        if not self.robot_alive:
            return False
        h, dh, eh = self._has_to_add()
        #print(h, dh, eh)
        if h == 0:
            self.robot_alive = False
            return True
        gs = self.field.gears
        g0 = gs[0]
        g1 = gs[h]
        if eh:
            g1.reverse()
        assert GameRobot.next_pos(g0.edges[1], dh) == g1.edges[0] 
        g0.edges[1] = g1.edges[1]
        g0.dirs.append(dh)
        g0.dirs.extend(g1.dirs)
        gs[h], gs[-1] = gs[-1], gs[h]
        gs.pop()
        return True

    def _add_all(self):
        if not self.robot_alive:
            return False
        res = False
        while self._has_to_add()[0]:
            self._add_one()
            res = True
        return res


    def _path_clear(self):
        return self.field.can_pass((self.robot.x, self.robot.y), self.robot.dir)

    def _step_forward(self):
        if not self.robot_alive:
            return False
        if not self._path_clear():
            self.robot_alive = False
            return True
        self._drop_tail()
        self.move_robot()
        return True

    def _tow(self):
        if not self.robot_alive:
            return False
        if not self._path_clear():
            self.robot_alive = False
            return True
        if not self._has_to_drop():
            self.robot_alive = False
            return True

        self.move_robot()
        return True

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

    def tow(self):
        ans = self._tow()
        self.finish_step(ans, ans)

    def step_forward(self):
        ans = self._step_forward()
        self.finish_step(ans, ans)

    def turn_right(self): 
        ans = self._turn_right()
        self.finish_step(True, ans)

    def turn_left(self): 
        ans = self._turn_left()
        self.finish_step(True, ans)

    def has_to_drop():
        ans = self._has_to_drop()
        self.finish_step(False, True)
        return ans

    def drop_one(self):
        self._drop_one()
        self.finish_step(True, True)

    def drop_all(self):
        self._drop_all()
        self.finish_step(True, True)

    def has_to_add():
        ans = self._has_to_add()
        self.finish_step(False, True)
        return ans

    def add_one(self):
        self._add_one()
        self.finish_step(True, True)

    def add_all(self):
        self._add_all()
        self.finish_step(True, True)

