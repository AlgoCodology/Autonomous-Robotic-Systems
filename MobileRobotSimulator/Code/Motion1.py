import pygame
import math
import numpy as np



# CREATED BY: SHISHIR
def distance(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2))

#CREATED BY: AMIT
class Graphics:
    def __init__(self, dimentions, robot_img_path, map_img_path):
        pygame.init()
        # colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        self.robot = pygame.image.load(robot_img_path)
        self.map_img = pygame.image.load(map_img_path)

        # map dims
        self.height = dimentions[0]
        self.width = dimentions[1]
        # visulization window settings
        pygame.display.set_caption("Robot Simulator")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.map.blit(self.map_img, (0, 0))
        # text variables
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render('default', True, self.white, self.black)
        self.textRect = self.text.get_rect()
        self.textRect.center = (dimentions[1] - 400, dimentions[0] - 100)

    def write_info(self, Vl, Vr, theta, px, py):
        txt = f"Vl = {Vl} Vr = {Vr}  theta = {int(math.degrees(theta))}  X={px} y={py}"
        self.text = self.font.render(txt, True, self.white, self.black)
        self.map.blit(self.text, self.textRect)

    def draw_robot(self, x, y, heading):
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(heading), 1)
        rect = rotated.get_rect(center=(x, y))
        self.map.blit(rotated, rect)

    def draw_sensor_data(self, point_cloud):
        for point in point_cloud:
            pygame.draw.circle(self.map, self.red, point, 3, 0)

## CREATED BY: SONGYUE
class Robot:
    def __init__(self, startpos, width):
        self.m2p = 3779.52  # meters 2 pixels

        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        # theta: heading angle
        self.theta = 0
        self.vl = 0.01 * self.m2p  # meters/s
        self.vr = 0.01 * self.m2p
        #         self.vl = 0
        #         self.vr = 0
        self.maxspeed = 0.02 * self.m2p
        self.minspeed = 0 * self.m2p
        # graphics
        # self.img = pygame.image.load(robotImg)
        # self.rotated = self.img
        # self.rect = self.rotated.get_rect(center=(self.x, self.y))

    # def draw(self, map):
    #     map.blit(self.rotated, self.rect)

    def move(self, event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.vl += 0.001 * self.m2p
                elif event.key == pygame.K_s:
                    self.vl -= 0.001 * self.m2p
                elif event.key == pygame.K_o:
                    self.vr += 0.001 * self.m2p
                elif event.key == pygame.K_l:
                    self.vr -= 0.001 * self.m2p
                elif event.key == pygame.K_x:
                    self.vl = 0
                    self.vr = 0
                elif event.key == pygame.K_t:
                    self.vl += 0.001 * self.m2p
                    self.vr += 0.001 * self.m2p
                elif event.key == pygame.K_g:
                    self.vl -= 0.001 * self.m2p
                    self.vr -= 0.001 * self.m2p

        # self.vr = max(min(self.maxspeed, self.vr), self.minspeed)
        # self.vl = max(min(self.maxspeed, self.vl), self.minspeed)

        self.x += ((self.vl + self.vr) / 2) * math.cos(self.theta) * dt
        self.y -= ((self.vl + self.vr) / 2) * math.sin(self.theta) * dt
        self.theta += (self.vr - self.vl) / self.w * dt
        if self.theta >= math.pi:
            # self.theta %= 2 * math.pi
            self.theta = - math.pi
        if self.theta < - math.pi:
            self.theta = math.pi

        #         if self.vl == self.vr:
        #             self.x += ((self.vl + self.vr) / 2) * math.cos(self.theta) * dt
        #             self.y += ((self.vl + self.vr) / 2) * math.sin(self.theta) * dt

        #         elif self.vl != self.vr:
        #             R = (self.vl + self.vr)/(self.vr - self.vl) * 0.5 * self.w
        #             ICCx = self.x - R*math.sin(self.theta)
        #             ICCy = self.y + R*math.cos(self.theta)
        #             omeg = (self.vr - self.vl) / self.w * dt
        #             self.x = math.cos(omeg)*(self.x - ICCx) - math.sin(omeg)*(self.y - ICCy) + ICCx
        #             self.y = math.sin(omeg)*(self.x - ICCx) + math.cos(omeg)*(self.y - ICCy) + ICCy
        #             self.theta -= (self.vr - self.vl) / self.w * dt

        # self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta), 1)
        # self.rect = self.rotated.get_rect(center=(self.x, self.y))
    def check_collision(self, colcheck):
        if distance(colcheck[0], [self.x + self.w/2, self.y]) < 1.2:
            if self.theta > 0 and self.theta < math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = math.pi / 2
            elif self.theta == 0 and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif self.theta < 0 and self.theta > - math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = - math.pi / 2

        if distance (colcheck[1], [self.x, self.y - self.w/2]) < 1.2:
            if self.theta > 0 and self.theta < math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = 0
            elif self.theta == math.pi / 2 and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif self.theta > math.pi / 2 and self.theta < math.pi and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = - math.pi

        if distance(colcheck[2], [self.x - self.w/2, self.y]) < 1.2:
            if self.theta > math.pi / 2 and self.theta < math.pi and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = math.pi / 2
            elif (self.theta == math.pi or self.theta == - math.pi) and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif self.theta < - math.pi/2 and self.theta > - math.pi and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = - math.pi / 2

        if distance (colcheck[3], [self.x, self.y + self.w/2]) < 1.2:
            if self.theta > - math.pi and self.theta < - math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = - math.pi
            elif self.theta == - math.pi / 2 and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif self.theta > - math.pi / 2 and self.theta < 0 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = 0

# CREATED BY: AMIT
class Intersection:

    def __init__(self, sensor_range, map):
        self.sensor_range = sensor_range
        self.map_width, self.map_height = pygame.display.get_surface().get_size()
        self.map = map

    def checkpoint(self, x, y):
        points = []
        x1, y1 = x, y
        for angle in np.linspace(0, math.radians(360), 4, False):
            x2 = x1 + self.sensor_range * math.cos(angle)
            y2 = y1 - self.sensor_range * math.sin(angle)
            for i in range(0, 500):
                u = i / 500
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.map_width and 0 < y < self.map_height:
                    color = self.map.get_at((x, y))
                    # self.map.set_at((x, y), (0, 208, 255))
                    if (color[0], color[1], color[2]) == (0, 0, 0):
                        points.append([x, y])
                        break
        return points

#CREATED BY: SHISHIR

class Ultrasonic:

    def __init__(self, sensor_range, map):
        self.sensor_range = sensor_range
        self.map_width, self.map_height = pygame.display.get_surface().get_size()
        self.map = map

    def sense_obstacles(self, x, y, heading):
        obstacles = []
        x1, y1 = x, y
        start_angle = heading - self.sensor_range[1]
        finish_angle = heading + self.sensor_range[1]
        for angle in np.linspace(start_angle, finish_angle, 12, False):
            x2 = x1 + self.sensor_range[0] * math.cos(angle)
            y2 = y1 - self.sensor_range[0] * math.sin(angle)
            for i in range(0, 100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.map_width and 0 < y < self.map_height:
                    color = self.map.get_at((x, y))
                    self.map.set_at((x, y), (0, 208, 255))
                    if (color[0], color[1], color[2]) == (0, 0, 0):
                        obstacles.append([x, y])
                        break
        return obstacles

#CREATED BY: SONGYUE
# Pygame initialisation
pygame.init()

# start position
start = (100, 100)

# dimentions
MAP_DIMENSIONS = (600, 1200)

# running flag
running = True

# the envir
gfx = Graphics(MAP_DIMENSIONS, 'Robot1.png', 'Map1.png')

# the robot
robot = Robot(start, 0.01 * 8000)
sensor_range = 250, math.radians(180)
ultra_sonic = Ultrasonic(sensor_range, gfx.map)
detection = Intersection(1200, gfx.map)

# dt
dt = 0
lasttime = pygame.time.get_ticks()
# simulation loop
while running:
    dt = (pygame.time.get_ticks() - lasttime) / 1000
    lasttime = pygame.time.get_ticks()

    gfx.map.blit(gfx.map_img, (0, 0))


    gfx.draw_robot(robot.x, robot.y, robot.theta)
    point_cloud = ultra_sonic.sense_obstacles(robot.x, robot.y, robot.theta)
    checkpoints = detection.checkpoint(robot.x, robot.y)
    # gfx.draw_sensor_data(checkpoints)
    robot.move()
    robot.check_collision(checkpoints)
    gfx.draw_sensor_data(point_cloud)
    gfx.write_info(int(robot.vl), int(robot.vr), robot.theta, int(robot.x), int(robot.y))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        robot.move(event)