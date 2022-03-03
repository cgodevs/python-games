from dices import *
from zombie import *

player = Zombie(is_player=True)
dice = DiceCup()
scoreboard = ScoreBoard(player)

last_round = False
print("Player goes first, you are rolling the dice now!\n")


# One round
while True: # TODO não estou conseguindo acumular brains, mesmo passando a vez

    zombie_playing = scoreboard.next_player()
    footsteps = []

    is_valid_turn = not zombie_playing.turn_ended and not zombie_playing.lost_turn and \
                    len(dice.dice_left) + len(footsteps) >= 3   # all dice available must be enough to roll 3

    while is_valid_turn:
        # ------------ Roll the Dice------------ #
        if footsteps:
            dice.roll_out_3(consider_footsteps=footsteps)
            footsteps = []
        else:
            dice.roll_out_3()
        dice.display_faces(scoreboard)
        zombie_playing.turn(dice.result)

        # ----------- Check for Dice OutCome -------------- #
        if zombie_playing.turn_ended:
            scoreboard.display_table()
        if zombie_playing.lost_turn:
            zombie_playing.reset_turn(dice.result)
            scoreboard.display_table()
            break
        else:
            for die in dice.result:     # collect footsteps, so the zombie can reuse the die by its color
                if die[1] == "footstep":
                    footsteps.append(die[0])

            # ------------------- Player plays ------------------- #
            #if zombie_playing.turn_ended:
                #scoreboard.display_table()     # to be used by some zombies
            if zombie_playing.is_player and not zombie_playing.turn_ended:
                choice = input("Would you like to roll again? Y or N ").upper()
                if choice == "N":
                    zombie_playing.end_turn_by_choice()
                    scoreboard.display_table()
                    break

            # -------------------- Check for Win ------------------ #
            if zombie_playing.collected_brains >= 13:
                scoreboard.last_round = True
                scoreboard.winners.append(zombie_playing)
                print(f"{zombie_playing.name} achieved {zombie_playing.collected_brains},"
                      f" we're moving to the last round!")
                break

    zombie_playing.lost_turn = False
    zombie_playing.turn_ended = False
    # if zombie_playing == scoreboard.zombies[-1]:
        # scoreboard.table = []
    end = scoreboard.check_for_winner()
    if end or scoreboard.last_round:
        break


    dice.reset_cup()
