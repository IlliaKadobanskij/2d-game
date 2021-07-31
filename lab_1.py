import pygame
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox


def info(message, title="Result"):
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()


pygame.init()
width = 700
height = 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Lab_1')
clock = pygame.time.Clock()
bg = pygame.image.load(r'sprites\bg\bg.png')


class Player(ABC):

    def __init__(self, x, y, w, h, c):
        self.hp = 50
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.c_a = self.c
        self.__speed = 7
        self.__jump_count = 17
        self.__attack_timer = 20
        self.__timer_after_attack = 20
        self.__is_jump = False
        self.attacked = False
        self.last_move = 'right'
        self.right = False
        self.left = False
        self.animation_count = 0

    @abstractmethod
    def draw(self):
        pass

    def action(self, buttons, side, damage):
        if keys[buttons[0]] and self.x < width - self.w:
            self.x += self.__speed
            self.last_move = 'right'
            self.left = False
            self.right = True
        elif keys[buttons[1]] and self.x > 0:
            self.x -= self.__speed
            self.last_move = 'left'
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = False
            self.animation_count = 0
        if self.attacked:
            self.__attack_timer -= 1
            self.hp -= damage
            if self.__attack_timer > 0:
                if side:
                    if self.x < width - self.w:
                        self.x += 5
                else:
                    if self.x >= 5:
                        self.x -= 5
                self.c = (255, 0, 0)
            else:
                self.c = self.c_a
                if self.__timer_after_attack > 0:
                    self.__timer_after_attack -= 1
                else:
                    self.c = self.c_a
                    self.__timer_after_attack = 20
                    self.__attack_timer = 20
                    self.attacked = False

        if not self.__is_jump:
            if keys[buttons[2]]:
                self.__is_jump = True
        else:
            if self.__jump_count >= -17:
                if self.__jump_count < 0:
                    self.y += (self.__jump_count ** 2) / 15
                else:
                    self.y -= (self.__jump_count ** 2) / 15
                self.__jump_count -= 1
            else:
                self.__is_jump = False
                self.__jump_count = 17


class Knight(Player):
    def __init__(self, x, y, w, h, c):
        super().__init__(x, y, w, h, c)
        self.damage = 0.4
        self.stand = pygame.image.load(r'sprites\idle.png')
        self.walk_right = [pygame.image.load(r'sprites\right\run1.png'),
                           pygame.image.load(r'sprites\right\run2.png'),
                           pygame.image.load(r'sprites\right\run3.png'),
                           pygame.image.load(r'sprites\right\run4.png'),
                           pygame.image.load(r'sprites\right\run5.png'),
                           pygame.image.load(r'sprites\right\run6.png'),
                           pygame.image.load(r'sprites\right\run7.png'),
                           pygame.image.load(r'sprites\right\run8.png')]
        self.walk_left = [pygame.image.load(r'sprites\left\run1.png'),
                          pygame.image.load(r'sprites\left\run2.png'),
                          pygame.image.load(r'sprites\left\run3.png'),
                          pygame.image.load(r'sprites\left\run4.png'),
                          pygame.image.load(r'sprites\left\run5.png'),
                          pygame.image.load(r'sprites\left\run6.png'),
                          pygame.image.load(r'sprites\left\run7.png'),
                          pygame.image.load(r'sprites\left\run8.png')]

    def draw(self):
        if self.animation_count + 1 >= 60:
            self.animation_count = 0

        if self.left:
            win.blit(self.walk_left[self.animation_count // 8], (self.x, self.y))
            self.animation_count += 1
        elif self.right:
            win.blit(self.walk_right[self.animation_count // 8], (self.x, self.y))
            self.animation_count += 1
        else:
            win.blit(self.stand, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 10, self.hp, 5))


class Warlock(Player):
    def __init__(self, x, y, w, h, c):
        super().__init__(x, y, w, h, c)
        self.damage = 0.2
        self.stand = pygame.image.load(r'sprites\idlem.png')
        self.walk_right = [pygame.image.load(r'sprites\rightm\run1.png'),
                           pygame.image.load(r'sprites\rightm\run2.png'),
                           pygame.image.load(r'sprites\rightm\run3.png'),
                           pygame.image.load(r'sprites\rightm\run4.png'),
                           pygame.image.load(r'sprites\rightm\run5.png'),
                           pygame.image.load(r'sprites\rightm\run6.png'),
                           pygame.image.load(r'sprites\rightm\run7.png'),
                           pygame.image.load(r'sprites\rightm\run8.png')]
        self.walk_left = [pygame.image.load(r'sprites\leftm\run1.png'),
                          pygame.image.load(r'sprites\leftm\run2.png'),
                          pygame.image.load(r'sprites\leftm\run3.png'),
                          pygame.image.load(r'sprites\leftm\run4.png'),
                          pygame.image.load(r'sprites\leftm\run5.png'),
                          pygame.image.load(r'sprites\leftm\run6.png'),
                          pygame.image.load(r'sprites\leftm\run7.png'),
                          pygame.image.load(r'sprites\leftm\run8.png')]

    def draw(self):
        if self.animation_count + 1 >= 60:
            self.animation_count = 0

        if self.left:
            win.blit(self.walk_left[self.animation_count // 8], (self.x, self.y))
            self.animation_count += 1
        elif self.right:
            win.blit(self.walk_right[self.animation_count // 8], (self.x, self.y))
            self.animation_count += 1
        else:
            win.blit(self.stand, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 10, self.hp, 5))

    def attack(self):
        if keys[pygame.K_RCTRL]:
            if self.last_move == 'right':
                facing = 1
            else:
                facing = -1

            if len(bullets) < 1:
                bullets.append(Shell(round(self.x + self.w // 2), round(self.y + self.h // 2), 5, (255, 0, 0), facing))

    def draw_bullets(self):
        for bullet in bullets:
            bullet.draw(win)


class Shell:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 12 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


player1 = Knight(25, 225, 50, 50, (0, 0, 255))
player2 = Warlock(width - 75, 225, 50, 50, (0, 255, 0))

buttons_player_1 = [pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_LCTRL]
buttons_player_2 = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_RCTRL]

timer = 100
bullets = []


# ------------------------------------  game  --------------------------------------

def draw_window():
    win.blit(bg, (0, 0))
    player1.draw()
    player2.draw()
    player2.draw_bullets()
    pygame.display.update()


running = True
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    if player1.hp <= 0:
        info('Player 2  wins!')
        running = False
    elif player2.hp <= 0:
        info('Player 1  wins!')
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if 700 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if keys[buttons_player_1[3]]:
        if abs(player1.x - player2.x) <= player1.w and abs(player1.y - player2.y) <= player1.h:
            player2.attacked = True
    for bullet in bullets:
        if abs(player1.x - bullet.x) <= player1.w and abs(player1.y - bullet.y) <= player1.h:
            player1.attacked = True

    side = True if player1.x > player2.x else False

    player1.action(buttons_player_1, side, player2.damage)
    player2.action(buttons_player_2, not side, player1.damage)
    player2.attack()

    draw_window()

pygame.quit()
