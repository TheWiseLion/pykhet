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
        solver = MinmaxSolver(max_evaluations=100)
        game = ClassicGame()
        iterations = 0
        color = TeamColor.silver

        while game.winner is None:
            if iterations > 10:
                self.assertTrue(True)  # Game should have ended..
            move = solver.get_move(game, color)
            game.apply_move(move)
            game.apply_laser(color)
            color = TeamColor.opposite_color(color)
            iterations += 1
