from game.round_manager import RoundManager
from core.player import Player
from core.wall import Wall
from ui.controller import CLIController, AIController, RichController
from ui.renderer import CLIRenderer
from ui.rich_renderer import RichRenderer

def main():

    player1 = Player(RichController())
    player2 = Player(AIController())
    player3 = Player(AIController())
    player4 = Player(AIController())

    players = [player1, player2, player3, player4]

    renderer = RichRenderer()
    game = RoundManager(players, Wall(), renderer=renderer)
    game.play_round()


if __name__ == "__main__":
    main()
