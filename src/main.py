from game.round_manager import RoundManager
from core.player import Player
from core.wall import Wall
from ui.cli import CLI

def main():

    ui = CLI()

    player1 = Player(True)
    player2 = Player(False)
    player3 = Player(False)
    player4 = Player(False)

    players = [player1, player2, player3, player4]

    game = RoundManager(players, ui, Wall())
    game.play_round()


if __name__ == "__main__":
    main()
