import click
import zombie as z
import random
from time import sleep

SLEEP = 1.5  # 1.5


class ScoreBoard:  # to be used by DiceCup
    def __init__(self, player: z.Zombie):
        self.player = player
        self.zombies = [player] + z.set_number_of_zombies()
        self.whose_turn = -1  # player goes first, the next_player method will add 1 to it before its turn
        self.last_round = False
        self.winners = []
        self.table = []

    def next_player(self):
        self.whose_turn = (self.whose_turn + 1) % len(self.zombies)
        next_player = self.zombies[self.whose_turn]
        return next_player

    def game_win(self):
        if len(self.winners) == 1:
            if self.last_round:
                del self.zombies[self.whose_turn]
                self.last_round = False
                return False
            else:   # meaning there's already been the last
                print(f"{self.winners[0].name} won the game!! YEEEEEAAAAAH brainssssscjkaweiolfqvj")
                return True
        elif len(self.winners) == 2:
            if self.last_round:
                scores = [winner.round_won_brains for winner in self.winners]
                winner_index = self.winners.index(max(scores))
                winner = self.winners[winner_index]
                print(f"\n {winner.name} won the game with a set of "
                      f"{winner.round_won_brains} brains! YEEEEEAAAAAH brainscjkaweiolfqvj")
                return True
            else:
                if self.player in self.winners:
                    p1_score = self.winners[0].round_won_brains
                    p2_score = self.winners[1].round_won_brains

                    if p1_score == p2_score:
                        self.last_round = True
                        self.zombies = self.winners
                        return False
                    elif p1_score >= p2_score:
                        print(f"{self.winners[0].name} won the game with a set of "
                              f"{p1_score} brains! YEEEEEAAAAAH brainscjkaweiolfqvj")
                    else:
                        print(f"{self.winners[1].name} won the game with a set of "
                              f"{p2_score} brains! YEEEEEAAAAAH brainscjkaweiolfqvj")
                    return True
                else:
                    print("Other zombies ate your brain too! Sorry you lost.")
                    return True
        else:
            return False

    def display_table(self):
        if self.table == [] or len(self.table) < self.whose_turn:
            self.table.append(f"{self.zombies[self.whose_turn].name}: ")
        click.clear()
        print("\n".join(self.table))

    def update_player_row(self, new_row="total brains"):
        if new_row == "total brains":
            zombie = self.zombies[self.whose_turn]
            new_row = f"{zombie.name}: {zombie.round_won_brains}" \
                      f" brain{'s' * bool(zombie.round_won_brains)}"
        try:
            self.table[self.whose_turn] = new_row
        except IndexError:
            self.table.append(new_row)

class DiceCup():
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


# p = z.Zombie(is_player=True)
# sb = ScoreBoard(p)
# d = DiceCup(sb)
# print(d.roll_out_3())


