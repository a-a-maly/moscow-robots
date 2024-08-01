import pygame, pygame.freetype
from moscow_robots.data import get_image
from moscow_robots.game_robot import GameRobot
from moscow_robots.game_vertun import FieldData


class Textures:
    def __init__(self, robot_kind, csize):
        t = get_image("iskun").convert_alpha()
        self.robot = pygame.transform.scale(t, (csize[0] * 4 // 5, csize[1] * 4 // 5))
        t = get_image("iskun_dead").convert_alpha()
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


class GameIskun(GameRobot):

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

    def draw_temp(self):
        if not self.robot_alive:
            return
        x = self.robot.x
        y = self.robot.y
        txt = str(self.field.cells[y][x].t)
        if len(txt) > 4:
            txt = "####"
        cx = self.csize[0]
        cy = self.csize[1]
        ch = cy // 8
        font = pygame.freetype.SysFont(None, ch)
        r = font.get_rect(txt)
        
        bx = cx * x + (cx - r.width) // 2
        by = cy * y + (cy - r.height) // 2
        font.render_to(self.screen, (bx, by), txt, pygame.Color('purple'))

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
        self.draw_temp()

    def move_robot(self):
        cx = self.csize[0]
        cy = self.csize[1]
        x = self.robot.x
        y = self.robot.y
        d = self.robot.dir % 4
        dx, dy = self.direction_vectors[d]

        t = self.textures.robot
        t = pygame.transform.rotate(t, ((4 - d) % 4) * 90)

        self.redraw_field()
        scopy = self.screen.copy()

        m = 8
        for i in range(1, m + 1):
            self.screen.blit(scopy, (0, 0))
            dxi, dyi = dx * cx * i // m, dy * cy * i // m
            bx = cx * x + cx // 10 + dxi
            by = cy * y + cy // 10 + dyi
            self.screen.blit(t, (bx, by))
            pygame.display.update()
            if i < m:
                pygame.time.wait(self.game_speed // m)

        self.robot.x += dx
        self.robot.y += dy
        self.draw_temp()
        pygame.display.update()
        pygame.time.wait(self.game_speed // m)


    def _fix_cell(self):
        if not self.robot_alive:
            return False
        self.field.cells[self.robot.y][self.robot.x].painted = 1
        return True

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
        return False

    def get_temp(self):
        ans = self.field.cells[self.robot.y][self.robot.x].t
        self.finish_step(False, True)
        return ans

    def cell_fixed(self):
        ans = self.field.cells[self.robot.y][self.robot.x].painted
        self.finish_step(False, True)
        return ans

    def fix_cell(self):
        ans = self._fix_cell()
        self.finish_step(ans, True)

    def path_clear_up(self):
        self.robot.dir = 0
        ans = self._path_clear()
        self.finish_step(False, True)
        return ans

    def path_clear_right(self):
        self.robot.dir = 1
        ans = self._path_clear()
        self.finish_step(False, True)
        return ans

    def path_clear_down(self):
        self.robot.dir = 2
        ans = self._path_clear()
        self.finish_step(False, True)
        return ans

    def path_clear_left(self):
        self.robot.dir = 3
        ans = self._path_clear()
        self.finish_step(False, True)
        return ans

    def step_up(self):
        self.robot.dir = 0
        ans = self._step_forward()
        self.finish_step(ans, ans)

    def step_right(self):
        self.robot.dir = 1
        ans = self._step_forward()
        self.finish_step(ans, ans)

    def step_down(self):
        self.robot.dir = 2
        ans = self._step_forward()
        self.finish_step(ans, ans)

    def step_left(self):
        self.robot.dir = 3
        ans = self._step_forward()
        self.finish_step(ans, ans)

