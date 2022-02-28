import random
import turtle

from snake import Snake
from scoreboard import Scoreboard
from food import Food

"""
IDEAS: one pill disables colisions with walls
"""


class EffectsManager():

    def __init__(self, snake: Snake, food: Food, scoreboard: Scoreboard):
        self.snake = snake
        self.food = food
        self.scoreboard = scoreboard

        self.effect_on = False
        self.current_effect = None
        self.counter = 0  # this helps the pink_pill and blue_pill effects
        self.repeat_effect_on = False

        # TODO add in purple
        self.food_specialty = {
            "available_colors": ["DeepPink", "yellow", "red", "green", "blue"],
            "first_position": (random.choice(list(range(-280, 280, 20))), random.choice(list(range(-280, 280, 20)))),
            "second_position": (random.choice(list(range(-280, 280, 20))), random.choice(list(range(-280, 280, 20))))
        }

    def attempt_effect(self):
        """Turns on a power with a 50% chance.
        If so, sets a food color and its corresponding effect for the next time user eats the colored food"""
        if self.snake.speed % 10 == 0:  # will guarantee the speed of snakes slowly increases as it grows
            self.snake.speed -= 0.015
        if random.randint(0, 1) == 0:
            self.current_effect = random.choice(self.food_specialty["available_colors"])
            if self.current_effect == "purple":
                self.food.color("purple")
            elif self.current_effect == "DeepPink":
                self.food.color("DeepPink")
            elif self.current_effect == "red":
                self.food.color("red")
            elif self.current_effect == "green":
                self.food.color("green")
            elif self.current_effect == "yellow":
                self.food.color("yellow")
            elif self.current_effect == "blue":
                self.food.color("blue")
            self.effect_on = True

    def turn_off(self):
        """Undoes the current pill effect"""
        self.effect_on = False
        self.apply_effect()
        self.current_effect = None

    def apply_effect(self):
        # ------------------ Repeating Actions ------------------- #
        self.food.color("white")  # back to the default color, Angela's is blue
        if self.current_effect == "DeepPink":
            self.pink_pill()
            return
        elif self.current_effect == "blue":
            self.blue_pill()
            return

        # ------------------ One Time Actions ----------------- #
        elif self.current_effect == "red":
            self.red_pill()
        elif self.current_effect == "purple":
            self.purple_pill()
        elif self.current_effect == "yellow":
            self.yellow_pill()
        elif self.current_effect == "green":
            self.green_pill()
        self.effect_on = False

    # ------------------------- "PILLS" ------------------------- #

    def red_pill(self):
        """increases speed"""
        if self.effect_on:
            self.snake.speed -= 0.05
        else:
            self.snake.speed += 0.05

    def green_pill(self):
        """increases score by 5 points"""
        if self.effect_on:
            self.scoreboard.score += 4
            self.scoreboard.clear()
            self.scoreboard.update_scoreboard()

    def yellow_pill(self):
        """Hides all segments but the head. Body still exists!"""
        if self.effect_on:
            for seg in self.snake.segments[1:]:
                seg.hideturtle()
        else:
            for seg in self.snake.segments[1:]:
                seg.showturtle()

    def blue_pill(self):
        """food appears at 2 places from time to time"""
        if self.effect_on:
            self.repeat_effect_on = True
            self.food.color("white")
            if self.counter == 0:
                self.food.goto(self.food_specialty["first_position"])
                self.counter = 1
            else:
                self.food.goto(self.food_specialty["second_position"])
                self.counter = 0
        else:
            self.counter = 0
            self.repeat_effect_on = False

        if self.snake.head.distance(self.food) < 15:  # main.py would not detect a collision with food for blue
            self.effect_on = False
            self.repeat_effect_on = False
            self.current_effect = None
            self.food.refresh()
            self.food_specialty["first_position"] = (random.choice(list(range(-280, 280, 20))),
                                                     random.choice(list(range(-280, 280, 20))))
            self.food_specialty["second_position"] = (random.choice(list(range(-280, 280, 20))),
                                                      random.choice(list(range(-280, 280, 20))))

    def pink_pill(self):
        """Colors the snake in a rainbow fashion and makes it move a bit faster"""
        if self.effect_on:
            self.repeat_effect_on = True
            self.snake.speed = 0.05
            rainbow_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
            for seg_index in range(len(self.snake.segments)):
                chosen_color = rainbow_colors[(seg_index + self.counter) % len(rainbow_colors)]
                self.snake.segments[seg_index].color(chosen_color)
            self.counter += 1
        else:
            self.snake.speed = 0.1
            self.counter = 0
            self.repeat_effect_on = False
            self.food.refresh()
            for seg in self.snake.segments:
                seg.color("white")

    def purple_pill(self):
        """moves the snake to an spiral shape starting from the center"""
        pass


