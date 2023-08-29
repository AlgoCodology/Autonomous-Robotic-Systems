import pygame
import math
import numpy as np

# IMPLEMENTED BY SHISHIR JAIN
def distance(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2))

#IMPLEMENTED BY SHISHIR JAIN
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
        self.textRect.center = (dimentions[1] - 800, dimentions[0] - 100)
        self.text2 = self.font.render('default', True, self.white, self.black)
        self.textRect2 = self.text2.get_rect()
        self.textRect2.center = (dimentions[1] - 800, dimentions[0] - 70)
        self.trail_set1 = []
        self.trail_set2 = []
#IMPLEMENTED BY SHISHIR JAIN
    def write_info(self, Vl, Vr, theta, px, py,pointcloud):
        txt = f"Vl = {Vl} Vr = {Vr}  theta = {int(math.degrees(theta))}  X={px} y={py}"
        self.text = self.font.render(txt, True, self.white, self.black)
        self.map.blit(self.text, self.textRect)
        txt2 = f"Feature observed at location: {pointcloud[0:-1:3]}"
        self.text2 = self.font.render(txt2, True, self.white, self.black)
        self.map.blit(self.text2, self.textRect2)
#IMPLEMENTED BY SHISHIR JAIN
    def draw_robot(self, x, y, heading):
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(heading), 1)
        rect = rotated.get_rect(center=(x, y))
        self.map.blit(rotated, rect)
#IMPLEMENTED BY SHISHIR JAIN
    def draw_sensor_data(self, point_cloud,robotx,roboty):
        for point in point_cloud:
            pygame.draw.line(self.map, self.blue, (robotx, roboty), point)
            pygame.draw.circle(self.map, self.blue, point, 3, 0)
#IMPLEMENTED BY SONGYUE ZHANG
    def trail(self, pos, color):
        if color == 'black':
            for i in range(0, len(self.trail_set1) - 1):
                pygame.draw.line(self.map, self.black, (self.trail_set1[i][0], self.trail_set1[i][1]),
                                 (self.trail_set1[i + 1][0], self.trail_set1[i + 1][1]),2)
            self.trail_set1.append(pos)
        if color == 'red':
            for i in range(0, len(self.trail_set2) - 1):
                pygame.draw.line(self.map, self.red, (self.trail_set2[i][0], self.trail_set2[i][1]),
                                 (self.trail_set2[i + 1][0], self.trail_set2[i + 1][1]),2)
            self.trail_set2.append(pos)


class Robot:
#IMPLEMENTED BY AMIT JADHAV
    def __init__(self, startpos, width):
        self.m2p = 1779.52  # meters 2 pixels

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
        self.noisy_vl = self.vl
        self.noisy_vr = self.vr
        self.noisy_x = self.x
        self.noisy_y = self.y
        self.noisy_theta = self.theta
        # graphics
        # self.img = pygame.image.load(robotImg)
        # self.rotated = self.img
        # self.rect = self.rotated.get_rect(center=(self.x, self.y))

    # def draw(self, map):
    #     map.blit(self.rotated, self.rect)
#IMPLEMENTED BY AMIT JADHAV
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

        self.noisy_vl = self.vl + np.random.uniform(low=-50, high=50)
        self.noisy_vr = self.vr + np.random.uniform(low=-50, high=50)
        # self.noisy_vl = self.vl + np.random.randn()
        # self.noisy_vr = self.vr + np.random.randn()
        self.x += ((self.vl + self.vr) / 2) * math.cos(self.theta) * dt
        self.y -= ((self.vl + self.vr) / 2) * math.sin(self.theta) * dt
        self.noisy_x += ((self.noisy_vl + self.noisy_vr) / 2) * math.cos(self.noisy_theta) * dt
        self.noisy_y -= ((self.noisy_vl + self.noisy_vr) / 2) * math.sin(self.noisy_theta) * dt
        self.theta += (self.vr - self.vl) / self.w * dt
        self.noisy_theta += (self.noisy_vr - self.noisy_vl) / self.w * dt
        if self.theta >= math.pi:
            # self.theta %= 2 * math.pi
            self.theta = - math.pi
        if self.theta < - math.pi:
            self.theta = math.pi

        #         self.noisy_vl = self.vl + np.random.uniform(low=-100,high=100)
        #         self.noisy_vr = self.vr + np.random.uniform(low=-100,high=100)
        #         self.noisy_x += ((self.noisy_vl + self.noisy_vr) / 2) * math.cos(self.noisy_theta) * dt
        #         self.noisy_y -= ((self.noisy_vl + self.noisy_vr) / 2) * math.sin(self.noisy_theta) * dt
        #         self.noisy_theta += (self.noisy_vr - self.noisy_vl) / self.w * dt
        if self.noisy_theta >= math.pi:
            # self.theta %= 2 * math.pi
            self.noisy_theta = - math.pi
        if self.noisy_theta < - math.pi:
            self.noisy_theta = math.pi

    #     def noise(self):
    #         self.noisy_vl = self.vl + np.random.uniform(low=-1,high=1)
    #         self.noisy_vr = self.vr + np.random.uniform(low=-1,high=1)
    #         self.noisy_x += ((self.noisy_vl + self.noisy_vr) / 2) * math.cos(self.noisy_theta) * dt
    #         self.noisy_y -= ((self.noisy_vl + self.noisy_vr) / 2) * math.sin(self.noisy_theta) * dt
    #         self.noisy_theta += (self.noisy_vr - self.noisy_vl) / self.w * dt
    #         if self.noisy_theta >= math.pi:
    #             # self.theta %= 2 * math.pi
    #             self.noisy_theta = - math.pi
    #         if self.noisy_theta < - math.pi:
    #             self.noisy_theta = math.pi
    #         return self.noisy_x, self.noisy_y
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
#IMPLEMENTED BY AMIT JADHAV
    def check_collision(self, colcheck):
        if distance(colcheck[0], [self.x + self.w / 2, self.y]) < 1.2:
            if 0 < self.theta < math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = math.pi / 2
            elif self.theta == 0 and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif 0 > self.theta > - math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = - math.pi / 2

        if distance(colcheck[1], [self.x, self.y - self.w / 2]) < 1.2:
            if 0 < self.theta < math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = 0
            elif self.theta == math.pi / 2 and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif math.pi / 2 < self.theta < math.pi and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = - math.pi

        if distance(colcheck[2], [self.x - self.w / 2, self.y]) < 1.2:
            if math.pi / 2 < self.theta < math.pi and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = math.pi / 2
            elif (self.theta == math.pi or self.theta == - math.pi) and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif - math.pi / 2 > self.theta > - math.pi and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.sin(self.theta))
                self.vl = self.vr
                self.theta = - math.pi / 2

        if distance(colcheck[3], [self.x, self.y + self.w / 2]) < 1.2:
            if - math.pi < self.theta < - math.pi / 2 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = - math.pi
            elif self.theta == - math.pi / 2 and self.vl + self.vr > 0:
                self.vr = 0
                self.vl = 0
            elif - math.pi / 2 < self.theta < 0 and self.vl + self.vr > 0:
                self.vr = ((self.vl + self.vr) / 2.0) * abs(math.cos(self.theta))
                self.vl = self.vr
                self.theta = 0


class Intersection:
#IMPLEMENTED BY SONGYUE ZHANG
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


class Ultrasonic:
#IMPLEMENTED BY SONGYUE ZHANG
    def __init__(self, sensor_range, map):
        self.sensor_range = sensor_range
        self.map_width, self.map_height = pygame.display.get_surface().get_size()
        self.map = map
#IMPLEMENTED BY AMIT JADHAV
    def sense_features(self, x, y, heading):
        features = []
        x1, y1 = x, y
        start_angle = heading - self.sensor_range[1]
        finish_angle = heading + self.sensor_range[1]
        for angle in np.linspace(start_angle, finish_angle, 360, False):
            x2 = x1 + self.sensor_range[0] * math.cos(angle)
            y2 = y1 - self.sensor_range[0] * math.sin(angle)
            for i in range(0, 100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.map_width and 0 < y < self.map_height:
                    color = self.map.get_at((x, y))
                    # self.map.set_at((x, y), (0, 208, 255))
                    if (color[0], color[1], color[2]) == (0, 0, 255):
                        features.append([x, y])
                        break
        return features

#IMPLEMENTED BY SONGYUE ZHANG TILL THE END
# Pygame initialisation
pygame.init()

# start position
start = (100, 100)

# dimentions
MAP_DIMENSIONS = (600, 1200)

# running flag
running = True

# the envir
gfx = Graphics(MAP_DIMENSIONS, "C:\\Users\\Amit\\MSC AI - ARS - P4Y1\\Assignment 2 MRS\\Robot.png",
               "C:\\Users\\Amit\\MSC AI - ARS - P4Y1\\ImageRGBtoCSV_Extracter\\MapRectFeatures.png")

# the robot
robot = Robot(start, 0.01 * 8000)
sensor_range = 180, math.radians(180)
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
    checkpoints = detection.checkpoint(robot.x, robot.y)
    robot.check_collision(checkpoints)
    point_cloud = ultra_sonic.sense_features(robot.x, robot.y, robot.theta)
    gfx.draw_sensor_data(point_cloud,robot.x,robot.y)
    robot.move()
    #     gfx.draw_sensor_data(point_cloud)
    gfx.write_info(int(robot.vl), int(robot.vr), robot.theta, int(robot.x), int(robot.y),point_cloud)
    gfx.trail((robot.x, robot.y), 'black')
    gfx.trail((robot.noisy_x, robot.noisy_y), 'red')
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        robot.move(event)
