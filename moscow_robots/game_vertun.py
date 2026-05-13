import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from moscow_robots.data import get_image
from moscow_robots.game_robot import GameRobot
import math

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
            elif c == 't':
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

    def export(self):
        res = dict()
        cs = [[str(self.cells[y][x]) for x in range(self.sx)] for y in range(self.sy)]
        hfs = ["".join([" -"[self.hfences[y][x]] for x in range(self.sx)]) for y in range(self.sy - 1)]
        vfs = ["".join([" |"[self.vfences[y][x]] for x in range(self.sx - 1)]) for y in range(self.sy)]
        res["sx"] = self.sx
        res["sy"] = self.sy
        res["cells"] = cs
        res["hfences"] = hfs
        res["vfences"] = vfs
        return res


class Textures:
    def __init__(self, robot_kind, csize):
        iso_csize = (csize[0], csize[1] // 2)

        self.robot = []
        for i in range(4):
            t = get_image("vertun" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.65, csize[1] * 1.1))
            self.robot.append(t)

        self.robot_turn = []
        for i in range(16):
            t = get_image("vertun_turn" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.65, csize[1] * 1.1))
            self.robot_turn.append(t)

        self.robot_dead = []
        for i in range(4):
            t = get_image("vertun_dead" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.65, csize[1] * 1.1))
            self.robot_dead.append(t)

        t = get_image("robot_dest").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        t = pygame.transform.scale(t, iso_csize)
        self.robot_dest = t

        t = get_image("field_normal").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.field_normal = pygame.transform.scale(t, iso_csize)
        t = get_image("field_normal_painted").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.field_normal_painted = pygame.transform.scale(t, iso_csize)
        t = get_image("field_broken").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.field_broken = pygame.transform.scale(t, iso_csize)
        t = get_image("field_broken_painted").convert_alpha()
        t = pygame.transform.rotate(t, 45)
        self.field_broken_painted = pygame.transform.scale(t, iso_csize)

        edge_len = math.sqrt((csize[0] / 2) ** 2 + (csize[1] / 4) ** 2) * math.sqrt(2)

        t = get_image("vertun_wall_hor").convert_alpha()
        t = pygame.transform.rotate(t, -45)
        t = pygame.transform.scale(t, (t.get_width(), t.get_height() // 2))
        scale = edge_len / t.get_width()
        scale *= 0.9
        self.hwall = pygame.transform.scale(
            t,
            (int(t.get_width() * scale), int(t.get_height() * scale))
        )

        t = get_image("vertun_wall_vert").convert_alpha()
        t = pygame.transform.rotate(t, -45)
        t = pygame.transform.scale(t, (t.get_width(), t.get_height() // 2))
        scale = edge_len / t.get_width()
        scale *= 0.9
        self.vwall = pygame.transform.scale(
            t,
            (int(t.get_width() * scale), int(t.get_height() * scale))
        )

        edge_len = math.sqrt(
            (csize[0] / 2) ** 2 +
            (csize[1] / 4) ** 2
        )

        t = get_image("vertun_depth_hor").convert_alpha()
        scale = edge_len * 0.9 / t.get_width()
        self.depth_hor = pygame.transform.scale(
            t,
            (
                int(t.get_width() * scale),
                int(t.get_height() * scale)
            )
        )

        t = get_image("vertun_depth_vert").convert_alpha()
        scale = edge_len * 0.9 / t.get_width()
        self.depth_vert = pygame.transform.scale(
            t,
            (
                int(t.get_width() * scale),
                int(t.get_height() * scale)
            )
        )


class GameVertun(GameRobot):
    robot_class_kind = 1

    def __init__(self, json_name):
        GameRobot.__init__(self, json_name)

        self.field = FieldData()
        self.field.load(self.json_data["field"])

        self._resize_screen_for_iso()
        self.textures = Textures(self.robot_kind, self.csize)
        self._create_depth_surface()

    def _resize_screen_for_iso(self):
        cx = self.csize[0]
        cy = self.csize[1]
        sx = self.field.sx
        sy = self.field.sy
        
        min_size = 1600  

        cx_needed = int(min_size * 2 / (sx + sy))
        cy_needed = int(min_size * 4 / (sx + sy))
        target_cell = min(cx_needed, cy_needed)

        target_cell = max(64, min(128, target_cell))
        
        if target_cell % 2:
            target_cell += 1
        
        self.csize = (target_cell, target_cell)
        cx = cy = target_cell
        
        min_bx, max_bx = float('inf'), float('-inf')
        min_by, max_by = float('inf'), float('-inf')
        
        for y in range(sy):
            for x in range(sx):
                bx = (x - y) * (cx // 2)
                by = (x + y) * (cy // 4)
                min_bx = min(min_bx, bx)
                max_bx = max(max_bx, bx)
                min_by = min(min_by, by)
                max_by = max(max_by, by)
        
        screen_w = int(max_bx - min_bx + cx * 2)
        screen_h = int(max_by - min_by + cy * 2 / math.sqrt(2))
        
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self._iso_offset_x = screen_w // 2 - (min_bx + max_bx) / 2
        self._iso_offset_y = screen_h // 2 - (min_by + max_by) / 2

    def _create_depth_surface(self):

        cx = self.csize[0]
        cy = self.csize[1]

        sx = self.field.sx
        sy = self.field.sy

        hw = cx // 2
        hh = cy // 4

        self._depth_surface = pygame.Surface(
            self.screen.get_size(),
            pygame.SRCALPHA
        )

        depth_offset = cy // 4

        for x in range(sx):
            bx, by = self.to_iso(x, sy - 1)
            t = self.textures.depth_hor

            px = bx - hw
            py = by + hh

            self._depth_surface.blit(
                t,
                (
                    int(px + 1),
                    int(py - depth_offset - 1)
                )
            )


        for y in range(sy):
            bx, by = self.to_iso(sx - 1, y)
            t = self.textures.depth_vert

            px = bx + hw
            py = by + hh

            self._depth_surface.blit(
                t,
                (
                    int(px - t.get_width()),
                    int(py - depth_offset - 1)
                )
            )

    def to_iso(self, x, y):
        cx = self.csize[0]
        cy = self.csize[1]

        bx = (x - y) * (cx // 2) + self._iso_offset_x
        by = (x + y) * (cy // 4) + self._iso_offset_y

        return bx, by

    def _z_key(self, x, y, dir=None):
        
        if (dir == "vert_move"):
            return (x + y, x, y)
        else:
            return (x + y, y, x)

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

    def redraw_all(self):
        self.screen.fill((0, 0, 255))
        self.screen.blit(self._depth_surface, (0, 0))
        self._draw_field_base()

        objects = self._gather_all_objects()

        self._draw_objects_sorted(objects)

    def _draw_field_base(self):
        sx = self.field.sx
        sy = self.field.sy

        for y in range(sy):
            for x in range(sx):
                cell = self.field.cells[y][x]
                t = None
                if cell.broken:
                    if cell.painted:
                        t = self.textures.field_broken_painted
                    else:
                        t = self.textures.field_broken
                else:  # normal
                    if cell.painted:
                        t = self.textures.field_normal_painted
                    else:
                        t = self.textures.field_normal

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
            by -= self.csize[1] // 2.5

            self.screen.blit(
                t,
                (
                    bx - t.get_width() // 2,
                    by - t.get_height() // 2
                )
            )

        elif obj_type == 'vwall':
            t = self.textures.vwall

            bx, by = self.to_iso(x, y)

            bx += 2.5
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

            bx += 2.5
            by -= 5

            self.screen.blit(
                t,
                (
                    bx - t.get_width() // 2,
                    by - t.get_height() // 2
                )
            )

    def _draw_objects_sorted(self, objects, dir=None):
        objects.sort(
            key=lambda obj: self._z_key(obj[1], obj[2], dir)
        )

        for obj_type, x, y, data in objects:
            self._draw_object(obj_type, x, y, data)

    def move_robot(self):
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]

        self.screen.fill((0, 0, 255))
        self.screen.blit(self._depth_surface, (0, 0))
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

            for wy in range(sy):
                for wx in range(sx - 1):
                    if self.field.vfences[wy][wx]:
                        anim_objects.append(('vwall', wx + 0.5, wy, None))

            for wy in range(sy - 1):
                for wx in range(sx):
                    if self.field.hfences[wy][wx]:
                        anim_objects.append(('hwall', wx, wy + 0.5, None))

            dir = None
            if dx == 0: 
                dir = "vert_move"

            self._draw_objects_sorted(anim_objects, dir)

            pygame.display.update()

            pygame.time.wait(self.game_speed // (m + 1))

    def rotate_robot(self, dd):
        x = self.robot.x
        y = self.robot.y

        d = self.robot.dir % 4

        self.screen.fill((0, 0, 255))
        self.screen.blit(self._depth_surface, (0, 0))
        self._draw_field_base()

        scopy = self.screen.copy()

        m = 16

        for i in range(m + 1):
            self.screen.blit(scopy, (0, 0))

            if dd == 1:
                mid_dir = (d * 4 + 4 * i / m) % 16
            else:
                mid_dir = (d * 4 - 4 * i / m) % 16

            idx = int(round(mid_dir)) % 16

            anim_objects = self._gather_all_objects()

            anim_objects = [
                obj for obj in anim_objects
                if obj[0] != 'robot'
            ]

            anim_objects.append(('robot', x, y, None))

            anim_objects.sort(key=lambda obj: self._z_key(obj[1], obj[2]))

            for obj_type, ox, oy, data in anim_objects:
                if obj_type == 'robot':
                    ti = self.textures.robot_turn[idx]

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