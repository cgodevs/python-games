from dices import *
from zombie import *

player = Zombie(is_player=True)
dice = DiceCup()
scoreboard = ScoreBoard(player)

print("Player goes first, you are rolling the dice now!\n")
while True:  # Loop for the round

    zombie_playing = scoreboard.next_player()
    footsteps = []
    scoreboard.update_player_row("total brains")

    while not zombie_playing.turn_ended and not zombie_playing.lost_turn and \
                    len(dice.dice_left) + len(footsteps) >= 3:    # Loop for one player's turn
        # --------------- Roll the Dice--------------- #
        if footsteps:
            dice.roll_out_3(consider_footsteps=footsteps)
        else:
            dice.roll_out_3()
        zombie_playing.turn(dice.result)
        dice.display_faces(scoreboard)

        # --------------- Check for Loss ----------------- #
        if zombie_playing.lost_turn:
            zombie_playing.reset_turn()
            break
        if zombie_playing.turn_ended or zombie_playing.lost_turn:
        #     # scoreboard.update_player_row("total brains")
        #     scoreboard.display_table()
        #     sleep(2)
            break
        else:
            footsteps = [die[0] for die in dice.result if die[1] == "footstep"]  # collect footsteps to reuse the die by its color

        # -------------------- Check for Win ------------------ #
            total_brains = zombie_playing.round_won_brains + zombie_playing.turn_brains
            if total_brains >= 13:
                scoreboard.last_round = True
                scoreboard.winners.append(zombie_playing)
                print(f"\n{zombie_playing.name} got to {total_brains} brains,"
                      f" we're moving to the last round!")
                sleep(2)
                break

        # ------------------- Player plays ------------------- #
            if zombie_playing.is_player:
                choice = input("\nWould you like to roll again? Y or N ").upper()
                if choice == "N":
                    scoreboard.display_table()
                    break
                else:
                    continue

    # After player's turn's ended
    zombie_playing.round_won_brains += zombie_playing.turn_brains
    zombie_playing.end_turn_by_choice()
    sleep(2)
    scoreboard.update_player_row("total brains")
    scoreboard.display_table()
    zombie_playing.lost_turn = False
    zombie_playing.turn_ended = False
    if scoreboard.game_win():
        sleep(3)
        break


    dice.reset_cup()
