import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
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
        iso_csize = (csize[0], csize[1] // 2)

        self.robot = []
        for i in range(4):
            t = get_image("dvigun" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.8, csize[1] * 0.7))
            self.robot.append(t)

        self.robot_dead = []
        for i in range(4):
            t = get_image("dvigun_dead" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.8, csize[1] * 0.7))
            self.robot_dead.append(t)

        t = get_image("robot_dest").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        t = pygame.transform.scale(t, iso_csize)
        self.robot_dest = t

        self.fields = []
        t = get_image("field_normal_other").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.fields.append(pygame.transform.scale(t, iso_csize))

        t = get_image("block_square_dest").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.fields.append(pygame.transform.scale(t, iso_csize))

        t = get_image("block_circle_dest").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.fields.append(pygame.transform.scale(t, iso_csize))

        t = get_image("block_any_dest").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.fields.append(pygame.transform.scale(t, iso_csize))

        self.blocks = [None]

        t = get_image("block_square").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 0.7, csize[1] * 0.7))
        self.blocks.append(t)

        t = get_image("block_circle").convert_alpha()
        t = pygame.transform.scale(t, (csize[0] * 0.6, csize[1] * 0.6))
        self.blocks.append(t)

        import math
        edge_len = math.sqrt((csize[0] / 2) ** 2 + (csize[1] / 4) ** 2) * math.sqrt(2)

        t = get_image("wall_hor").convert_alpha()
        t = pygame.transform.rotate(t, -45)
        t = pygame.transform.scale(t, (t.get_width(), t.get_height() // 2))
        scale = edge_len / t.get_width()
        self.hwall = pygame.transform.scale(
            t,
            (int(t.get_width() * scale), int(t.get_height() * scale))
        )

        t = get_image("wall_vert").convert_alpha()
        t = pygame.transform.rotate(t, -45)
        t = pygame.transform.scale(t, (t.get_width(), t.get_height() // 2))
        scale = edge_len / t.get_width()
        self.vwall = pygame.transform.scale(
            t,
            (int(t.get_width() * scale), int(t.get_height() * scale))
        )


class GameDvigun(GameRobot):
    robot_class_kind = 3

    def __init__(self, json_name):
        GameRobot.__init__(self, json_name)
        self.field = DvigunFieldData()
        self.field.load(self.json_data["field"])
        self.textures = DvigunTextures(self.robot_kind, self.csize)
        self._resize_screen_for_iso()

    def _resize_screen_for_iso(self):
        cx = self.csize[0]
        cy = self.csize[1]
        sx = self.field.sx
        sy = self.field.sy
        min_bx, max_bx = float('inf'), float('-inf')
        min_by, max_by = float('inf'), float('-inf')
        for y in range(-1, sy + 1):
            for x in range(-1, sx + 1):
                bx = (x - y) * (cx // 2)
                by = (x + y) * (cy // 4)
                min_bx = min(min_bx, bx)
                max_bx = max(max_bx, bx)
                min_by = min(min_by, by)
                max_by = max(max_by, by)
        screen_w = int(max_bx - min_bx)
        screen_h = int(max_by - min_by + cy // 2)
        
        # Минимальный размер экрана — 80% от размера монитора
        info = pygame.display.Info()
        min_w = info.current_w * 4 // 5
        min_h = info.current_h * 4 // 5
        screen_w = max(screen_w, min_w)
        screen_h = max(screen_h, min_h)
        
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self._iso_offset_x = screen_w // 2 - (min_bx + max_bx) / 2
        self._iso_offset_y = screen_h // 2 - (min_by + max_by) / 2

    def to_iso(self, x, y):
        cx = self.csize[0]
        cy = self.csize[1]

        bx = (x - y) * (cx // 2) + self._iso_offset_x
        by = (x + y) * (cy // 4) + self._iso_offset_y

        return bx, by

    def _z_key(self, obj_type, x, y, moving_shift=False):
        z = x + y

        if moving_shift and (obj_type == "robot" or obj_type == "block"):
            z += 0.15

        return (z, y, x)

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

    def redraw_all(self):
        self.screen.fill((255, 0, 255))

        self._draw_field_base()

        objects = self._gather_all_objects()

        self._draw_objects_sorted(objects)

    def _draw_field_base(self):
        sx = self.field.sx
        sy = self.field.sy

        for y in range(sy):
            for x in range(sx):
                cell = self.field.cells[y][x]

                t = self.textures.fields[cell.bdest]

                bx, by = self.to_iso(x, y)

                self.screen.blit(
                    t,
                    (
                        bx - t.get_width() // 2,
                        by - t.get_height() // 2
                    )
                )

        fpos = self.robot.fpos
        if fpos is not None:
            t = self.textures.robot_dest
            bx, by = self.to_iso(fpos[0], fpos[1])
            self.screen.blit(
                t,
                (
                    bx - t.get_width() // 2,
                    by - t.get_height() // 2
                )
            )

    def _gather_all_objects(self):
        objects = []

        sx = self.field.sx
        sy = self.field.sy

        objects.append(('robot', self.robot.x, self.robot.y, None))

        for y in range(sy):
            for x in range(sx):
                block = self.field.cells[y][x].block

                if block:
                    objects.append((
                        'block',
                        x,
                        y,
                        {
                            'block': block
                        }
                    ))

        for y in range(sy):
            for x in range(sx - 1):
                if self.field.vfences[y][x]:
                    objects.append(('vwall', x + 0.5, y, None))

        for y in range(sy - 1):
            for x in range(sx):
                if self.field.hfences[y][x]:
                    objects.append(('hwall', x, y + 0.5, None))

        return objects

    def _draw_object(self, obj_type, x, y, data=None, robot_tex=None):
        if obj_type == 'robot':
            t = robot_tex

            if t is None:
                d = self.robot.dir % 4

                if not self.robot_alive:
                    t = self.textures.robot_dead[d]
                else:
                    t = self.textures.robot[d]

            bx, by = self.to_iso(x, y)

            self.screen.blit(
                t,
                (
                    bx - t.get_width() // 2,
                    by - t.get_height() // 2 - self.csize[1] // 6
                )
            )

        elif obj_type == 'block':
            block_id = data['block']

            t = self.textures.blocks[block_id]

            bx, by = self.to_iso(x, y)

            self.screen.blit(
                t,
                (
                    bx - t.get_width() // 2,
                    by - t.get_height() // 2 - self.csize[1] // 8
                )
            )

        elif obj_type == 'vwall':
            t = self.textures.vwall

            bx, by = self.to_iso(x, y)

            bx += 5
            by -= 5

            self.screen.blit(
                t,
                (
                    bx - t.get_width() // 2,
                    by - t.get_height() // 2
                )
            )

        elif obj_type == 'hwall':
            t = self.textures.hwall

            bx, by = self.to_iso(x, y)

            by -= 5

            self.screen.blit(
                t,
                (
                    bx - t.get_width() // 2,
                    by - t.get_height() // 2
                )
            )

    def _draw_objects_sorted(self, objects, moving_shift=False, skip_robot=False):
        objects.sort(
            key=lambda obj: self._z_key(obj[0], obj[1], obj[2], moving_shift)
        )

        for obj_type, x, y, data in objects:
            if skip_robot and obj_type == 'robot':
                continue

            self._draw_object(obj_type, x, y, data)

    def move_robot(self, k):
        x = self.robot.x
        y = self.robot.y

        d = self.robot.dir % 4

        dx, dy = self.direction_vectors[d]

        blocks = [0 for i in range(k)]

        for i in range(k):
            xi = x + dx * (i + 1)
            yi = y + dy * (i + 1)

            blocks[i] = self.field.cells[yi][xi].block

            assert blocks[i]

            self.field.cells[yi][xi].block = 0

        self.screen.fill((255, 0, 255))

        self._draw_field_base()

        scopy = self.screen.copy()

        m = 8

        sx = self.field.sx
        sy = self.field.sy

        for i in range(m + 1):
            self.screen.blit(scopy, (0, 0))

            fx = x + dx * i / m
            fy = y + dy * i / m

            anim_objects = []

            anim_objects.append(('robot', fx, fy, None))

            for j in range(1, k + 1):
                bx_pos = fx + dx * j
                by_pos = fy + dy * j

                anim_objects.append((
                    'block',
                    bx_pos,
                    by_pos,
                    {
                        'block': blocks[j - 1]
                    }
                ))

            for by in range(sy):
                for bx in range(sx):
                    block = self.field.cells[by][bx].block

                    if block:
                        anim_objects.append((
                            'block',
                            bx,
                            by,
                            {
                                'block': block
                            }
                        ))

            for wy in range(sy):
                for wx in range(sx - 1):
                    if self.field.vfences[wy][wx]:
                        anim_objects.append(('vwall', wx + 0.5, wy, None))

            for wy in range(sy - 1):
                for wx in range(sx):
                    if self.field.hfences[wy][wx]:
                        anim_objects.append(('hwall', wx, wy + 0.5, None))

            moving_shift = False
            if dy > 0 or dx > 0:
                moving_shift = True

            self._draw_objects_sorted(anim_objects, moving_shift)

            pygame.display.update()

            pygame.time.wait(self.game_speed // (m + 1))

        for i in range(k):
            xi = x + dx * (i + 2)
            yi = y + dy * (i + 2)

            self.field.cells[yi][xi].block = blocks[i]

        self.robot.x += dx
        self.robot.y += dy

    def rotate_robot(self, dd):
        x = self.robot.x
        y = self.robot.y

        d = self.robot.dir % 4

        self.screen.fill((255, 0, 255))

        self._draw_field_base()

        scopy = self.screen.copy()

        m = 8

        for i in range(m + 1):
            self.screen.blit(scopy, (0, 0))

            mid_dir = (d + dd * i / m) % 4

            idx = int(round(mid_dir)) % 4

            anim_objects = self._gather_all_objects()

            anim_objects = [
                obj for obj in anim_objects
                if obj[0] != 'robot'
            ]

            anim_objects.append(('robot', x, y, idx))

            anim_objects.sort(key=lambda obj: self._z_key(obj[0], obj[1], obj[2]))

            for obj_type, ox, oy, data in anim_objects:
                if obj_type == 'robot':
                    ti = self.textures.robot[idx]

                    self._draw_object(
                        'robot',
                        ox,
                        oy,
                        robot_tex=ti
                    )
                else:
                    self._draw_object(obj_type, ox, oy, data)

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