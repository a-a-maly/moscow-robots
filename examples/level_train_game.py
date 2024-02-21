from general import piktomir

# 214
game1 = piktomir.Game("level_train.json")
#game1.change_speed(700)

game1.link_all()
game1.unlink_one()
game1.link_one()
game1.pull()
game1.pull()
game1.pull()
game1.rotate_left()
game1.rotate_left()
game1.rotate_left()
game1.link_one()
game1.unlink_all()
game1.link_one()
#game1.pull()
# game1.link_all()
# # game1.unlink_all()
# # game1.link_one()
# # game1.link_one()
# # game1.link_one()
# # game1.link_one()
# # game1.rotate_right()

# game1.link_one()
# game1.rotate_left()
# # game1.rotate_left()
# # game1.link_one()
# game1.go()


# game1.link_all()
# game1.rotate_left()


# game1.go()
# game1.rotate_right()
# game1.go()
# game1.link_all()
# game1.pull()

#game1.unlink_one()
# game1.unlink_one()
# game1.link_one()
# game1.link_one()
# game1.unlink_all()

game1.main_loop()
# mass = [
#     {
#         "type": "active",
#         "mas_elem": [
#             {
#                 "type": 0,  # 0 - tractor, 1 - block1, 2 - block2
#                 "pos": self.x + self.y * self.max_x
#             }
#         ]
#     }
# ]
# for i in range(self.max_x * self.max_y):
#     if cells[i]["blocks"] != 0:
#         mass.append(
#             {
#                 "type": "passive",
#                 "mas_elem": [
#                     {
#                         "type": cells[i]["blocks"],
#                         "pos": i
#                     }
#                 ]
#             }
#         )
#         cells[i]["blocks"] = 0
# self.mas_trains.append(
#     {
#         "type": "passive",
#         "mas_elem": [
#             {
#                 "type": 1,
#                 "pos": 13
#             },
#             {
#                 "type": 1,
#                 "pos": 19
#             }
#         ]
#     }
# )
# self.mas_trains.append(
#     {
#         "type": "passive",
#         "mas_elem": [
#             {
#                 "type": 1,
#                 "pos": 20
#             },
#             {
#                 "type": 1,
#                 "pos": 21
#             }
#         ]
#     }
# )


# def blit(self, change_x, change_y, surface, pos):
#     x = pos % self.max_x
#     y = int(pos / self.max_x)
#     self.screen.blit(surface, (
#         self.cell_size[0] * (x + change_x),
#         self.cell_size[1] * (y + change_y)))


