import random
import ascii_art

ZOMBIES = ["Zack", "Zed", "Ziggy", "Zoe", "Zulu"]


class Zombie:
    def __init__(self, is_player=False):
        self.name = ""
        self.is_player = is_player
        if is_player:
            # TODO print(ascii_art.logo)
            self.name = input("What is your name? ")
        self.turn_brains = 0
        self.turn_shotguns = 0
        self.round_won_brains = 11
        self.lost_turn = False
        self.turn_ended = False    # to be used by some examples of Zombie

    def turn(self, dice_outcome):
        """Adds the dice result to the zombie's internal counting of turn points"""
        for die in dice_outcome:
            if die[1] == "shotgun":
                self.turn_shotguns += 1
            if die[1] == "brain":
                self.turn_brains += 1
        if self.turn_shotguns >= 3:
            self.lost_turn = True
        elif self.turn_brains >= 13:
            self.turn_ended = True
        else:   # check for what sort of zombie is playing and make it play with the dice_outcome along its nature
            if not self.is_player:
                self.turn_ended = True   # placeholder, take away depending on the zombie's characteristics

    def reset_turn(self):
        if self.is_player:
            print(f"\nYou lost your turn by accumulating {self.turn_shotguns} shotguns.")
        else:
            print(f"\nZombie {self.name} lost its turn.")
        self.turn_ended = True
        self.turn_shotguns = 0
        self.turn_brains = 0
        # self.turn_footsteps = 0

    def end_turn_by_choice(self):
        self.turn_ended = True
        self.turn_shotguns = 0
        self.turn_brains = 0


# STATIC
def create_zombie():
    new_zombie = Zombie()
    random.shuffle(ZOMBIES)
    new_zombie.name = ZOMBIES.pop()
    return new_zombie


def set_number_of_zombies():
    try:
        number_of_zombies = int(input("How many zombies do you wanna play against? (Up to 5) "))
        if number_of_zombies < 0 or number_of_zombies > 5:
            raise Exception("Number of Zombies must be and integer from 1 to 5")
    except:
        return set_number_of_zombies()
    else:
        total_zumbies = []
        for i in range(number_of_zombies):
            total_zumbies.append(create_zombie())
        return total_zumbies


