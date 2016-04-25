#!/usr/bin/env python

import pygame
import random
import sys
import time

pygame.init()

# Screen size (pixels)
SCREEN_W = 500
SCREEN_H = 500

# Block size (pixels)
BS = 5

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Directions
L, D, R, U = 0, 1, 2, 3


class Block:

    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color

    def draw(self):
        global screen
        rect_position = (self._x * BS, self._y * BS, BS, BS)
        pygame.draw.rect(screen, self._color, rect_position, 0)

    def get_position(self):
        return (self._x, self._y)


class Snake:

    def __init__(self):
        self._blocks = [Block(50, 50, green), Block(51, 50, green)]
        self._direction = L

    def draw(self):
        for block in self._blocks:
            block.draw()

    def grow(self):

        # Get the current position of the head
        x, y = self.get_head_position()

        # Add a new block depending on current direction
        if self._direction == L:
            new_x, new_y = x - 1, y
        elif self._direction == D:
            new_x, new_y = x, y + 1
        elif self._direction == R:
            new_x, new_y = x + 1, y
        elif self._direction == U:
            new_x, new_y = x, y - 1

        # Create the new block and insert it at the head of the list
        new_block = Block(new_x, new_y, green)
        self._blocks.insert(0, new_block)

    def shrink(self):
        self._blocks.pop()

    def move(self):
        self.grow()
        self.shrink()

    def get_head_position(self):
        return self._blocks[0].get_position()

    def set_direction(self, direction):
        if self._direction == L and direction == R:
            return
        elif self._direction == D and direction == U:
            return
        elif self._direction == R and direction == L:
            return
        elif self._direction == U and direction == D:
            return
        self._direction = direction

    def is_dead(self):

        global board

        # Get the current position of the head
        x, y = self.get_head_position()

        # If snake is off screen, kill it
        if (((x * BS) < 0 or (x * BS) > SCREEN_W) or
            ((y * BS) < 0 or (y * BS) > SCREEN_H)):
            return True

        # If snake has run into itself, kill it
        for block in self._blocks[1:]:
            if (x, y) == block.get_position():
                return True

        # If snake has run into a wall, kill it
        if board.location_on_wall(x, y):
            return True

        # Else, it's still alive
        return False

    def location_on_snake(self, x, y):
        for block in self._blocks:
            if (x, y) == block.get_position():
                return True
        return False


class Fruits:

    def __init__(self):
        self._fruits = []
        self.spawn_fruit()

    def spawn_fruit(self):

        global board
        global snake

        while len(self._fruits) < 3:

            # Spawn fruit in random location
            x = random.randint(1, 98)
            y = random.randint(1, 98)

            # Ensure that fruit isn't spawned on snake, another fruit, or wall
            while (snake.location_on_snake(x, y) and
                   not self.fruit_already_exists(x, y) and
                   not board.location_on_wall(x, y)):
                x = random.randint(1, 98)
                y = random.randint(1, 98)

            fruit = Block(x, y, red)
            self._fruits.append(fruit)

    def found_fruit(self):
        global snake
        for fruit in self._fruits:
            if fruit.get_position() == snake.get_head_position():
                self._fruits.remove(fruit)
                return True
        return False

    def fruit_already_exists(self, x, y):
        for fruit in self._fruits:
            if (x, y) == fruit.get_position():
                return True
        return False

    def draw(self):
        for fruit in self._fruits:
            fruit.draw()


class Board:

    def __init__(self, filename=None):
        self._blocks = []
        if filename is None:
            self.generate_default()

    def generate_default(self):

        for x in xrange(SCREEN_W / BS):
            self._blocks.append(Block(x, 0, blue))
            self._blocks.append(Block(x, SCREEN_H / BS - 1, blue))

        for y in xrange(SCREEN_H / BS):
            self._blocks.append(Block(0, y, blue))
            self._blocks.append(Block(SCREEN_W / BS - 1, y, blue))

        self.uniqueify()

    def uniqueify(self):
        self._blocks = list(set(self._blocks))

    def location_on_wall(self, x, y):
        for block in self._blocks:
            if (x, y) == block.get_position():
                return True
        return False

    def draw(self):
        for block in self._blocks:
            block.draw()

# Initialize display
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# Initialize objects
snake = Snake()
fruits = Fruits()
board = Board()

# Draw initial objects
snake.draw()
fruits.draw()
board.draw()

# Update display
pygame.display.update()

# Don't start until key is pressed
paused = True

# Main game loop
while True:

    # Check for key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction(L)
                paused = False
            elif event.key == pygame.K_DOWN:
                snake.set_direction(D)
                paused = False
            elif event.key == pygame.K_RIGHT:
                snake.set_direction(R)
                paused = False
            elif event.key == pygame.K_UP:
                snake.set_direction(U)
                paused = False
            elif event.key == pygame.K_SPACE:
                paused = not paused

    if paused:
        continue

    # Refresh screen and move snake
    screen.fill((0, 0, 0))
    snake.move()

    # Check if snake died
    if snake.is_dead():
        snake = Snake()  # Reset the snake
        fruits = Fruits()  # Reset the fruits
        fruits.spawn_fruit()
        paused = True  # Pause the game

    # Check if snake ate fruit
    if fruits.found_fruit():
        snake.grow()
        fruits.spawn_fruit()

    # Draw
    snake.draw()
    fruits.draw()
    board.draw()
    pygame.display.update()
    time.sleep(0.025)
