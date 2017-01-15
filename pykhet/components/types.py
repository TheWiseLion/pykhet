from enum import Enum


class LaserPathType(Enum):
    hit = "hit"
    bounce = "bounce"
    through = "pass"
    # destroy = "destroy"


class MoveType(Enum):
    rotate = "ROTATE"
    move = "MOVE"
    swap = "SWAP"


class Move(object):
    def __init__(self, move_type, move_position, move_value):
        self.type = move_type
        self.position = move_position
        self.value = move_value

    def to_dictionary(self):
        value = self.value
        if not isinstance(value, (int, long, float)):
            value = value.to_dictionary()

        return {"type": self.type.value, "position": self.position.to_dictionary(), "value": value}

    @staticmethod
    def from_dictionary(value):
        move_type = MoveType(value["type"])
        position = Position(value["position"]["x"], value["position"]["y"])
        value = value["value"]  # Notice the aliasing...
        if move_type is not MoveType.rotate:
            value = Position(value["x"], value["y"])
        return Move(move_type, position, value)

    def __str__(self):
        return "{ T: " + str(self.type.value) + ", P: " + str(self.position) + ", V: " + str(self.value) + "}"


class Orientation(Enum):
    """Class for orientations"""
    up = 0
    left = 90
    right = 270
    down = 180
    none = -1

    @staticmethod
    def from_position(position1, position2):
        return Orientation.up

    @staticmethod
    def next_position(position, direction):
        if direction is Orientation.up:
            return Position(position.x, position.y - 1)

        if direction is Orientation.down:
            return Position(position.x, position.y + 1)

        if direction is Orientation.left:
            return Position(position.x - 1, position.y)

        if direction is Orientation.right:
            return Position(position.x + 1, position.y)

    @staticmethod
    def delta(orientation, delta):
        delta %= 360
        if orientation is Orientation.none:
            return Orientation.none
        else:
            if orientation.value + delta < 0:
                return Orientation((orientation.value + 360 + delta) % 360)
            else:
                return Orientation((orientation.value + delta) % 360)


class TeamColor(Enum):
    red = "red"
    silver = "silver"
    blank = "blank"

    @staticmethod
    def opposite_color(color):
        if color is TeamColor.blank:
            return TeamColor.blank
        elif color is TeamColor.silver:
            return TeamColor.red
        else:
            return TeamColor.silver


class PieceType(Enum):
    """Class for piece types and valid orientations"""
    pharaoh = "pharaoh"
    anubis = "anubis"
    pyramid = "pyramid"
    scarab = "scarab"
    sphinx = "sphinx"

    @staticmethod
    def can_move(from_piece, to_piece):
        """
        Determine if a move is valid
        :param from_piece: Square
        :param to_piece: Square
        :return: Boolean
        """
        # Check Place Color
        if to_piece.color is not TeamColor.blank and from_piece.color is not to_piece.color:
            return False

        # Make sure it's a movable piece
        if from_piece.piece.type is PieceType.sphinx:
            return False

        # Make sure pieces are swappable
        if to_piece.piece is not None:
            # scarab can swap with pyramid and anubis
            if from_piece.piece.type is PieceType.scarab:
                if to_piece.piece.type is PieceType.pyramid or to_piece.piece.type is PieceType.anubis:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    @staticmethod
    def can_rotate(piece, target_orientation):
        """
        Returns true if a piece can rotate
        :param piece: Piece
        :param target_orientation: Orientation
        :return: Boolean
        """
        if target_orientation is Orientation.none:
            return False

        if abs(piece.orientation.value - target_orientation.value) == 180:  # 270 or 90 are the allowed values
            return False

        if piece.type is PieceType.sphinx:
            if piece.color is TeamColor.silver:
                return target_orientation is Orientation.down or target_orientation is Orientation.right
            else:
                return target_orientation is Orientation.up or target_orientation is Orientation.left

        return True

    @staticmethod
    def bounce_direction(piece, light_direction):
        if piece.type is PieceType.pyramid:
            if light_direction is Orientation.up:
                if piece.orientation is Orientation.down:
                    return Orientation.left
                elif piece.orientation is Orientation.right:
                    return Orientation.right
                else:
                    return None
            elif light_direction is Orientation.down:
                if piece.orientation is Orientation.left:
                    return Orientation.left
                elif piece.orientation is Orientation.up:
                    return Orientation.right
                else:
                    return None
            elif light_direction is Orientation.left:
                if piece.orientation is Orientation.right:
                    return Orientation.down
                elif piece.orientation is Orientation.up:
                    return Orientation.up
                else:
                    return None
            elif light_direction is Orientation.right:
                if piece.orientation is Orientation.down:
                    return Orientation.down
                elif piece.orientation is Orientation.left:
                    return Orientation.up
                else:
                    return None

        if piece.type is PieceType.scarab:
            if piece.orientation is Orientation.down or piece.orientation is Orientation.up:
                if light_direction is Orientation.up:
                    return Orientation.left
                elif light_direction is Orientation.down:
                    return Orientation.right
                elif light_direction is Orientation.left:
                    return Orientation.up
                elif light_direction is Orientation.right:
                    return Orientation.down

            elif piece.orientation is Orientation.left or piece.orientation is Orientation.right:
                if light_direction is Orientation.up:
                    return Orientation.right
                elif light_direction is Orientation.down:
                    return Orientation.left
                elif light_direction is Orientation.left:
                    return Orientation.down
                elif light_direction is Orientation.right:
                    return Orientation.up

        return None

    @staticmethod
    def valid_rotations(piece):
        current_orientation = piece.orientation
        if piece.type is PieceType.pharaoh:
            return []
        elif piece.type is PieceType.sphinx:
            if current_orientation is Orientation.down:
                return [Orientation.right]
            elif current_orientation is Orientation.right:
                return [Orientation.down]
            elif current_orientation is Orientation.up:
                return [Orientation.left]
            else:
                return [Orientation.up]
        else:
            return [Orientation.delta(current_orientation, -90), Orientation.delta(current_orientation, 90)]

    @staticmethod
    def can_swap(piece_from, piece_to):
        if piece_from.type is PieceType.sphinx:
            return False
        if piece_to is None:
            return True
        return piece_from.type is PieceType.scarab and \
               (piece_to.type is PieceType.pyramid or piece_to.type is PieceType.anubis)


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def to_dictionary(self):
        return {"x": self.x, "y": self.y}

    @staticmethod
    def from_dictionary(value):
        return Position(value["x"], value["y"])


class Piece(object):
    """Generic Piece Class"""

    def __init__(self, piece_type, color, orientation=Orientation.none):
        self.color = color
        self.type = piece_type
        self.orientation = orientation

    def to_dictionary(self):
        return {"type": self.type.value, "color": self.color.value, "orientation": self.orientation.value}

    @staticmethod
    def from_dictionary(value):
        return Piece(PieceType(value["type"]), TeamColor(value["color"]), Orientation(value["orientation"]))

    def __str__(self):
        return "(" + str(self.color.value) + "," + str(self.type.value) + "," + str(self.orientation.value) + ")"


class Square(object):
    def __init__(self, square_type, position):
        self.color = square_type
        self.piece = None
        self.position = position

    def get_moves(self, board):
        if self.piece is None:
            return []
        # Get Squares
        squares = [board.get(self.position.x + 1, self.position.y),
                   board.get(self.position.x - 1, self.position.y),
                   board.get(self.position.x, self.position.y + 1),
                   board.get(self.position.x, self.position.y - 1),
                   board.get(self.position.x + 1, self.position.y - 1),
                   board.get(self.position.x + 1, self.position.y + 1),
                   board.get(self.position.x - 1, self.position.y + 1),
                   board.get(self.position.x - 1, self.position.y - 1)]
        squares = [x for x in squares if x is not None and (x.color is TeamColor.blank or x.color is self.color)]

        moves = []
        # Get Valid Moves
        for square in squares:
            if PieceType.can_swap(self.piece, square.piece):
                if square.piece is None:
                    moves.append(Move(MoveType.move, self.position, square.position))
                else:
                    moves.append(Move(MoveType.swap, self.position, square.position))

        # Get Valid Rotations
        rotations = PieceType.valid_rotations(self.piece)
        for rotation in rotations:
            moves.append(Move(MoveType.rotate, self.position, rotation))

        return moves

    def to_dictionary(self):
        value = {"position": self.position.to_dictionary(), "color": self.color.value}
        if self.piece is not None:
            value["piece"] = self.piece.to_dictionary()
        return value
