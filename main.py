import random

import pygame
#import time
from pygame.locals import *
import time

size = 40
Background_Color = (110,120,6)
class Frog:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/frog.jpeg").convert()
        self.image_small = pygame.transform.scale(self.image,(30,30))
        self.parent_screen = parent_screen
        self.block_x = size*3
        self.block_y = size*3

    def draw(self):
        self.parent_screen.blit(self.image_small ,
                                    (
                                    self.block_x, self.block_y))  # blit funct to draw the block on the background
        pygame.display.flip()  # the above line should be followed by this line to show the updated screen

    def move(self):#when the snake collide with the frog, it will move its position
        self.block_x = random.randint(0,24)*size
        self.block_y = random.randint(0,19)*size

class Snake:
    def __init__(self,surface,length):
        self.length = length # length of the snake

        self.parent_screen = surface
        self.block = pygame.image.load("resources/block image.jpeg").convert()
        self.block_small = pygame.transform.scale(self.block, (30, 30))
        self.block_x = [size]*length
        self.block_y: int = [size]*length
        self.direction = 'down'
    def draw(self):
        self.parent_screen.fill(Background_Color)  # fill the background color here surface is the background the main one
        for i in range (self.length):
            self.parent_screen.blit(self.block_small,
                                (self.block_x[i], self.block_y[i]))  # blit funct to draw the block on the background
        pygame.display.flip()  # the above line should be followed by this line to show the updated screen

    def increase_length(self):
        self.length +=1
        self.block_x.append(-1)
        self.block_y.append(-1)

    def move_left(self): #move the block left
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1,0,-1): #going in the reverse direction
            self.block_x[i] = self.block_x[i - 1]
            self.block_y[i] = self.block_y[i - 1]
        if self.direction == 'up':
            self.block_y[0] -= size
        if self.direction == 'down':
            self.block_y[0] += size
        if self.direction == 'left':
            self.block_x[0] -= size
        if self.direction == 'right':
            self.block_x[0] += size

        self.draw()
class Game:
    def __init__(self):
        pygame.init()  # initiating pygame

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))  # only size is given in the argument
        self.surface.fill((144, 38, 37))  # fill the background color here surface is the background the main one
        self.snake = Snake(self.surface, 2) # length -> length of the snake here 4 blocks
        self.snake.draw()
        self.frog = Frog(self.surface)
        self.frog.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size :  #increase the size of the snake
            if y1 >= y2 and y1 < y2 + size:
                return True

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3") #Sound is a one time noice
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        back_sound = pygame.mixer.music.load("resources/backgroundmusic.mp3")
        pygame.mixer.music.play()

    def set_background(self):
        bg = pygame.image.load("resources/score_board.jpg").convert()
        self.surface.blit(bg,(0,0))

    def play(self): #do all the drawings if we have to call either multiple times this should be easu
        self.set_background()
        self.snake.walk()
        self.frog.draw()
        self.display_score()
        pygame.display.flip()


#snake eating frog
        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.frog.block_x, self.frog.block_y):
            #print("Collision occured")
            self.play_sound("game_point") #name of file
            self.snake.increase_length()
            self.frog.move()

    #snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
               # print("game over")
               #exit(0)
               self.play_sound("videogame-death")  #name of file
               raise "Game is Over!!!"


    def show_game_over(self):
        self.set_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Game is over !!! Your Score: {self.snake.length}', True, (255,255,255))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play the game again press Enter. To exit press Esc", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length}', True, (255,255,255))
        self.surface.blit(score,(800,10)) #anything on the background ie. surface should use blit function

    def reset(self):
        self.snake = Snake(self.surface, 1)  # length -> length of the snake here 4 blocks
        self.frog = Frog(self.surface)


    def run(self):
        running = True
        pause = False
        while running:  # event loop
            for event in pygame.event.get():  # event is pygame module for interacting with events and queue get->get event from queue
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # when esc key is pressed screen is exited
                        running = False
                    if event.key == K_RETURN: #it is the enter button
                        pause = False
                        pygame.mixer.music.unpause()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.3)
if __name__=="__main__":
    game = Game() #object Game
    game.run()


    pygame.display.flip() #the above line should be followed by this line to show the updated screen

 #  time.sleep(5) #after 5 sec the display will sleep /shut
