import unittest

from components.board import KhetBoard, Piece, PieceType, Position, Orientation, TeamColor, LaserPathType


class TestBoardMethods(unittest.TestCase):
    def setUp(self):
        self.board = KhetBoard()

    def tearDown(self):
        self.board = None

    def test_set(self):
        self.board.set_piece(Position(0, 0), Piece(PieceType.sphinx, TeamColor.silver, Orientation.down))
        self.board.set_piece(Position(9, 7), Piece(PieceType.sphinx, TeamColor.red, Orientation.up))
        self.assertTrue(self.board.squares[0][0].piece.type is PieceType.sphinx)
        self.assertTrue(self.board.squares[9][7].piece.type is PieceType.sphinx)

    def test_get_pieces(self):
        self.board.set_piece(Position(0, 0), Piece(PieceType.sphinx, TeamColor.silver, Orientation.down))
        self.board.set_piece(Position(9, 7), Piece(PieceType.sphinx, TeamColor.red, Orientation.up))
        self.board.set_piece(Position(8, 6), Piece(PieceType.anubis, TeamColor.red, Orientation.up))

        self.assertTrue(len(self.board.squares_with_pieces_of_color(TeamColor.red)) is 2)
        self.board.remove_piece(Position(9, 7))
        self.assertTrue(len(self.board.squares_with_pieces_of_color(TeamColor.red)) is 1)


    def test_remove(self):
        self.board.set_piece(Position(0, 0), Piece(PieceType.sphinx, TeamColor.silver, Orientation.down))
        self.board.set_piece(Position(9, 7), Piece(PieceType.sphinx, TeamColor.red, Orientation.up))
        self.board.remove_piece(Position(9, 7))
        self.board.remove_piece(Position(0, 0))
        self.assertTrue(self.board.squares[0][0].piece is None)
        self.assertTrue(self.board.squares[9][7].piece is None)

    def test_bounce_path(self):
        self.board.set_piece(Position(0, 0), Piece(PieceType.sphinx, TeamColor.silver, Orientation.down))
        self.board.set_piece(Position(9, 7), Piece(PieceType.sphinx, TeamColor.red, Orientation.up))
        self.board.set_piece(Position(9, 4), Piece(PieceType.pyramid, TeamColor.red, Orientation.down))
        self.board.set_piece(Position(0, 4), Piece(PieceType.pyramid, TeamColor.silver, Orientation.up))

        self.assertTrue(self.board.squares[0][0].piece.type is PieceType.sphinx)
        self.assertTrue(self.board.squares[9][7].piece.type is PieceType.sphinx)

        red_path = self.board.get_laser_path(TeamColor.red)
        silver_path = self.board.get_laser_path(TeamColor.silver)
        self.assertTrue(red_path[-1][1] is LaserPathType.hit and red_path[-1][0].x is 0)
        self.assertTrue(silver_path[-1][1] is LaserPathType.hit and silver_path[-1][0].x is 9)

    def test_bounce_path_complex(self):
        # Test should involve every mirror in every direction
        self.board.set_piece(Position(0, 0), Piece(PieceType.sphinx, TeamColor.silver, Orientation.down))
        self.board.set_piece(Position(9, 7), Piece(PieceType.sphinx, TeamColor.red, Orientation.up))
        self.board.set_piece(Position(9, 4), Piece(PieceType.scarab, TeamColor.red, Orientation.down))
        self.board.set_piece(Position(8, 4), Piece(PieceType.scarab, TeamColor.red, Orientation.up))
        self.board.set_piece(Position(8, 3), Piece(PieceType.pyramid, TeamColor.red, Orientation.down))
        self.board.set_piece(Position(1, 3), Piece(PieceType.scarab, TeamColor.silver, Orientation.left))
        self.board.set_piece(Position(1, 4), Piece(PieceType.scarab, TeamColor.silver, Orientation.right))
        self.board.set_piece(Position(0, 4), Piece(PieceType.pyramid, TeamColor.silver, Orientation.up))

        red_path = self.board.get_laser_path(TeamColor.red)
        self.assertTrue(red_path[-1][1] is LaserPathType.hit and red_path[-1][0].x is 0)

    def test_board_serialization(self):
        self.board.set_piece(Position(0, 0), Piece(PieceType.sphinx, TeamColor.silver, Orientation.down))
        self.board.set_piece(Position(9, 7), Piece(PieceType.sphinx, TeamColor.red, Orientation.up))
        self.board.set_piece(Position(9, 4), Piece(PieceType.pyramid, TeamColor.red, Orientation.down))
        self.board.set_piece(Position(0, 4), Piece(PieceType.pyramid, TeamColor.silver, Orientation.up))

        squares = self.board.to_serialized_squares()
        board = KhetBoard.from_serialized_squares(squares)
        self.assertTrue(board.get(0, 0).piece.color is TeamColor.silver)

        squares = self.board.to_serialized_squares_full()
        board = KhetBoard.from_serialized_squares(squares)
        self.assertTrue(board.get(0, 0).piece.color is TeamColor.silver)

if __name__ == '__main__':
    unittest.main()
