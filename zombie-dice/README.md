*Play this game from the Terminal, so the screen may be refreshed!*

# Instructions

Players are zombies trying to eat as many brains as possible. There is a cup with 13 dice. So are its settings:

- Yellow dice: 2 footsteps, 2 brains, 2 shotguns
- Green dice: 2 footsteps, 3 brains, 1 shotgun
- Red dice: 2 footsteps, 1 brain, 3 shotguns



## One player's turn:

Consists of taking away 3 dice from the cup and counting the number of shotguns and brains. 
A player's turn may continue for as long as 3 shots are not collected, in which case the player looses its turn and the number of collected brains is set back to 0, or enough dice to play a set of 3 can still be drawn from the cup.
If a player decides to go for a next turn , all dice with footsteps must be used again, and enough dice collected from the cup, to complete a set of 3 to play again.

## Game win:

When a player collects 13 brains, the player's turn is over and the rest of players must play one last round. 
In case no one else completes 13 points, the first winner wins the game. 
However, as soon as someone does complete 13 points, one last round is played with the winner and the first one to reach 13 points wins the game.



### Bots:

- A bot that, after the first roll, randomly decides if it will continue or stop
- A bot that stops rolling after it has rolled two brains
- A bot that stops rolling after it has rolled two shotguns
- A bot that initially decides it’ll roll the dice one to four times, but will stop early if it rolls two shotguns
- A bot that stops rolling after it has rolled more shotguns than brains
- Made-up names: Zack, Zed, Zulu, Ziggy, Zoe
