import pygame
import math

from random import randint

pygame.init()

GRAVITY = 1
run = True
started = False

win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Bird!")

bg_img = pygame.image.load('birdupbg.png')
ground_img = pygame.image.load('birdupground.png')
pipe_img = pygame.image.load('birduppipe.png')
bird_img = pygame.image.load('birdup.png')

font = pygame.font.SysFont('Comic Sans MS', 30)


class Bird:
    def __init__(self, win, img, x=250, y=250, vel=0, gravity=1):
        self.win = win
        self.img = img
        self.rotated_img = img

        self.x = x
        self.y = y
        self.vel = vel
        self.runs = -2
        self.gravity = gravity

        self.dead = False

    def update(self, started):
        self.runs += 1
        if started:
            if self.y < 475:
                self.y += self.vel
                self.vel += self.gravity
            else:
                self.y = 475
                self.dead = True
            if self.y < 0:
                self.y = 0
                self.vel = 0
        else:
            bird.y = 250 + math.sin(self.runs/10)*15

    def show(self):
        self.rotated_img = pygame.transform.rotate(self.img, -3*self.vel)
        self.win.blit(self.rotated_img, (bird.x, bird.y))

    def jump(self):
        self.vel = -10


class Pipe:
    def __init__(self, win, img, dir, x, len):
        self.win = win
        self.img = img

        self.dir = dir
        self.x = x
        self.len = len

    def update(self):
        self.x -= 7

    def show(self):
        if self.dir == "UP":
            self.win.blit(self.img, (self.x, 600-self.len))
        else:
            self.win.blit(pygame.transform.rotate(self.img, 180), (self.x, self.len-431))

    def check_collide(self, bird):
        if self.dir == "DOWN":
            if bird.x + 48 > self.x and self.x + 75 > bird.x:
                if bird.y + 2 < self.len:
                    bird.dead = True
        else:
            if bird.x + 48 > self.x and self.x + 75 > bird.x:
                if bird.y + 45 > 600-self.len:
                    bird.dead = True


class Ground:
    def __init__(self, win, img):
        self.win = win
        self.img = img
        self.runs = 0

        self.x = 0
        self.y = 500

    def update(self):
        self.x = (self.runs % 111) * -7
        self.runs += 1

    def show(self):
        self.win.blit(self.img, (self.x, self.y))


class ScoreBoard:
    def __init__(self, win):
        self.win = win

        self.score = -2
        self.runs = -2

    def update(self, started):
        if self.runs % 45 == 0 and started:
            self.score += 1
        self.runs += 1

    def show(self):
        scoreboard = font.render(str(self.score), False, (0, 0, 0))
        if self.score > -1:
            pygame.draw.rect(self.win, (255, 255, 255), (7, 5, len(str(self.score)) * 15 + 10, 35))
            win.blit(scoreboard, (10, 0))


class Background:
    def __init__(self, win, img):
        self.win = win
        self.img = img

    def show(self):
        self.win.blit(self.img, (0, 0))


class PipeController:
    def __init__(self, win, img):
        self.win = win
        self.img = img

        self.runs = -2
        self.pipes = []

    def update(self, bird, started):
        if self.runs % 45 == 0 and started:
            self.spawn_pipe_pair()

        self.runs += 1

        for p in self.pipes:
            if not bird.dead:
                p.update()
                p.check_collide(bird)

    def spawn_pipe_pair(self):
        r = randint(75, 350)
        self.pipes.append(Pipe(self.win, self.img, "DOWN", 900, r))
        self.pipes.append(Pipe(self.win, self.img, "UP", 900, 600-(r+125)))

    def show(self):
        for p in self.pipes:
            p.show()


pipe_controller = PipeController(win, pipe_img)
background = Background(win, bg_img)
bird = Bird(win, bird_img, gravity=GRAVITY)
ground = Ground(win, ground_img)
score_board = ScoreBoard(win)


while run:
    pygame.time.delay(5)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_SPACE:
                if not started:
                    started = True
                if not bird.dead:
                    bird.jump()
            elif event.key == pygame.K_r:
                started = False

                pipe_controller = PipeController(win, pipe_img)
                background = Background(win, bg_img)
                bird = Bird(win, bird_img, gravity=GRAVITY)
                ground = Ground(win, ground_img)
                score_board = ScoreBoard(win)
        elif event.type == pygame.QUIT:
            run = False

    if not bird.dead:
        score_board.update(started)
        pipe_controller.update(bird, started)
        ground.update()

    bird.update(started)

    background.show()
    pipe_controller.show()
    bird.show()
    ground.show()
    score_board.show()

    pygame.display.update()

pygame.quit()

