import random
import ascii_art

ZOMBIES = ["Zack", "Zed", "Ziggy", "Zoe", "Zulu"]


class Zombie:
    def __init__(self, is_player=False):
        self.name = ""
        self.is_player = is_player
        if is_player:
            print(ascii_art.logo)
            self.name = input("What is your name? ")
        self.turn_brains = 0
        self.turn_shotguns = 0
        self.round_won_brains = 0
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

    def reset_turn_stats(self, by_choice=False):
        """Resets the zombie's counting of relevant points, so it may start a next
        round with refreshed points or loose its points in case it collected 3 or more shots"""
        self.turn_ended = True
        self.turn_shotguns = 0
        self.turn_brains = 0
        if not by_choice:
            print(f"\n{self.name} lost its turn by accumulating {self.turn_shotguns} shots.")
        else:
            self.lost_turn = False
            self.turn_ended = False

    def turn_is_on(self):
        if not self.turn_ended and not self.lost_turn:
            return True
        return False

    def total_turn_brains(self):
        return self.round_won_brains + self.turn_brains

# STATIC
def create_zombie():
    """Returns a zombie object"""
    new_zombie = Zombie()
    random.shuffle(ZOMBIES)
    new_zombie.name = ZOMBIES.pop()
    return new_zombie


def set_number_of_zombies():
    """Returns a set of zombies. To be used by a Scoreboard."""
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


