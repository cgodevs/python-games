from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
from effects import EffectsManager

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()
effects = EffectsManager(snake, food, scoreboard)

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    snake.speed_checkup()
    snake.move()

    #Detect collision with food.
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

        # Sets an effect by chance
        if effects.current_effect is None:  # setting food color and turning on effect for current food refreshed
            effects.attempt_effect()        # effect_on = True; effects.current_effect = "xxx"
        elif effects.counter > 0:           # used by the pink effect
            effects.turn_off()
        elif effects.current_effect is not None:  # effect is finally activated when you get the now colored food
            if effects.effect_on:
                effects.apply_effect()
            else:
                effects.turn_off()

    #Detect collision with wall.
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 300 or snake.head.ycor() < -290:
        game_is_on = False
        scoreboard.game_over()

    #Detect collision with tail.
    for segment in snake.segments:
        if segment == snake.head:
            pass
        elif snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()

    # Reocurring effects (some must keep repeating)
    if effects.repeat_effect_on:
        effects.apply_effect()

screen.exitonclick()
