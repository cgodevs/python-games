from dices import *
from zombie import *

player = Zombie(is_player=True)
dice = DiceCup()
scoreboard = ScoreBoard(player)
print("Player goes first, you are rolling the dice now!\n")


game_on = True
while game_on:  # Game round

    zombie_playing = scoreboard.next_player()
    footsteps = []

    while zombie_playing.turn_is_on() and dice.enough_dice_left(footsteps):    # One player's turn

        # --------------- Roll the Dice--------------- #
        dice.roll_out_3(considered_footsteps=footsteps)
        zombie_playing.turn(dice.result)
        dice.display_faces(scoreboard)

        # --------------- Check for Loss ----------------- #
        if zombie_playing.lost_turn:
            zombie_playing.reset_turn_stats(by_choice=False)
            break
        else:
            footsteps = [die[0] for die in dice.result if die[1] == "footstep"]  # collect footsteps to reuse the die by its color

        # -------------------- Check for Win ------------------ #
            if zombie_playing.total_turn_brains() >= 13:
                scoreboard.move_zombie_to_winners(zombie_playing)
                break

        # ------------------- Player plays ------------------- #
            if zombie_playing.is_player:
                play_again = input("\nWould you like to roll again? Y or N ").upper()
                if play_again == "N":
                    break
            if zombie_playing.turn_ended:
                break

    # -------------- Update Zombie's and game's conditions after its turn ended --------------- #
    zombie_playing.round_won_brains += zombie_playing.turn_brains
    scoreboard.set_player_round_stats()
    scoreboard.display_current_stats()
    sleep(1)
    click.clear()
    zombie_playing.reset_turn_stats(by_choice=True)

    dice.reset_cup()
    if scoreboard.last_round_complete():
        break


if len(scoreboard.winners) == 1:
    print(f"{scoreboard.winners[0][0].name} won the game!!")
else:
    # LAST ROUND BETWEEN WINNERS
    scoreboard.get_reset_for_winners()

    last_round_of_winners_on = True
    while last_round_of_winners_on:
        zombie_playing = scoreboard.next_player()
        footsteps = []

        while zombie_playing.turn_is_on() and dice.enough_dice_left(footsteps):  # One player's turn

            # --------------- Roll the Dice--------------- #
            dice.roll_out_3(considered_footsteps=footsteps)
            zombie_playing.turn(dice.result)
            dice.display_faces(scoreboard)

            # --------------- Check for Loss ----------------- #
            if zombie_playing.lost_turn:
                zombie_playing.reset_turn_stats(by_choice=False)
                break
            else:
                footsteps = [die[0] for die in dice.result if
                             die[1] == "footstep"]  # collect footsteps to reuse the die by its color

                # -------------------- Check for Win ------------------ #
                if zombie_playing.total_turn_brains() >= 13:
                    scoreboard.display_current_stats()
                    print(f"\n{zombie_playing.name} won the game!!")
                    sleep(4)
                    last_round_of_winners_on = False
                    break

                # ------------------- Player plays ------------------- #
                if zombie_playing.is_player:
                    play_again = input("\nWould you like to roll again? Y or N ").upper()
                    if play_again == "N":
                        break
                if zombie_playing.turn_ended:
                    break

        # -------------- Update Zombie's and game's conditions after its turn ended --------------- #
        zombie_playing.round_won_brains += zombie_playing.turn_brains
        scoreboard.set_player_round_stats()
        # scoreboard.display_current_stats()
        sleep(1)
        click.clear()
        zombie_playing.reset_turn_stats(by_choice=True)

        dice.reset_cup()

