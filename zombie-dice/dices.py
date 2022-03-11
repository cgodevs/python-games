import click
import zombie as z
import random
from time import sleep

SLEEP = 1  # 1.5


class ScoreBoard:  # to be used by DiceCup
    def __init__(self, player: z.Zombie):
        self.player = player
        self.zombies = [player] + z.set_number_of_zombies()
        self.whose_turn = -1  # player goes first, the next_player method will add 1 to it before its turn
        self.last_round = False
        self.winners = []   # list of [zombie object, its turn]
        self.table = []

    def next_player(self):
        self.whose_turn = (self.whose_turn + 1) % len(self.zombies)
        next_player = self.zombies[self.whose_turn]
        return next_player

    def game_ends(self):
        if len(self.winners) > 0:   # are there any winners so far?
            if self.whose_turn == self.winners[0][1] - 1:  # if the round was completed
                if len(self.winners) == 1:
                    print(f"{self.winners[0][0].name} won the game!! YEEEEEAAAAAH brainssssscjkaweiolfqvj")
                    return True
                elif len(self.winners) == 2:
                    score1 = self.winners[0][0].round_won_brains
                    score2 = self.winners[1][0].round_won_brains
                    if score1 > score2:
                        print(f"{self.winners[0][0].name} won the game!! YEEEEEAAAAAH brainssssscjkaweiolfqvj")
                    elif score1 < score2:
                        print(f"{self.winners[1][0].name} won the game!! YEEEEEAAAAAH brainssssscjkaweiolfqvj")
                    else:   # If there was a draw, consider a last turn only if the player is one of the winners
                        if self.winners[0][0].is_player or self.winners[1][0].is_player:
                            self.zombies = [winner[0] for winner in self.winners]
                            self.whose_turn = 0
                            self.last_round = True
                            return False
                        else:
                            print("There was a draw. Game Over.")
                    return True
        else:
            return False
        # if self.last_round:
        #     self.whose_turn -= 1  # não entendi essa
        #     # self.last_round = False
        #     return False


    def display_table(self):
        if self.table == [] or len(self.table) < self.whose_turn:
            self.table.append(f"{self.zombies[self.whose_turn].name}: ")
        click.clear()
        print("\n".join(self.table))

    def update_player_row(self, new_row="total brains"):
        if new_row == "total brains":
            if self.winners:
                zombie = self.zombies[-1]
            else:
                zombie = self.zombies[self.whose_turn]
            new_row = f"{zombie.name}: {zombie.round_won_brains}" \
                      f" brain{'s' * bool(zombie.round_won_brains - 1)}"
        try:
            self.table[self.whose_turn] = new_row
        except IndexError:
            self.table.append(new_row)

    def move_zombie_to_winners(self, zombie: z.Zombie):
        self.winners.append([zombie, self.whose_turn])
        del self.table[self.whose_turn]
        del self.zombies[self.whose_turn]  # winner doesn't take place in the next round
        self.whose_turn -= 2    # next player will take on the winner zombie's position, and next zombie will have the turn set higher on its turn
        if self.last_round:
            return
        print(f"\n{zombie.name} got to {zombie.round_won_brains + zombie.turn_brains} brains,"
              f" we're moving to the last round!")


class DiceCup:
    def __init__(self):
        self.faces = {
            "yellow": ["footstep", "footstep", "brain", "brain", "shotgun", "shotgun"],
            "red": ["footstep", "footstep", "brain", "shotgun", "shotgun", "shotgun"],
            "green": ["footstep", "footstep", "brain", "brain", "brain", "shotgun"]
        }
        self.dice_left = ["yellow"] * 5 + ["red"] * 4 + ["green"] * 4
        self.result = []    # [["yellow", "brain"], ["red", "shotgun"], ["green", "brain"]]

    def roll_out_3(self, consider_footsteps=None):   # picks out (actually removes) 3 dice from cup
        random.shuffle(self.dice_left)
        if consider_footsteps:
            colors = consider_footsteps + [self.dice_left.pop()] * (3 - len(consider_footsteps))
        else:
            colors = [self.dice_left.pop(), self.dice_left.pop(), self.dice_left.pop()]
        three_faces = [random.choice(self.faces[color]) for color in colors]
        result = [[colors[i], three_faces[i]] for i in range(3)]
        self.result = result

    def reset_cup(self):
        self.dice_left = ["yellow"] * 5 + ["red"] * 4 + ["green"] * 4
        self.result = []

    def display_faces(self, board: ScoreBoard):
        faces_at_display = "\nDice: "

        def add_face_to_die_result(new_face):
            """Prints current table from the scoreboard, along with a new die face.
            The reason for delay is to five the user time to see the result."""
            nonlocal faces_at_display
            board.display_table()
            print(faces_at_display, end="")
            sleep(SLEEP)
            print(new_face)
            faces_at_display += new_face

        zombie = board.zombies[board.whose_turn]
        brains = len([die[1] for die in self.result if die[1] == "brain"])
        footsteps = len([die[1] for die in self.result if die[1] == "footstep"])
        shots = len([die[1] for die in self.result if die[1] == "shotgun"])

        if brains > 0:      # the things with bool() is to decide on whether or not to make the word plural
            add_face_to_die_result(f"{brains} BRAIN{'S' * bool(brains-1)}")
        if footsteps > 0:
            if brains:
                faces_at_display += ", "
            add_face_to_die_result(f"{footsteps} FOOTSTEP{'S' * bool(footsteps-1)}...")
        if shots > 0:
            if footsteps or brains:
                faces_at_display += ", "
            add_face_to_die_result(f"{shots} SHOTGUN{'S' * bool(shots-1)}!!")
            if zombie.turn_shotguns >= 3:
                add_face_to_die_result(" ----> TURN LOST!")
                board.update_player_row("total brains")
                sleep(SLEEP)
                board.display_table()
                return

        board.update_player_row(f"{zombie.name}: {zombie.round_won_brains + zombie.turn_brains} "
                                f"brain{'s' * bool(zombie.round_won_brains + brains - 1)}, "   
                                        f"{zombie.turn_shotguns} shotgun{'s' * bool(zombie.turn_shotguns - 1)}")
        sleep(2)
        board.display_table()

