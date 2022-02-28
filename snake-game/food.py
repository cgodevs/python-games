from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.8, stretch_wid=0.8)
        self.color("white")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        # x and y are chosen out of multiples of 20, so the food can always be aligned with the snake
        random_x = random.choice(list(range(-280, 280, 20)))
        random_y = random.choice(list(range(-280, 280, 20)))
        self.goto(random_x, random_y)
