import unittest

from components.types import MoveType, Move, TeamColor, Orientation
from components.types import Position
from games.game_types import ClassicGame


class TestClassicGames(unittest.TestCase):
    def setUp(self):
        self.game = ClassicGame()

    def tearDown(self):
        self.game = None

    def test_available_moves_classic(self):
        sphinx_moves_silver = self.game.get(0, 0).get_moves(self.game)
        sphinx_moves_red = self.game.get(9, 7).get_moves(self.game)

        # Sphinx Only Has 1 Move
        self.assertEquals(len(sphinx_moves_silver), 1)
        self.assertEquals(len(sphinx_moves_silver), len(sphinx_moves_red))

        pharaoh_moves_silver = self.game.get(5, 0).get_moves(self.game)
        pharaoh_moves_red = self.game.get(4, 7).get_moves(self.game)
        # three moves, zero rotations
        self.assertEquals(len(pharaoh_moves_red), 3)
        self.assertEquals(len(pharaoh_moves_red), len(pharaoh_moves_silver))

        # Test Anubises
        anubis_moves_silver = self.game.get(4, 0).get_moves(self.game)
        anubis_moves_red = self.game.get(5, 7).get_moves(self.game)
        # four move, two rotations
        self.assertEquals(len(anubis_moves_red), 6)
        self.assertEquals(len(anubis_moves_red), len(anubis_moves_silver))

        anubis_moves_silver = self.game.get(6, 0).get_moves(self.game)
        anubis_moves_red = self.game.get(3, 7).get_moves(self.game)
        # three moves, two rotations
        self.assertEquals(len(anubis_moves_red), 5)
        self.assertEquals(len(anubis_moves_red), len(anubis_moves_silver))

        # Test Scarabs
        scarab1_moves_silver = self.game.get(4, 3).get_moves(self.game)
        scarab1_moves_red = self.game.get(5, 4).get_moves(self.game)
        # 4 moves, 1 swap, 2 rotations
        self.assertEquals(len(scarab1_moves_silver), 7)
        self.assertEquals(len(scarab1_moves_red), len(scarab1_moves_silver))

        scarab2_moves_silver = self.game.get(5, 3).get_moves(self.game)
        scarab2_moves_red = self.game.get(4, 4).get_moves(self.game)
        # 5 moves, 2 rotations
        self.assertEquals(len(scarab2_moves_silver), 7)
        self.assertEquals(len(scarab2_moves_red), len(scarab2_moves_silver))

        # Test Pyramids:
        p1_silver = self.game.get(2, 1).get_moves(self.game)
        p1_red = self.game.get(7, 6).get_moves(self.game)
        # 6 moves, 2 rotations
        self.assertEquals(len(p1_silver), 8)
        self.assertEquals(len(p1_red), len(p1_silver))

        p2_silver = self.game.get(6, 5).get_moves(self.game)
        p2_red = self.game.get(3, 2).get_moves(self.game)
        # 5 moves, 2 rotations
        self.assertEquals(len(p2_red), 7)
        self.assertEquals(len(p2_red), len(p2_silver))

        p3_silver = self.game.get(0, 3).get_moves(self.game)
        p3_red = self.game.get(9, 3).get_moves(self.game)
        # 4 moves, 2 rotations
        self.assertEquals(len(p3_red), 6)
        self.assertEquals(len(p3_red), len(p3_silver))

        p3_silver = self.game.get(0, 4).get_moves(self.game)
        p3_red = self.game.get(9, 4).get_moves(self.game)
        # 4 moves, 2 rotations
        self.assertEquals(len(p3_red), 6)
        self.assertEquals(len(p3_red), len(p3_silver))

        p4_silver = self.game.get(2, 3).get_moves(self.game)
        p4_red = self.game.get(7, 4).get_moves(self.game)
        # 6 moves, 2 rotations
        self.assertEquals(len(p4_red), 8)
        self.assertEquals(len(p4_red), len(p4_silver))

    def test_destroy_pieces_classic(self):
        self.game.apply_move(Move(MoveType.move, Position(2, 1), Position(2, 0)))
        self.game.apply_laser(TeamColor.silver)

        self.game.apply_move(Move(MoveType.move, Position(7, 6), Position(7, 7)))
        self.game.apply_laser(TeamColor.red)

        self.game.apply_move(Move(MoveType.rotate, Position(0, 0), Orientation.right))
        self.game.apply_laser(TeamColor.silver)

        self.assertEquals(len(self.game.squares_with_pieces_of_color(TeamColor.silver)),
                          len(self.game.squares_with_pieces_of_color(TeamColor.red)) + 1)

        self.game.apply_move(Move(MoveType.rotate, Position(9, 7), Orientation.left))
        self.game.apply_laser(TeamColor.red)
        self.assertEquals(len(self.game.squares_with_pieces_of_color(TeamColor.silver)),
                          len(self.game.squares_with_pieces_of_color(TeamColor.red)))

    def test_red_wins_classic(self):
        self.game.apply_move(Move(MoveType.move, Position(0, 3), Position(0, 2)))
        self.game.apply_move(Move(MoveType.move, Position(3, 2), Position(5, 2)))
        self.game.apply_laser(TeamColor.silver)
        self.assertEquals(self.game.winner, TeamColor.red)

    def simple_silver_win(self):
        pass

    def test_same_number_moves(self):
        red_moves = self.game.get_available_moves(TeamColor.red)
        silver_moves = self.game.get_available_moves(TeamColor.silver)
        self.assertEquals(len(red_moves), len(silver_moves))
