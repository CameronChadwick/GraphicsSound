import math
import pygame
import random
# in terminal -> pip install pygame

# color constants
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRASSGREEN = (19, 112, 30)
BLUE = (0, 0, 255)
SKYBLUE = (66, 135, 245)
WINDOWBLUE = (148, 189, 255)
BLACK = (0, 0, 0)
BROWN = (43, 24, 14)
GRAY = (117, 109, 102)
ROAD = (46, 46, 46)
CAR_COLORS = [RED, WHITE, YELLOW, GREEN]
ENEMYSPEEDS = [-5, -6, -7]

# game constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 400

SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
FPS = 60

##########################################################################


class Car():
    def __init__(self, x, y, width, height, radius, color1, color2, color3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.x_speed = random.choice(ENEMYSPEEDS)
        self.y_speed = 0
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3

    def draw_car(self):
        mainbody1 = (self.x, self.y, self.width, self.height)
        mainbody2 = (self.x - 20, self.y + 15, self.width - 25, self.height - 15)
        mainbody3 = (self.x + 50, self.y + 15, self.width - 25, self.height - 15)
        rearwindow = ([self.x, self.y], [self.x, self.y + 15], [self.x - 10, self.y + 15])
        frontwindow = ([self.x + 50, self.y], [self.x + 50, self.y + 15], [self.x + 60, self.y + 15])
        sidewindow = (self.x + 5, self.y + 5, self.width - 9, self.height - 25)
        windowsplit = (self.x + 23, self.y + 5, self.width - 45, self.height - 25)
        wheel1 = (self.x - 5, self.y + 40)
        wheel2 = (self.x + 60, self.y + 40)

        pygame.draw.rect(screen, self.color1, mainbody1)
        pygame.draw.rect(screen, self.color1, mainbody2)
        pygame.draw.rect(screen, self.color1, mainbody3)
        pygame.draw.rect(screen, self.color3, sidewindow)
        pygame.draw.rect(screen, self.color1, windowsplit)
        pygame.draw.polygon(screen, self.color3, rearwindow)
        pygame.draw.polygon(screen, self.color3, frontwindow)
        pygame.draw.circle(screen, self.color2, wheel1, self.radius)
        pygame.draw.circle(screen, self.color2, wheel2, self.radius)

    def update(self):
        self.y += self.y_speed

        if self.y <= 0:
            self.y = 0
        elif self.y + self.width >= DISPLAY_WIDTH:
            self.y = DISPLAY_WIDTH - self.width

    def move_enemy(self):
        self.x += self.x_speed
        if self.x < -100:
            self.x = 900
            self.y = random.randrange(21, 289)
            self.color1 = random.choice(CAR_COLORS)
            self.x_speed = random.choice(ENEMYSPEEDS)

    def enemy_collision(self):
        if (self.x <= enemy.x <= self.x + self.width or self.x <= enemy.x + enemy.width < self.x + self.width) \
                and (self.y < enemy.y < self.y + self.width or self.y < enemy.y + enemy.width < self.y + self.width):
            self.color1 = random.choice(CAR_COLORS)


class Barrier():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw_barrier(self):
        point_list = (self.x, self.y, self.width, self.height)

        pygame.draw.rect(screen, self.color, point_list)

    def barrier_collide_top(self):
        if player.y <= self.y + 20:
            player.y = 21

    def barrier_collide_bottom(self):
        if player.y >= self.y - 60:
            player.y = 289


class Road():
    def __init__(self, road_x, road_y, height, width, color1, linex, liney, linewidth, lineheight, color2):
        self.x = road_x
        self.y = road_y
        self.width = width
        self.height = height
        self.color1 = color1
        self.linex = linex
        self.liney = liney
        self.linewidth = linewidth
        self.lineheight = lineheight
        self.color2 = color2

    def draw_road(self):
        road_points = (self.x, self.y, self.width, self.height)
        line_points = (self.linex, self.liney, self.linewidth, self.lineheight)

        pygame.draw.rect(screen, self.color1, road_points)
        pygame.draw.rect(screen, self.color2, line_points)


road = Road(0, 200, 150, 800, ROAD, 0, 190, 800, 20, WHITE)
road2 = Road(0, 50, 150, 800, ROAD, 0, 195, 800, 0, WHITE)
barrier1 = Barrier(0, 0, 800, 50, BLACK)
barrier2 = Barrier(0, 350, 800, 50, BLACK)
background_image = pygame.image.load("saturn_bg.jpg")
player_image = pygame.image.load("player.png")

pygame.init()


screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pygame Picture")

clock = pygame.time.Clock()

# player
player_width = 50
x_loc = (150 - player_width)/2
y_loc = DISPLAY_HEIGHT - 2*player_width
player = Car(x_loc, y_loc, 50, 40, 10, BLUE, BLACK, WINDOWBLUE)

# enemies
enemy_width = 50
enemy_height = 40
enemy_radius = 10
enemy_list = []
for i in range(5):
    x_coord = 900
    random_y = random.randrange(21, 289)

    enemy = Car(x_coord, random_y, enemy_width, enemy_height, enemy_radius, random.choice(CAR_COLORS), BLACK, WINDOWBLUE)
    enemy_list.append(enemy)

running = True

while running:

    # pos = pygame.mouse.get_pos()
    # player.x = pos[0] - .5 * player.width
    # player.y = pos[1] - .5 * player.width

    for event in pygame.event.get():

        # check for user input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.y_speed = -4
            if event.key == pygame.K_s:
                player.y_speed = 4
        if event.type == pygame.KEYUP:
            player.y_speed = 0

        if event.type == pygame.QUIT:
            running = False

    # game logic

    screen.fill(WHITE)

    road.draw_road()
    road2.draw_road()
    barrier1.draw_barrier()
    barrier1.barrier_collide_top()
    barrier2.draw_barrier()
    barrier2.barrier_collide_bottom()
    screen.blit(background_image, [0, 0])
    player.draw_car()
    player.update()
    for enemy in enemy_list:
        enemy.draw_car()
        enemy.move_enemy()
        if player.enemy_collision():
            print("Lose")

    pygame.display.flip()

    clock.tick(FPS)

# quit
pygame.quit()
