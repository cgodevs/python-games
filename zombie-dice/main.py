from dices import *
from zombie import *

player = Zombie(is_player=True)
dice = DiceCup()
scoreboard = ScoreBoard(player)

print("Player goes first, you are rolling the dice now!\n")
while True:  # Loop for the round  # TODO depois que alguém chega a 13 brains, mt coisa tá zuada, repete nome e não faz a última rodada

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
        else:
            footsteps = [die[0] for die in dice.result if die[1] == "footstep"]  # collect footsteps to reuse the die by its color

        # -------------------- Check for Win ------------------ #
            total_brains = zombie_playing.round_won_brains + zombie_playing.turn_brains
            if total_brains >= 13:
                scoreboard.move_zombie_to_winners(zombie_playing)
                if scoreboard.last_round:
                    break
                scoreboard.last_round = True
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
        if zombie_playing.turn_ended:
            break

    # -------------- Check for Game Win --------------- #
    zombie_playing.round_won_brains += zombie_playing.turn_brains
    scoreboard.update_player_row("total brains")
    scoreboard.display_table()
    if scoreboard.game_ends():
        sleep(3)
        break

    # After player's turn's ended, set conditions for next player
    zombie_playing.end_turn_by_choice()
    sleep(2)
    zombie_playing.lost_turn = False
    zombie_playing.turn_ended = False
    # if scoreboard.game_ends():
    #     sleep(3)
    #     break

    dice.reset_cup()
