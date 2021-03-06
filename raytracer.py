import math
import random
from tqdm import tqdm
import time
import numpy as np
from PIL import Image
# -------------------------------
resolution_x = 500
resolution_y = 500
render_distance = 100

player_pos_x = 160
player_pos_y = 160
player_pos_z = 160

player_angle_x = 0
player_angle_y = 0

fov_x = 60
fov_y = 60

size_x = 40
size_y = 40
size_z = 40

block_size = 10
block_threshold = 0.02
# -------------------------------


def sin(x):
    return math.sin(math.radians(x))
def cos(x):
    return math.cos(math.radians(x))
def tan(x):
    return math.tan(math.radians(x))
def cotan(x):
    return 1 / tan(x)


room = [[[0 for _ in range(size_z)] for _ in range(size_y)] for _ in range(size_x)]


for x in range(size_x):
    for y in range(size_y):
        for z in range(size_z):
            number = random.random()
            if x % 3 == 0 and y % 3 == 0 and z % 3 == 0:
                number = 0
            else:
                number = 1

            if number < block_threshold:
                room[x][y][z] = 1




for i in range(180):
    distance_list = [[None for _ in range(resolution_y)] for _ in range(resolution_x)]



    # calculate distances

    for pix_x in tqdm(range(resolution_x)):
        for pix_y in range(resolution_y):
            ray_angle_phi = ((player_angle_x - (0.5 * fov_x)) + (pix_x * (fov_x / resolution_x)))
            ray_angle_theta = ((player_angle_y - (0.5 * fov_y)) + (pix_y * (fov_y / resolution_y)))

            # ray_angle_phi %= 360
            # ray_angle_theta %= 360

            dis_x = None
            dis_y = None
            dis_z = None


            x_multiplier = 0
            y_multiplier = 0
            z_multiplier = 0

            if ray_angle_phi > 90 and ray_angle_phi < 270:
                dis_to_block_border_x = player_pos_x % block_size
                x_multiplier = -1
            elif ray_angle_phi > 270 or ray_angle_theta < 90:
                dis_to_block_border_x = block_size - (player_pos_x % block_size)
                x_multiplier = 1
            else:
                dis_x = -1
            
            if ray_angle_phi > 0 and ray_angle_phi < 180:
                dis_to_block_border_y = block_size - (player_pos_y % block_size)
                y_multiplier = 1
            elif ray_angle_phi > 180 and ray_angle_phi < 360:
                dis_to_block_border_y = player_pos_y % block_size
                y_multiplier = -1
            else:
                dis_y = -1

            if ray_angle_theta > 0 and ray_angle_theta < 180:
                dis_to_block_border_z = block_size - (player_pos_z % block_size)
                z_multiplier = 1
            elif ray_angle_theta > 180 and ray_angle_theta < 360:
                dis_to_block_border_z = player_pos_z % block_size
                z_multiplier = -1
            else:
                dis_z = -1

            # calculate distance x
            if dis_x != -1:
                ray_x_pos_x = player_pos_x + (dis_to_block_border_x * x_multiplier)
                ray_x_pos_y = player_pos_y + ((dis_to_block_border_x * tan(ray_angle_phi)))
                ray_x_pos_z = player_pos_z + ((dis_to_block_border_x / cos(ray_angle_phi)) * tan(ray_angle_theta))

                dis_x = (dis_to_block_border_x / cos(ray_angle_phi)) / cos(ray_angle_theta)

                ray_x_offset_x = block_size * x_multiplier
                ray_x_offset_y = ((block_size * tan(ray_angle_phi)))
                ray_x_offset_z = ((block_size / cos(ray_angle_phi)) * tan(ray_angle_theta))

                dis_x_offset = (block_size / cos(ray_angle_phi)) / cos(ray_angle_theta)

                

                for block in range(render_distance):
                    ray_x_block_x = int(ray_x_pos_x // block_size)
                    ray_x_block_y = int(ray_x_pos_y // block_size)
                    ray_x_block_z = int(ray_x_pos_z // block_size)

                    # print(ray_x_block_x, ray_x_block_y, ray_x_block_z)

                    if ray_x_block_x > len(room) -1 or ray_x_block_y > len(room[0]) -1 or ray_x_block_z > len(room[0][0]) -1 or ray_x_block_x < 0 or ray_x_block_y < 0 or ray_x_block_z < 0:
                        dis_x = -1
                        break

                    if room[ray_x_block_x][ray_x_block_y][ray_x_block_z] == 1:
                        break
                    dis_x += dis_x_offset
                    ray_x_pos_x += ray_x_offset_x
                    ray_x_pos_y += ray_x_offset_y
                    ray_x_pos_z += ray_x_offset_z
                else:
                    dis_x = -1

            if dis_x != -1:
                dis_x = dis_x

            # calculate distance y 
            if dis_y != -1:
                ray_y_pos_x = player_pos_x + ((dis_to_block_border_y * cotan(ray_angle_phi)))
                ray_y_pos_y = player_pos_y + (dis_to_block_border_y * y_multiplier)
                ray_y_pos_z = player_pos_z + ((dis_to_block_border_y / sin(ray_angle_phi)) * tan(ray_angle_theta))

                dis_y = (dis_to_block_border_x / sin(ray_angle_phi)) / cos(ray_angle_theta)

                ray_y_offset_x = ((block_size * cotan(ray_angle_phi)))
                ray_y_offset_y = block_size * y_multiplier
                ray_y_offset_z = ((block_size / sin(ray_angle_phi)) * tan(ray_angle_theta))

                dis_y_offset = (block_size / sin(ray_angle_phi)) / cos(ray_angle_theta)

                
                for block in range(render_distance):
                    ray_y_block_x = int(ray_y_pos_x // block_size)
                    ray_y_block_y = int(ray_y_pos_y // block_size)
                    ray_y_block_z = int(ray_y_pos_z // block_size)

                    # print(ray_x_block_x, ray_x_block_y, ray_x_block_z)

                    if ray_y_block_x > len(room) -1 or ray_y_block_y > len(room[0]) -1 or ray_y_block_z > len(room[0][0]) -1 or ray_y_block_x < 0 or ray_y_block_y < 0 or ray_y_block_z < 0:
                        dis_y = -1
                        break

                    if room[ray_y_block_x][ray_y_block_y][ray_y_block_z] == 1:
                        break
                    dis_y += dis_y_offset
                    ray_y_pos_x += ray_y_offset_x
                    ray_y_pos_y += ray_y_offset_y
                    ray_y_pos_z += ray_y_offset_z
                else:
                    dis_y = -1

            if dis_y != -1:
                dis_y = dis_y

            #calculate distance z 
            if dis_z != -1:
                ray_z_pos_x = player_pos_x + (dis_to_block_border_z / tan(ray_angle_theta) * cos(ray_angle_phi))
                ray_z_pos_y = player_pos_y + (dis_to_block_border_z / tan(ray_angle_theta) * sin(ray_angle_phi))
                ray_z_pos_z = player_pos_z + (dis_to_block_border_z * z_multiplier)

                dis_z = (dis_to_block_border_z / sin(ray_angle_theta))

                ray_z_offset_x = (block_size / tan(ray_angle_theta) * cos(ray_angle_phi))
                ray_z_offset_y = (block_size / tan(ray_angle_theta) * sin(ray_angle_phi))
                ray_z_offset_z = (block_size * z_multiplier)

                dis_z_offset = (block_size / sin(ray_angle_theta))

                

                for block in range(render_distance):
                    ray_z_block_x = int(ray_z_pos_x // block_size)
                    ray_z_block_y = int(ray_z_pos_y // block_size)
                    ray_z_block_z = int(ray_z_pos_z // block_size)

                    # print(ray_x_block_x, ray_x_block_y, ray_x_block_z)

                    if ray_z_block_x > len(room) -1 or ray_z_block_y > len(room[0]) -1 or ray_z_block_z > len(room[0][0]) -1 or ray_z_block_x < 0 or ray_z_block_y < 0 or ray_z_block_z < 0:
                        dis_z = -1
                        break

                    if room[ray_z_block_x][ray_z_block_y][ray_z_block_z] == 1:
                        break
                    dis_z += dis_z_offset
                    ray_z_pos_x += ray_z_offset_x
                    ray_z_pos_y += ray_z_offset_y
                    ray_z_pos_z += ray_z_offset_z
                else:
                    dis_z = -1

            if dis_z != -1:
                dis_z = dis_z
            
            # dis_z = 1000
            # dis_y = 1000
            # dis_x = 1000
            if dis_x == -1:
                dis_x = 1000
            if dis_y == -1:
                dis_y = 1000
            if dis_z == -1:
                dis_z = 1000


            if dis_x == dis_y == dis_z == 1000:
                color = [255, 255, 255]
            elif dis_x == min([dis_x, dis_y, dis_z]):
                color = [dis_x, 0, 0]
                color = [255, 0, 0]
            elif dis_y == min([dis_x, dis_y, dis_z]):
                color = [0, dis_y, 0]
                color = [0, 255, 0]
            elif dis_z == min([dis_x, dis_y, dis_z]):
                color = [0, 0, dis_z]
                color = [0, 0, 255]

            distance_list[pix_x][pix_y] = color



            
            # get smallest distance




    array = np.array(distance_list ,dtype=np.uint8)
    image = Image.fromarray(array)
    image = image.rotate(90, expand=True)
    image.save("render.png")

    # ascii_color_list = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'.")
    # screen = []
    # for line in distance_list:
    #     line_text = ""
    #     for element in line:
    #         line_text += (3*ascii_color_list[int(element) % len(ascii_color_list)])
    #     screen.append(line_text + "\n")
    # # print(*ascii_color_list)
    # with open("output.txt", "w") as f:
    #     f.writelines(screen)
    exit()
    player_angle_x += 15
    print(player_angle_x)




# ascii_color_list = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'.")
# for line in distance_list:
#     for element in line:
#         print(ascii_color_list[int(element) % len(ascii_color_list)], end="")
#     print("")
# print(*ascii_color_list)
