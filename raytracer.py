import math
import random
# -------------------------------
resolution_x = 100
resolution_y = 100

player_pos_x = 1
player_pos_y = 1
player_pos_z = 1

player_angle_x = 0
player_angle_y = 0

fov = 60

size_x = 4
size_y = 4
size_z = 4

block_size = 100
block_threshold = 0.1
# -------------------------------




room = [[[0 for _ in range(size_z)] for _ in range(size_y)] for _ in range(size_x)]


for x in range(size_x):
    for y in range(size_y):
        for z in range(size_z):
            number = random.random()

            if number < block_threshold:
                room[x][y][z] = 1





distance_list = [[None for _ in range(resolution_y)] for _ in range(resolution_x)]



# calculate distances


















ascii_color_list = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'.")

print(ascii_color_list)
