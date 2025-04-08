#! /usr/bin/python3

import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

class IconsLoader:

    def __init__(self):
        self.cmd_fnames = {
           "_": "delete_command",
           "nop": "do_nop",
        
           "A": "do_sub_a",
           "B": "do_sub_b",
           "C": "do_sub_c",
           "D": "do_sub_d",
           "E": "do_sub_e",
        
           "fl0-": "do_fl0_down",
           "fl0+": "do_fl0_up",
           "fl1-": "do_fl1_down",
           "fl1+": "do_fl1_up",
           "pit0": "do_pit_clear",
           "pit++": "do_pit_inc",
           "pit--": "do_pit_dec",
           "mem0": "do_mem_clear",
           "mem+p": "do_mem_add",
           "mem-p": "do_mem_sub",
        
           "rfwd": "do_step_forward",
           "rright": "do_turn_right",
           "rleft": "do_turn_left",
           "rfix": "do_paint",
           "rtow": "do_tow",
        
           "rmup": "do_move_up",
           "rmright": "do_move_right",
           "rmdown": "do_move_down",
           "rmleft": "do_move_left",
        
           "radd": "do_link_all",
           "radd1": "do_link_one",
           "rdrop": "do_unlink_all",
           "rdrop1": "do_unlink_one",
        
           "(1)": "loop_1",
           "(2)": "loop_2",
           "(3)": "loop_3",
           "(4)": "loop_4",
           "(5)": "loop_5",
           "(6)": "loop_6",
           "(pit)": "loop_pit",
           "(mem)": "loop_mem",
        
           "<fl0>": "if_fl0_up",
           "<!fl0>": "if_fl0_down",
           "<fl1>": "if_fl1_up",
           "<!fl1>": "if_fl1_down",
           "<pit>": "if_not_pit_empty",
           "<!pit>": "if_pit_empty",
           "<memeq>": "if_mem_eq",
           "<!memeq>": "if_mem_ne",
           "<memlt>": "if_mem_lt",
           "<!memlt>": "if_mem_ge",
           "<memgt>": "if_mem_gt",
           "<!memgt>": "if_mem_le",
        
           "<rclr>": "if_way_clean",
           "<!rclr>": "if_not_way_clean",
           "<rfwd>": "if_can_step",
           "<!rfwd>": "if_not_can_step",
        
           "<rcnor>": "if_cell_azure",
           "<!rcnor>": "if_not_cell_azure",
           "<rcbro>": "if_cell_gray",
           "<!rcbro>": "if_not_cell_gray",
           "<rcfix>": "if_cell_blue",
           "<!rcfix>": "if_not_cell_blue",
        
           "<rmup>": "if_can_move_up",
           "<!rmup>": "if_not_can_move_up",
           "<rmright>": "if_can_move_right",
           "<!rmright>": "if_not_can_move_right",
           "<rmdown>": "if_can_move_down",
           "<!rmdown>": "if_not_can_move_down",
           "<rmleft>": "if_can_move_left",
           "<!rmleft>": "if_not_can_move_left",
        
           "<radd>": "if_can_link",
           "<!radd>": "if_not_can_link",
           "<rdrop>": "if_can_unlink",
           "<!rdrop>": "if_not_can_unlink",
        
           "[fl0]": "while_fl0_up",
           "[!fl0]": "while_fl0_down",
           "[fl1]": "while_fl1_up",
           "[!fl1]": "while_fl1_down",
           "[pit]": "while_not_pit_empty",
           "[!pit]": "while_pit_empty",
           "[memeq]": "while_mem_eq",
           "[!memeq]": "while_mem_ne",
           "[memlt]": "while_mem_lt",
           "[!memlt]": "while_mem_ge",
           "[memgt]": "while_mem_gt",
           "[!memgt]": "while_mem_le",
        
           "[rclr]": "while_way_clean",
           "[!rclr]": "while_not_way_clean",
           "[rfwd]": "while_can_step",
           "[!rfwd]": "while_not_can_step",
        
           "[rcnor]": "while_cell_azure",
           "[!rcnor]": "while_not_cell_azure",
           "[rcbro]": "while_cell_gray",
           "[!rcbro]": "while_not_cell_gray",
           "[rcfix]": "while_cell_blue",
           "[!rcfix]": "while_not_cell_blue",
        
           "[rmup]": "while_can_move_up",
           "[!rmup]": "while_not_can_move_up",
           "[rmright]": "while_can_move_right",
           "[!rmright]": "while_not_can_move_right",
           "[rmdown]": "while_can_move_down",
           "[!rmdown]": "while_not_can_move_down",
           "[rmleft]": "while_can_move_left",
           "[!rmleft]": "while_not_can_move_left",

           "[radd]": "while_can_link",
           "[!radd]": "while_not_can_link",
           "[rdrop]": "while_can_unlink",
           "[!rdrop]": "while_not_can_unlink",
        }

        self.cmd_icons = dict()
        for (key, name) in self.cmd_fnames.items():
            t = None
            if name:
                fname = os.path.join("icons", name + ".png")
                t = pygame.image.load(fname)
            self.cmd_icons[key] = t

    def get_icons(self):
        return self.cmd_icons     

    
class PEditor:

    def __init__(self):

        self.csize = 48
        self.mwidth = 8
        self.pwidth = 8
        self.fheight = 16

        csize = self.csize
        pygame.display.init()
        pygame.display.set_caption("PEditor")
        screen_resolution = ((self.mwidth + self.pwidth) * csize, self.fheight * csize)
        self.screen = pygame.display.set_mode(screen_resolution)
        self.screen.fill((0, 0, 0))

        self.menu_rect = (0, 0, self.mwidth * csize, self.fheight * csize)
        self.menu_sf = self.screen.subsurface(self.menu_rect)
        self.menu_blank = pygame.Surface((csize, csize))
        self.menu_blank.blit(self.menu_sf, (0, 0), (0, 0, csize, csize))

        self.prog_rect = (self.mwidth * csize, 0, self.pwidth * csize, self.fheight * csize)
        self.prog_sf = self.screen.subsurface(self.prog_rect)
        self.prog_sf.fill((0, 0, 191))
        self.prog_blank = pygame.Surface((csize, csize))
        self.prog_blank.blit(self.prog_sf, (0, 0), (0, 0, csize, csize))

        t = pygame.image.load("rblock.png").convert_alpha()
        self.iframe = pygame.transform.scale(t, (csize, csize))

        il = IconsLoader()
        self.images = il.get_icons()
        d = dict()
        for (key, v) in il.get_icons().items():
            t = v.convert_alpha()
            t = pygame.transform.smoothscale(t, (csize * 7 // 8, csize * 7 // 8))
            ts = t.get_size()
            dx = (csize - ts[0]) // 2
            dy = (csize - ts[1]) // 2
            w = pygame.Surface((csize, csize), pygame.SRCALPHA)
            w.fill((0, 0, 0, 0))
            w.blit(t, (dx, dy), (0, 0, ts[0], ts[1]))
            d[key] = w
        self.menu_icons = d
        self.prog_icons = d.copy()
        self.prog_icons['_'] = self.prog_blank


        menu0 = [[None for x in range(self.mwidth)] for y in range(self.fheight)]
        menu1 = [[None for x in range(self.mwidth)] for y in range(self.fheight)]
        self.menus = [menu0, menu1]
        self.menu_id = 0
        self.cmd_selected = "_"
        self.proga = [['_' for x in range(self.pwidth)] for y in range(self.fheight)]
        self.progb = [['_' for x in range(self.pwidth)] for y in range(self.fheight)]

        robot_dict = [
            [['(1)', 'A'], ['(2)', 'B'], ['(3)', 'C'], ['(4)', 'D'], ['(5)', 'E'], ['(6)', 'nop'], [], ['_', '_']],
            [['pit0', 'mem0'], ['pit++', 'mem+p'], ['pit--', 'mem-p'], ['(pit)', '(mem)'], ['<pit>', '[pit]'], ['<!pit>', '[!pit]'], ['', ''], ['', '']],
            [['<memeq>', '[memeq]'], ['<!memeq>', '[!memeq]'], ['<memlt>', '[memlt]'], ['<memgt>', '[memgt]'], ['<!memlt>', '[!memlt]'], ['<!memgt>', '[!memgt]'], ['', ''], ['', '']],
            [['fl0+', 'fl1+'], ['fl0-', 'fl1-'], ['<fl0>', '<fl1>'], ['<!fl0>', '<!fl1>'], ['[fl0]', '[fl1]'], ['[!fl0]', '[!fl1]'], ['', ''], ['', '']],
            [['rleft', 'rleft'], ['rright', 'rright'], ['rfwd', 'rtow'], ['rfix', ''], ['<rclr>', '<rfwd>'], ['<!rclr>', '<!rfwd>'], ['[rclr]', '[rfwd]'], ['[!rclr]', '[!rfwd]']],
            [['<rcnor>', '[rcnor]'], ['<!rcnor>', '[!rcnor]'], ['<rcbro>', '[rcbro]'], ['<!rcbro>', '[!rcbro]'], ['<rcfix>', '[rcfix]'], ['<!rcfix>', '[!rcfix]'], ['', ''], ['', '']],
            [['rmup', 'rmup'], ['rmright', 'rmright'], ['rmdown', 'rmdown'], ['rmleft', 'rmleft'], ['', ''], ['', ''], ['', ''], ['', '']],
            [['<rmup>', '[rmup]'], ['<!rmup>', '[!rmup]'], ['<rmright>', '[rmright]'], ['<!rmright>', '[!rmright]'], ['<rmdown>', '[rmdown]'], ['<!rmdown>', '[!rmdown]'], ['<rmleft>', '[rmleft]'], ['<!rmleft>', '[!rmleft]']],
            [['radd1', 'radd1'], ['radd', 'radd'], ['rdrop1', 'rdrop1'], ['rdrop', 'rdrop'], ['<radd>', '[radd]'], ['<!radd>', '[!radd]'], ['<rdrop>', '[rdrop]'], ['<!rdrop>', '[!rdrop]']],
        ]
        self.fill_menus(robot_dict)


    def fill_menus(self, d):
        ny = min(len(d), self.fheight)
        for y in range(ny):
            dy = d[y]
            nx = min(len(dy), self.mwidth)
            for x in range(nx):
                dyx = dy[x]
                l = min(len(dyx), 2)
                for z in range(l):
                    self.menus[z][y][x] = dyx[z]

    def get_current_prog(self):
        prog = [[self.proga[y][x] for x in range(self.pwidth)] for y in range(self.fheight)]
        for line in prog:
            while line and line[-1] == '_':
                line.pop()
        while prog and not prog[-1]:
            prog.pop()
        res = ""
        for line in prog:
            res += " ".join(line) + "\n"
        return res

    def redraw_menu(self):
        csize = self.csize
        menu = self.menus[self.menu_id]
        for y in range(self.fheight):
            for x in range(self.mwidth):
                cx, cy = x * csize, y * csize
                self.menu_sf.blit(self.menu_blank, (cx, cy))
                s = menu[y][x]
                if not s:
                    continue
                if s == self.cmd_selected:
                    self.menu_sf.blit(self.iframe, (cx, cy))
                t = self.menu_icons.get(s, None)
                if t:
                    self.menu_sf.blit(t, (cx, cy))

    def redraw_prog(self):
        self.prog_sf.fill((0, 0, 191))
        csize = self.csize
        for y in range(self.fheight):
            for x in range(self.pwidth):
                t = self.prog_icons[self.proga[y][x]]
                self.prog_sf.blit(t, (x * csize, y * csize))


    def redraw(self):
        self.redraw_menu()
        self.redraw_prog()

    def decode_pos(self, pos):
        none = (None, None, None)
        x = pos[0] // self.csize
        y = pos[1] // self.csize
        if x < 0 or x >= self.mwidth + self.pwidth:
            return none
        if y < 0 or y >= self.fheight:
            return none
        if x >= self.mwidth:
            return (x - self.mwidth, y, 1)
        else:
            return (x, y, 0)


    def do_kbclick(self, ev):
        return False

    def do_mclick(self, ev, mods):
        (px, py, pz) = self.decode_pos(ev.pos)
        if pz is None:
            return False
        if pz:
            # program panel
            pressed = pygame.key.get_pressed()
            if self.cmd_selected == self.proga[py][px]:
                self.proga[py][px] = self.progb[py][px]
                self.progb[py][px] = self.cmd_selected
            else:
                self.progb[py][px] = self.proga[py][px]
                self.proga[py][px] = self.cmd_selected
        else:
            # menu panel
            s = self.menus[self.menu_id][py][px]
            if s:
                self.cmd_selected = s
            else:
                self.menu_id = 1 - self.menu_id

        return True


    def main(self):
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        flag_dirty = True
        while True:
            if flag_dirty:
                flag_dirty = False
                self.redraw()
                pygame.display.flip()

            ev = pygame.event.wait()

            if ev.type == pygame.WINDOWSHOWN:
                pygame.display.flip()
                continue

            if ev.type == pygame.QUIT:
                break

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    break
                if ev.key == pygame.K_TAB:
                    self.menu_id = 1 - self.menu_id
                    flag_dirty = True
                    continue

            if ev.type == pygame.KEYDOWN:
                flag_dirty = self.do_kbclick(ev)
                continue

            if ev.type == pygame.MOUSEBUTTONDOWN:
                flag_dirty = self.do_mclick(ev, pygame.key.get_mods())
                continue

        pygame.display.flip()
        print(self.get_current_prog())

pe = PEditor()
pe.main()

