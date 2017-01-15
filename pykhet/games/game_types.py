# Game is composed of a board, initial positions, and valid moves
import abc

from pykhet.components import KhetBoard, Position, Piece, PieceType, TeamColor, Orientation


class Game(KhetBoard):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Game, self).__init__()
        self.winner = None

    def apply_laser(self, color):
        """
        Returns path the laser took and piece destroyed (if any)
        :param color:
        :return:
        """
        if self.winner is not None:
            raise RuntimeError("Game is already complete " + str(self.winner.value) + " won")
        results = {}
        path, piece = super(Game, self).apply_laser(color)

        path_results = []
        for p in path:
            path_results.append({"position": {"x": p[0].x, "y": p[0].y}, "type": p[1].value})

        if piece is not None:
            results["destroyed"] = piece.to_dictionary()
            if piece.type is PieceType.pharaoh:
                self.winner = TeamColor.opposite_color(piece.color)
                results["winner"] = self.winner.value

        results["path"] = path_results
        return results


class ClassicGame(Game):
    def __init__(self):
        super(ClassicGame, self).__init__()
        # Set all piece locations

        # Sphinx Locations:
        self.set_piece(Position(0, 0), Piece(PieceType.sphinx, TeamColor.silver, Orientation.down))
        self.set_piece(Position(9, 7), Piece(PieceType.sphinx, TeamColor.red, Orientation.up))

        # Scarab Locations:
        self.set_piece(Position(4, 3), Piece(PieceType.scarab, TeamColor.silver, Orientation.up))
        self.set_piece(Position(5, 3), Piece(PieceType.scarab, TeamColor.silver, Orientation.left))

        self.set_piece(Position(4, 4), Piece(PieceType.scarab, TeamColor.red, Orientation.right))
        self.set_piece(Position(5, 4), Piece(PieceType.scarab, TeamColor.red, Orientation.down))

        # Pyramid Locations:
        # left cluster (silver side)
        self.set_piece(Position(0, 3), Piece(PieceType.pyramid, TeamColor.silver, Orientation.up))
        self.set_piece(Position(0, 4), Piece(PieceType.pyramid, TeamColor.silver, Orientation.right))
        self.set_piece(Position(2, 3), Piece(PieceType.pyramid, TeamColor.red, Orientation.down))
        self.set_piece(Position(2, 4), Piece(PieceType.pyramid, TeamColor.red, Orientation.left))

        # right cluster (red side)
        self.set_piece(Position(7, 3), Piece(PieceType.pyramid, TeamColor.silver, Orientation.right))
        self.set_piece(Position(7, 4), Piece(PieceType.pyramid, TeamColor.silver, Orientation.up))
        self.set_piece(Position(9, 3), Piece(PieceType.pyramid, TeamColor.red, Orientation.left))
        self.set_piece(Position(9, 4), Piece(PieceType.pyramid, TeamColor.red, Orientation.down))

        # Two Corner Pieces:
        # Silver side (left)
        self.set_piece(Position(2, 1), Piece(PieceType.pyramid, TeamColor.silver, Orientation.down))
        self.set_piece(Position(3, 2), Piece(PieceType.pyramid, TeamColor.red, Orientation.left))

        # Red side (right)
        self.set_piece(Position(7, 6), Piece(PieceType.pyramid, TeamColor.red, Orientation.up))
        self.set_piece(Position(6, 5), Piece(PieceType.pyramid, TeamColor.silver, Orientation.right))

        # Pharaoh lines:
        # Silver
        self.set_piece(Position(4, 0), Piece(PieceType.anubis, TeamColor.silver, Orientation.down))
        self.set_piece(Position(5, 0), Piece(PieceType.pharaoh, TeamColor.silver, Orientation.down))
        self.set_piece(Position(6, 0), Piece(PieceType.anubis, TeamColor.silver, Orientation.down))
        self.set_piece(Position(7, 0), Piece(PieceType.pyramid, TeamColor.silver, Orientation.up))

        # Red
        self.set_piece(Position(2, 7), Piece(PieceType.pyramid, TeamColor.red, Orientation.left))
        self.set_piece(Position(3, 7), Piece(PieceType.anubis, TeamColor.red, Orientation.up))
        self.set_piece(Position(4, 7), Piece(PieceType.pharaoh, TeamColor.red, Orientation.up))
        self.set_piece(Position(5, 7), Piece(PieceType.anubis, TeamColor.red, Orientation.up))
