import unittest

from pykhet.components.board import TeamColor
from pykhet.solvers.minmax import MinmaxSolver, CMinMaxSolver

from pykhet.games.game_types import ClassicGame


class TestClassicGameSolver(unittest.TestCase):
    def setUp(self):
        self.game = ClassicGame()

    def tearDown(self):
        self.game = None

    # def test_simple_game(self):
    #     solver = MinmaxSolver(max_evaluations=100)
    #     game = ClassicGame()
    #     iterations = 0
    #     color = TeamColor.silver
    #
    #     while game.winner is None:
    #         if iterations > 10:
    #             self.assertTrue(True)  # Game should have ended..
    #         move = solver.get_move(game, color)
    #         game.apply_move(move)
    #         game.apply_laser(color)
    #         color = TeamColor.opposite_color(color)
    #         iterations += 1

    def test_c_minmax(self):
        solver1 = CMinMaxSolver(max_evaluations=200000)
        solver2 = CMinMaxSolver(max_evaluations=1000)
        game = ClassicGame()
        iterations = 0
        color = TeamColor.silver

        while game.winner is None:
            if color is TeamColor.red:
                move = solver1.get_move(game, color)
            else:
                move = solver2.get_move(game, color)
            game.apply_move(move)
            game.apply_laser(color)
            color = TeamColor.opposite_color(color)
            iterations += 1

        # Red should win as it has a significant advantage
        self.assertTrue(game.winner is TeamColor.red)
