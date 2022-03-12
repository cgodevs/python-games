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
        self.last_round_turns = 0
        self.winners = []   # list of [zombie object, its turn]
        self.stats = [zombie.get_round_stats()
                      for zombie in self.zombies]    # keeps track of zombie's stats, as many items as there are zombies

    def next_player(self):
        """Returns the next zombie object in the list of inner zombies making up the scoreboard"""
        self.whose_turn = (self.whose_turn + 1) % len(self.zombies)
        next_player = self.zombies[self.whose_turn]
        return next_player

    def display_current_stats(self):
        """CLeans screen and displays inner set of all zombie's stats"""
        click.clear()
        print("\n".join(self.stats))

    def set_player_round_stats(self):
        """Modify a player's stats with the full amount of guaranteed brains achieved"""
        zombie_playing = self.zombies[self.whose_turn]
        self.stats[self.whose_turn] = zombie_playing.get_round_stats()

    def set_player_turn_stats(self, msg: str):
        """Modify a player's stats for the message in the argument"""
        self.stats[self.whose_turn] = msg

    def move_zombie_to_winners(self, zombie: z.Zombie):
        self.winners.append([zombie, self.whose_turn])
        del self.zombies[self.whose_turn]  # winner doesn't take place in the next round
        del self.stats[self.whose_turn]
        self.whose_turn -= 1  # next player will take on the winner's current position
        if len(self.winners) == 1:
            print(f"\n{zombie.name} got to {zombie.round_won_brains + zombie.turn_brains} brains,"
              f" we're moving to the last round!")
            self.last_round = True
        else:
            print(f"\n{zombie.name} got to 13 brains too!! The two winners will play one last round alone.")
        sleep(2)

    def last_round_complete(self):
        if self.last_round:
            if len(self.winners) == 2:
                return True
            if self.last_round_turns == len(self.zombies):
                return True
            else:
                self.last_round_turns += 1
        return False

    def get_reset_for_winners(self):
        self.zombies = []
        self.whose_turn = -1
        for winner in self.winners:
            winner[0].reset_turn_stats(by_choice=True)
            winner[0].round_won_brains = 12
            self.zombies.append(winner[0])
        self.stats = [zombie.get_round_stats() for zombie in self.zombies]


class DiceCup:
    def __init__(self):
        self.faces = {
            "yellow": ["footstep", "footstep", "brain", "brain", "shotgun", "shotgun"],
            "red": ["footstep", "footstep", "brain", "shotgun", "shotgun", "shotgun"],
            "green": ["footstep", "footstep", "brain", "brain", "brain", "shotgun"]
        }
        self.dice_left = ["yellow"] * 5 + ["red"] * 4 + ["green"] * 4
        self.result = []    # [["yellow", "brain"], ["red", "shotgun"], ["green", "brain"]]

    def roll_out_3(self, considered_footsteps):
        """Picks out (actually removes) 3 dice from cup"""
        random.shuffle(self.dice_left)
        if considered_footsteps:
            colors = considered_footsteps + [self.dice_left.pop()] * (3 - len(considered_footsteps))
        else:
            colors = [self.dice_left.pop(), self.dice_left.pop(), self.dice_left.pop()]
        three_faces = [random.choice(self.faces[color]) for color in colors]
        result = [[colors[i], three_faces[i]] for i in range(3)]
        self.result = result

    def reset_cup(self):
        self.dice_left = ["yellow"] * 5 + ["red"] * 4 + ["green"] * 4
        self.result = []

    def enough_dice_left(self, turn_footsteps):
        return len(self.dice_left) + len(turn_footsteps) >= 3

    def display_faces(self, board: ScoreBoard):
        """Repeatedly displays the scoreboard stats, along with a new face for the dice result.
        Time between each display of a die face means to add suspense and simulate a die roll a little better"""
        faces_at_display = "\nDice: "

        def add_face_to_die_result(new_face):
            """Prints current table from the scoreboard, along with a new die face.
            The reason for delay is to five the user time to see the result."""
            nonlocal faces_at_display
            board.display_current_stats()
            print(faces_at_display, end="")
            sleep(SLEEP)
            print(new_face)
            faces_at_display += new_face

        zombie = board.zombies[board.whose_turn]
        brains = len([die[1] for die in self.result if die[1] == "brain"])
        footsteps = len([die[1] for die in self.result if die[1] == "footstep"])
        shots = len([die[1] for die in self.result if die[1] == "shotgun"])

        if brains > 0:      # the thing with bool() is to decide on whether or not to make the word plural
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
                board.set_player_round_stats()
                sleep(2)
                return

        board.set_player_turn_stats(f"{zombie.name}: {zombie.round_won_brains + zombie.turn_brains} brain"
                                    f"{'s' * bool(zombie.round_won_brains + brains - 1)}, "   
                                    f"{zombie.turn_shotguns} shotgun"
                                    f"{'s' * bool(zombie.turn_shotguns - 1)}")
        sleep(2)
        board.display_current_stats()


