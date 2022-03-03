import click
import zombie as z
import random
from time import sleep
from prettytable import PrettyTable

SLEEP = 1 #1.5

"""
ALL ZOMBIES --> SCOREBOARD --> DICE (ascending order of information received)
"""

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

    def check_for_winner(self):
        if len(self.winners) == 1:
            if not self.last_round:
                print(f"{self.winners[0].name} won the game!! YEEEEEAAAAAH brainscjkaweiolfqvj")
                return True
            else:
                print(f"{self.winners[0].name} got to 13 brains!! We're moving to the last round now. ")
                self.last_round = True
                return False
        elif len(self.winners) == 2:
            if self.last_round:
                scores = [winner.collected_brains for winner in self.winners]
                winner_index = self.winners.index(max(scores))
                winner = self.winners[winner_index]
                print(f"{winner.name} won the game with a set of "
                      f"{winner.collected_brains} brains! YEEEEEAAAAAH brainscjkaweiolfqvj")
                return True
            else:
                if self.player in self.winners:
                    p1_score = self.winners[0].collected_brains
                    p2_score = self.winners[1].collected_brains

                    if p1_score == p2_score:
                        self.last_round = True
                        self.zombies = self.winners
                        return False
                    elif p1_score >= p2_score:
                        print(f"{self.winners[0].name} won the game with a set of "
                              f"{self.winners[0].collected_brains} brains! YEEEEEAAAAAH brainscjkaweiolfqvj")
                    else:
                        print(f"{self.winners[1].name} won the game with a set of "
                              f"{self.winners[0].collected_brains} brains! YEEEEEAAAAAH brainscjkaweiolfqvj")
                    self.last_round = True
                    return True
                else:
                    print("Other zombies ate your brain too! Sorry you lost.")
                    return True
        else:
            return False

    def display_table(self):
        current_zombie_playing_name = self.zombies[self.whose_turn].name
        if self.table == [] or len(self.table) < self.whose_turn:
            self.table.append(f"{current_zombie_playing_name}: ")

        click.clear()
        print("\n".join(self.table))

    def update_player_row(self, new_row):
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
        self.faces_at_display = "\nDice: "

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
        self.faces_at_display = "\nDice: "

    def display_faces(self, board: ScoreBoard):
        def suspense(time=SLEEP):
            sleep(time)
            board.display_table()

        def show_die_face(new_face):
            board.display_table()
            print(self.faces_at_display, end="")
            sleep(SLEEP)
            print(new_face)
            self.faces_at_display += new_face

        zombie_player = board.zombies[board.whose_turn]
        brains = len([die[1] for die in self.result if die[1] == "brain"])
        footsteps = len([die[1] for die in self.result if die[1] == "footstep"])
        shots = len([die[1] for die in self.result if die[1] == "shotgun"])

        if brains > 0:
            show_die_face(f"{brains} BRAINS")
        if footsteps > 0:
            if brains:
                self.faces_at_display += ", "
            show_die_face(f"{footsteps} FOOTSTEPS...")
        if shots > 0:
            if footsteps or brains:
                self.faces_at_display += ", "
            show_die_face(f"{shots} SHOTGUNS!!")
            if shots >= 3:
                show_die_face(" ----> TURN LOST!")
                board.update_player_row(f"{zombie_player.name}: {zombie_player.collected_brains} brain{'s'*bool(shots)}")
                suspense()
                return

        board.update_player_row(f"{zombie_player.name}: {zombie_player.collected_brains + brains} "
                                f"brain{'s'*bool(zombie_player.collected_brains + brains)}, "   # to place letter "s" 
                                        f"{zombie_player.collected_shotguns + shots} "
                                f"shotgun{'s'*bool(zombie_player.collected_shotguns + shots)}")
        suspense(1.5)
        self.faces_at_display = "\nDice: "

# p = z.Zombie(is_player=True)
# sb = ScoreBoard(p)
# d = DiceCup(sb)
# print(d.roll_out_3())


