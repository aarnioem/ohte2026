from game.round_manager import RoundManager
from core.player import Player
from core.wall import Wall
from ui.controller import CLIController, AIController, RichController
from ui.renderer import CLIRenderer
from ui.rich_renderer import RichRenderer

def main():

    renderer = RichRenderer()
    wall = Wall()

    player1 = Player(RichController(renderer))
    player2 = Player(AIController())
    player3 = Player(AIController())
    player4 = Player(AIController())

    players = [player1, player2, player3, player4]

    game = RoundManager(players=players, wall=wall, renderer=renderer)
    renderer.start_live()
    try:
        game.play_round()
    finally:
        renderer.stop_live()

if __name__ == "__main__":
    main()
