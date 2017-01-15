# Solver Chooses From Available Moves
from pykhet.components import PieceType, TeamColor, KhetBoard

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
        evaluations = 0L
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


