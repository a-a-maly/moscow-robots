import os
import warnings
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
           "<!memlt>": "",
           "<memgt>": "if_mem_gt",
           "<!memgt>": "",
        
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
           "[!memlt]": "",
           "[memgt]": "while_mem_gt",
           "[!memgt]": "",
        
           "[rclr]": "while_way_clean",
           "[!rclr]": "while_not_way_clean",
           "[rfwd]": "while_can_step",
           "[!rfwd]": "",
        
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
    pass
    


