from player import Player
import click
import zombie


class ScoreBoard: #will be used by DiceCup
    def __init__(self, player: Player):
        self.player = player
        self.zombies = zombie.set_number_of_zombies() + [player]

    def set_screen(self, game_on=True):
        click.clear()
        for zombie in self.zombies:
            name = zombie.name
            shotguns = zombie.collected_shotguns
            brains = zombie.collected_brains
            footsteps = zombie.collected_footsteps
            print(f"{name}: ", end="")
            if game_on:
                if brains > 0:
                    print(f"{brains} BRAINS", end="")
                if shotguns > 0:
                    print(f"{shotguns} SHOTSUNS", end="")
                if footsteps > 0:
                    print(f"{footsteps} FOOTSTEPS", end="")
                print("\n")
            else:
                print("Turn not started")
        print('\n')





p = Player()
sb = ScoreBoard(p)

