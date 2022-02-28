from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 20, "normal")

with open("data.txt") as file:
    HIGHSCORE = int(file.read())

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.high_score = HIGHSCORE
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        if self.score > self.high_score:
            with open("data.txt", mode="w") as file:
                self.high_score = self.score
                file.write(str(self.high_score))
        self.write(f"Score: {self.score}  High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()
