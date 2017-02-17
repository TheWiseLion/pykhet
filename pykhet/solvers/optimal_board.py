"""
Translation from C binding to native python state for board/game state.
#TODO: edge case - scarab on silver location, swap on to non-silver
"""
# Piece Types
from pykhet.components.types import PieceType, Orientation, TeamColor
from pykhet.games.game_types import ClassicGame

# Colors
_silver = 1
_red = 0
_color_mask = 1

_pharaoh = 2
_anubis = 4
_scarab = 6
_pyramid = 8
_sphinx = 10
_type_mask = 14

# Orientations
_up = 0
_right = 16
_down = 32
_left = 48
_orientation_mask = 48

# Empty
_vacant = 0
_occupied = -128
_vacant_mask = -128


#### Representation ####
#    10 x 8 Board
#    occupied/vacant (1) | color (1) | type (3) | orientation (2)
#

def piece_to_byte_piece(piece):
    if piece is PieceType.pharaoh:
        return _pharaoh
    if piece is PieceType.anubis:
        return _anubis
    if piece is PieceType.pyramid:
        return _pyramid
    if piece is PieceType.sphinx:
        return _sphinx
    if piece is PieceType.scarab:
        return _scarab


def orientation_to_byte_orientation(orientation):
    if orientation is Orientation.down:
        return _down
    if orientation is Orientation.up:
        return _up
    if orientation is Orientation.left:
        return _left
    if orientation is Orientation.right:
        return _right


def color_to_byte_color(color):
    if color is TeamColor.red:
        return _red
    else:
        return _silver


def move_value_to_orientation(value):
    if value == _up:
        return Orientation.up
    elif value == _down:
        return Orientation.down
    elif value == _left:
        return Orientation.left
    else:
        return Orientation.right


def board_to_node(board):
    board_state = []
    for y in range(0, 8, 1):
        for x in range(0, 10, 1):
            square = board.squares[x][y]
            if square.piece is not None:
                ptype = piece_to_byte_piece(square.piece.type)
                porientation = orientation_to_byte_orientation(square.piece.orientation)
                pcolor = color_to_byte_color(square.piece.color)
                board_state.append(_occupied + ptype + porientation + pcolor)
            else:
                board_state.append(_vacant)
    return board_state

# All in all a speed up factor of 2.6x
