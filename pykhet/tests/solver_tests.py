import unittest

from pykhet.components.board import TeamColor
from pykhet.solvers.minmax import MinmaxSolver

from pykhet.games.game_types import ClassicGame


class TestClassicGameSolver(unittest.TestCase):
    def setUp(self):
        self.game = ClassicGame()

    def tearDown(self):
        self.game = None

    def test_simple_game(self):
        solver = MinmaxSolver()
        game = ClassicGame()
        iterations = 0
        color = TeamColor.silver

        while game.winner is None:
            if iterations > 300:
                self.assertTrue(False)  # Game should have ended..
            move = solver.get_move(game, color)
            game.apply_move(move)
            game.apply_laser(color)
            print len(game.squares_with_pieces_of_color(TeamColor.silver)), " vs ", \
                len(game.squares_with_pieces_of_color(TeamColor.red))
            color = TeamColor.opposite_color(color)
            iterations += 1
