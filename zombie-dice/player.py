from ascii_art import logo
from zombie import Zombie
import random


class Player(Zombie):
    def __init__(self):
        super().__init__()
        print(logo)
        self.name = input("What is your name? ")

    def turn(self):
        pass# TODO pegar 3 dados aleatórios do DiceCup, guardar info sobre suas cores

        # TODO observar qual combinação de brain, footstep e shotgun saiu
        #
