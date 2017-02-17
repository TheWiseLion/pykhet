# Solver Chooses From Available Moves
import random
import khetsearch
from pykhet.solvers import optimal_board as ob
from pykhet.components.board import KhetBoard
from pykhet.components.types import Position, Piece, PieceType, TeamColor, Orientation, Move, MoveType

piece_to_score = {PieceType.anubis: 2, PieceType.pyramid: 1, PieceType.scarab: 0, PieceType.sphinx: 0}


def color_score(board, color):
    squares = board.squares_with_pieces_of_color(color)
    is_pharaoh = False
    score = 0
    for square in squares:
        if square.piece.type is PieceType.pharaoh:
            is_pharaoh = True
        else:
            score += piece_to_score[square.piece.type]

    if not is_pharaoh:
        return -1000
    else:
        return score


class Node(object):
    def __init__(self, bias_color, board, color, move=None, parent=None):
        self.move = move  # last made move to get to the given board
        self.bias_color = bias_color
        self.color = color
        self.representation = board.to_serialized_squares()
        self.red_score = color_score(board, TeamColor.red)
        self.silver_score = color_score(board, TeamColor.silver)
        self.children = None
        self.moves = board.get_available_moves(self.color)
        self.score = self.red_score - self.silver_score
        self.parent = parent

    def expand(self):
        board = KhetBoard.from_serialized_squares(self.representation)

        opposite_color = TeamColor.opposite_color(self.color)
        self.children = []
        for move in self.moves:
            new_board = board.board_from_move(move, self.color)
            self.children.append(Node(self.bias_color, new_board, opposite_color, move, parent=self))
        return len(self.moves)

    def update_score(self, color):
        """
        Sets new score value for self based on children then updates parent

        SCORE:
            score = red_score - silver_score if no children
            else
            score = min(children.score)
        :return:
        """
        if self.children is not None:
            bias = 0  # Add small bias for directions that have better probabilistic outcomes
            if self.parent is not None:
                parent_base = self.parent.red_score - self.parent.silver_score
                scores = [x.score for x in self.children]
                if self.bias_color is TeamColor.red and all(i >= parent_base for i in scores):
                    bias = (.5 * len([1 for i in scores if i > parent_base])) / len(scores)
                elif self.bias_color is TeamColor.silver and all(i <= parent_base for i in scores):
                    bias = (.5 * len([1 for i in scores if i < parent_base])) / len(scores)

            if self.color is color:
                if color is TeamColor.red:
                    self.score = max(self.children, key=lambda x: x.score).score + bias
                else:
                    self.score = min(self.children, key=lambda x: x.score).score - bias
            else:
                if color is TeamColor.red:
                    self.score = min(self.children, key=lambda x: x.score).score + bias
                else:
                    self.score = max(self.children, key=lambda x: x.score).score - bias

        if self.parent is not None:
            self.parent.update_score(color)

    def get_minimum_leaf(self, color):
        """
        The color that we want to maximize the minimum of
        :param color:
        :return:
        """
        # Base Case
        if self.children is None:
            return self
        # TODO what if childern is empty?

        # IF COLOR == Red, "high" is most positive
        # IF COLOR == Silver, "high" is most negative
        if color is self.color:
            # choose the node with the highest score (this is a move that we get to pick)
            max_value = None
            if color is TeamColor.red:
                max_value = max(self.children, key=lambda x: x.score)
            else:
                max_value = min(self.children, key=lambda x: x.score)
            return max_value.get_minimum_leaf(color)
        else:
            # choose the node with the LOWEST score (this is a move that don't get to pick)
            min_value = None
            if color is TeamColor.red:
                min_value = min(self.children, key=lambda x: x.score)
            else:
                min_value = max(self.children, key=lambda x: x.score)
            return min_value.get_minimum_leaf(color)


class MinmaxSolver(object):
    """
    Iterative Search Based On Alpha-Beta Pruning & Known Path Favoritism
    """

    def __init__(self, max_evaluations=1000, min_depth=2):
        """

        :param max_evaluations:
        :param min_depth: TODO: minimum depth to accept a move path
        """
        self.max_evaluations = max_evaluations
        self.min_depth = min_depth

    def get_move(self, board, color):
        """
        Return the next move (and some stats) for the given color
        :param board:
        :param color:
        :return:
        """
        evaluations = 0
        root = Node(color, board, color)

        evaluations += root.expand()

        # Iteratively expand the tree's levels till limit is reached
        # Expand the least promising leaf of the most promising path
        while evaluations < self.max_evaluations:
            # log(N) for getting leaf
            # ~C to expand
            # log(N) to update scores
            leaf = root.get_minimum_leaf(color)
            if leaf.score is -1000:
                # We lost the game (min leaf == lose then we lost)
                break
            evaluations += leaf.expand()
            leaf.update_score(color)

        if color is TeamColor.red:
            return max(root.children, key=lambda x: x.score).move
        else:
            return min(root.children, key=lambda x: x.score).move





# game = ClassicGame()
# board = board_to_node(game)
# print(len(board_to_node(game)))
# results = khetsearch.khetsearch(_red, board, 3, 100000)
# print results[75*2:]

class CMinMaxSolver(object):
    """
    Iterative Search Based On Alpha-Beta Pruning & Known Path Favoritism

    """

    def __init__(self, max_evaluations=100000, min_depth=2, bias=0.01):
        """

        :param max_evaluations:
        :param min_depth: TODO: minimum depth to accept a move path
        """
        self.max_evaluations = max_evaluations
        self.min_depth = min_depth
        self.bias = bias

    def get_move(self, board, color):
        """
        Return the next move (and some stats) for the given color
        :param board:
        :param color:
        :return:
        """
        numeric_board = ob.board_to_node(board)
        numeric_color = ob.color_to_byte_color(color)

        results = khetsearch.khetsearch(numeric_color, numeric_board, self.min_depth, self.max_evaluations)
        move_ratings = []
        # print(str(len(results))+" results")
        for x in range(0, int(len(results) / 2)):

            value = results[x * 2]
            score = results[x * 2 + 1]

            base = (value >> 16) & 0x7FFF
            other_value = value & 0xFFFF
            xp = base >> 8
            yp = base & 0xFF
            rotate = (value >> 31) & 0x1
            pos = Position(xp, yp)
            move = None
            if rotate == 1:
                # print(str(pos)+" rotates "+ob.move_value_to_orientation(other_value).name+" -- "+str(other_value))
                move = Move(MoveType.rotate, pos, ob.move_value_to_orientation(other_value))
            else:
                pos2 = Position(other_value >> 8, other_value & 0xFF)
                # print(str(pos)+" to "+str(pos2))

                if board.get(pos2.x, pos2.y).piece is None:
                    move = Move(MoveType.move, pos, pos2)
                else:
                    move = Move(MoveType.swap, pos, pos2)


            move_ratings.append({
                "move": move,
                "score": score
            })

        reasonable_moves = []
        # Lowest first if silver, highest first if red
        move_ratings = sorted(move_ratings, key=lambda lx: lx["score"], reverse=(color is TeamColor.red))

        min_score = move_ratings[0]["score"]
        # print("Min Score: "+str(min_score))
        for move in move_ratings:
            # We want values higher than min score if red
            if color is TeamColor.red and min_score <= move["score"]:
                reasonable_moves.append(move)

            # We want values lower than min score if silver
            elif color is TeamColor.silver and min_score >= move["score"]:
                reasonable_moves.append(move)

        # Randomly Choose A Move Amongst Equivalent' Moves
        r_move = random.choice(reasonable_moves)

        return r_move["move"]

