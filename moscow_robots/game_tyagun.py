import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from moscow_robots.data import get_image
from moscow_robots.game_robot import IsoGameRobot
from moscow_robots.game_dvigun import DvigunCellData as CellData
from moscow_robots.game_dvigun import DvigunFieldData as FieldData
from moscow_robots.game_dvigun import DvigunTextures

class Textures(DvigunTextures):
    def __init__(self, robot_kind, csize):
        DvigunTextures.__init__(self, robot_kind, csize)
        
        self.robot = []
        for i in range(4):
            t = get_image("tyagun" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.9, csize[1] * 0.8))
            self.robot.append(t)

        self.robot_turn = []
        for i in range(16):
            t = get_image("tyagun_turn" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.9, csize[1] * 0.8))
            self.robot_turn.append(t)

        self.robot_dead = []
        for i in range(4):
            t = get_image("tyagun_dead" + str(i)).convert_alpha()
            t = pygame.transform.scale(t, (csize[0] * 0.9, csize[1] * 0.8))
            self.robot_dead.append(t)


class GameTyagun(IsoGameRobot):
    robot_class_kind = 4

    def __init__(self, json_name):
        IsoGameRobot.__init__(self, json_name)

        self.field = FieldData()
        self.field.load(self.json_data["field"])

        self._resize_screen_for_iso()
        self.textures = Textures(self.robot_kind, self.csize)
        self._create_background_surface((102, 0, 255), self.textures)
        self._create_depth_surface(self.textures)

        self.robot_offset_y = self.csize[1] // 5
        self.block_offset_y = self.csize[1] // 6

    def _gather_all_objects(self):
        objects = IsoGameRobot._gather_all_objects(self)

        sx = self.field.sx
        sy = self.field.sy

        for y in range(sy):
            for x in range(sx):
                block = self.field.cells[y][x].block

                if block:
                    objects.append(('block', x, y, {'block': block}))

        return objects

    def move_robot(self, k):
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]

        blocks = [0 for i in range(k)]

        for i in range(k):
            xi = x - dx * (i + 1)
            yi = y - dy * (i + 1)

            blocks[i] = self.field.cells[yi][xi].block

            assert blocks[i]

            self.field.cells[yi][xi].block = 0

        self.screen.blit(self._background_surface, (0, 0))
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

            for j in range(1, k + 1):
                bx_pos = fx - dx * j
                by_pos = fy - dy * j

                anim_objects.append(('block', bx_pos, by_pos, {'block': blocks[j - 1]}))

            for by in range(sy):
                for bx in range(sx):
                    block = self.field.cells[by][bx].block

                    if block:
                        anim_objects.append(('block', bx, by, {'block': block}))

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

        for i in range(k):
            xi = x - dx * i
            yi = y - dy * i

            self.field.cells[yi][xi].block = blocks[i]

        self.robot.x += dx
        self.robot.y += dy


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
    
    def _can_pass(self, pos, d):
        sx = self.field.sx
        sy = self.field.sy
        x0, y0 = pos
        if not (0 <= x0 < sx):
            return False
        if not (0 <= y0 < sy):
            return False

        dx, dy = self.direction_vectors[d % 4]
        x1 = x0 + dx
        y1 = y0 + dy
        if not (0 <= x1 < sx):
            return False
        if not (0 <= y1 < sy):
            return False

        if dx and self.field.vfences[y0][min(x0, x1)]:
            return False
        if dy and self.field.hfences[min(y0, y1)][x0]:
            return False
        return self.field.cells[y1][x1].block == 0

    def _can_tow(self):
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]
        for i in range(-1, 1):
            if not self._can_pass((x + i * dx, y + i * dy), d):
                return False
        return self.field.cells[y - dy][x - dx].block != 0

    def _tow(self):
        if not self.robot_alive:
            return False
        if not self._can_tow():
            self.robot_alive = False
            return True

        self.move_robot(1)
        return False

    def _path_clear(self):
        return self._can_pass((self.robot.x, self.robot.y), self.robot.dir)

    def _step_forward(self):
        if not self.robot_alive:
            return False
        if not self._path_clear():
            self.robot_alive = False
            return True

        self.move_robot(0)
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

    def tow(self):
        ans = self._tow()
        self.finish_step(ans, ans)

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

