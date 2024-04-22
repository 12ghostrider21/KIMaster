import Arena
from TicTacToeGame import TicTacToeGame
from TicTacToePlayers import RandomPlayer, HumanTicTacToePlayer


human_vs_cpu = True

g = TicTacToeGame(3)

# all players
rp = RandomPlayer(g).play
hp = HumanTicTacToePlayer(g).play


arena = Arena.Arena(rp, hp, g, display=TicTacToeGame.display)

print(arena.playGames(2, verbose=True))
