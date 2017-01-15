from pykhet.components.types import TeamColor, Position, Square, PieceType, LaserPathType, Orientation, MoveType, Piece, \
    LaserPathNode


class KhetBoard(object):
    """
    Board is always 8x10 with specific square types
    x = columns
    y = rows
    """

    def __init__(self, squares=None):
        self.winner = None
        self.sphinxes = {}
        self.color_pieces = {TeamColor.red: [], TeamColor.silver: []}
        self.squares = [x[:] for x in [[None] * 8] * 10]
        for x in range(0, 10, 1):
            for y in range(0, 8, 1):
                position = Position(x, y)
                if x is 0 or (x is 8 and y is 0) or (x is 8 and y is 7):
                    self.squares[x][y] = Square(TeamColor.silver, position)
                elif x is 9 or (x is 1 and y is 0) or (x is 1 and y is 7):
                    self.squares[x][y] = Square(TeamColor.red, position)
                else:
                    self.squares[x][y] = Square(TeamColor.blank, position)

        if squares is not None:
            for square in squares:
                piece_clone = Piece(square.piece.type, square.piece.color, square.piece.orientation)
                self.set_piece(square.position, piece_clone)

    @staticmethod
    def _on_board(pos):
        return 10 > pos.x >= 0 and 8 > pos.y >= 0

    def _validate_position(self, pos):
        if not KhetBoard._on_board(pos):
            raise RuntimeError("Position must be on board " + str(pos))

    def set_piece(self, position, piece):
        self._validate_position(position)
        if self.squares[position.x][position.y].piece is not None:
            raise RuntimeError("Piece already exists at location " + str(position))
        self.squares[position.x][position.y].piece = piece

        if piece.type is PieceType.sphinx:
            self.sphinxes[piece.color] = position

        self.color_pieces[piece.color].append(self.squares[position.x][position.y])

    def rotate_piece(self, position, orientation):
        self._validate_position(position)
        if self.squares[position.x][position.y].piece is None:
            raise RuntimeError("Piece doesnt exist at location")
        elif PieceType.can_rotate(self.squares[position.x][position.y].piece, orientation):
            self.squares[position.x][position.y].piece.orientation = orientation
        else:
            raise RuntimeError("Illegal Move Can't Rotate")

    def move_piece(self, from_square, to_square):
        # Validate Move Can Be Made
        if not KhetBoard._on_board(from_square) or not KhetBoard._on_board(to_square):
            raise RuntimeError("Invalid move from or to is not on board")

        if self.squares[from_square.x][from_square.y] is None:
            raise RuntimeError("Square has no movable piece")

        if self.squares[to_square.x][to_square.y].piece is not None:
            raise RuntimeError("Cannot move to occupied square: " + str(to_square))

        if not PieceType.can_move(self.squares[from_square.x][from_square.y], self.squares[to_square.x][to_square.y]):
            raise RuntimeError("Piece cannot move to that location")

        # Make move
        piece = self.squares[from_square.x][from_square.y].piece
        self.remove_piece(from_square)
        self.set_piece(to_square, piece)

    def get_laser_path(self, color):
        """Return path of the laser. (Square, LaserType, Orientation)"""
        sphinx_position = self.sphinxes[color]
        sphinx = self.squares[sphinx_position.x][sphinx_position.y].piece

        path = []
        last_position = Position(sphinx_position.x, sphinx_position.y)
        last_event = LaserPathType.through
        last_direction = sphinx.orientation
        while last_direction is not None and last_event is not LaserPathType.hit:
            next_position = Orientation.next_position(last_position, last_direction)
            if KhetBoard._on_board(next_position):
                square = self.squares[next_position.x][next_position.y]
                path_type = LaserPathType.through
                tmp_dir = last_direction
                if square.piece is not None:
                    # hit or bounce...
                    last_direction = PieceType.bounce_direction(piece=square.piece, light_direction=last_direction)
                    if last_direction is None:
                        path_type = LaserPathType.hit
                    else:
                        path_type = LaserPathType.bounce

                path.append(LaserPathNode(path_type, next_position, tmp_dir))
                last_position = next_position
                last_event = path_type
            else:
                break
        return path

    def remove_piece(self, position):
        self._validate_position(position)
        piece = self.squares[position.x][position.y].piece
        self.color_pieces[piece.color].remove(self.squares[position.x][position.y])
        self.squares[position.x][position.y].piece = None
        return piece

    def squares_with_pieces_of_color(self, color):
        return self.color_pieces[color]

    def get(self, x, y):
        if not KhetBoard._on_board(Position(x, y)):
            return None
        return self.squares[x][y]

    def swap_pieces(self, pos1, pos2):
        self._validate_position(pos1)
        self._validate_position(pos2)
        piece1 = self.squares[pos1.x][pos1.y].piece
        piece2 = self.squares[pos2.x][pos2.y].piece
        if piece2 is None or piece1 is None:
            raise RuntimeError("Pieces must exist in both locations {p1:" + str(pos1) + ", p2:" + str(pos2) + "}")
        self.remove_piece(pos1)
        self.remove_piece(pos2)
        self.set_piece(pos1, piece2)
        self.set_piece(pos2, piece1)

    def get_available_moves(self, team_color):
        """Describes all moves for a color by position. Should be json serializable."""
        squares = self.squares_with_pieces_of_color(team_color)
        moves = []
        for square in squares:
            moves.extend(square.get_moves(self))
        return moves

    def apply_move(self, move):
        """Applies a move generated by @get_available_moves"""
        if move.type is MoveType.rotate:
            self.rotate_piece(move.position, move.value)
        elif move.type is MoveType.swap:
            self.swap_pieces(move.position, move.value)
        else:
            self.move_piece(move.position, move.value)

    def _apply_laser(self, color):
        """
        Applies Board Changes Based On Firing Laser Of Given Color
        :param color:
        :return:
        """
        path = self.get_laser_path(color)
        if path[-1].type is LaserPathType.hit:
            square = self.get(path[-1].position.x, path[-1].position.y)
            if (square.piece.type is PieceType.anubis and square.piece.orientation is path[-1].direction) \
                    or square.piece.type is PieceType.sphinx:
                # Hit but not destroyed
                pass
            else:
                piece = self.remove_piece(path[-1].position)
                return path, piece
        return path, None

    def apply_laser(self, color):
        """
        Returns path the laser took and piece destroyed (if any) and new winner (if one)
        :param color:
        :return:
        """
        if self.winner is not None:
            raise RuntimeError("Game is already complete " + str(self.winner.value) + " won")
        results = {}
        path, piece = self._apply_laser(color)

        if piece is not None:
            results["destroyed"] = piece
            if piece.type is PieceType.pharaoh:
                self.winner = TeamColor.opposite_color(piece.color)
                results["winner"] = self.winner

        results["path"] = path
        return results

    def board_from_move(self, move, color):
        """
        Returns new board without modifying current board after applying move + laser
        :return: KhetBoard
        """
        new_board = KhetBoard(self.color_pieces[TeamColor.silver] + self.color_pieces[TeamColor.red])
        new_board.apply_move(move)
        new_board.apply_laser(color)
        return new_board

    def to_serialized_squares(self):
        """
        Returns list of non-empty square representations
        :return:
        """
        squares = []
        for lst in self.squares:
            for square in lst:
                if square.piece is not None:
                    squares.append(square.to_dictionary())
        return squares

    def to_serialized_squares_full(self):
        """
        Returns list of all square representations
        :return:
        """
        squares = []
        for lst in self.squares:
            for square in lst:
                squares.append(square.to_dictionary())
        return squares

    @staticmethod
    def from_serialized_squares(lst):
        board = KhetBoard()
        for square in lst:
            if "piece" in square:
                pos = Position.from_dictionary(square["position"])
                piece = Piece.from_dictionary(square["piece"])
                board.set_piece(pos, piece)

        return board
