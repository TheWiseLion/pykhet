pykhet: a library for the board game khet
=========================================

.. image:: https://travis-ci.org/TheWiseLion/pykhet.svg?branch=master
    :target: https://travis-ci.org/TheWiseLion/pykhet.svg?branch=master


Introduction
------------

The Khet board game logic and structures implemented in python. Also exposes adversarial search based algorithms.

.. code-block:: python

    from pykhet.components.types import TeamColor
    from pykhet.games.game_types import ClassicGame
    import random
    from pykhet.solvers.minmax import MinmaxSolver

    # Create a game with classic piece placement
    game = ClassicGame()

    # Get all valid silver moves
    silver_moves = game.get_available_moves(TeamColor.silver)

    # Randomly Play One
    game.apply_move(random.choice(silver_moves))

    # Finish the turn by applying the laser
    game.apply_laser(TeamColor.silver)

    # Use adversarial search to pick a move
    solver = MinmaxSolver()
    move = solver.get_move(game, TeamColor.red)
    game.apply_move(move)
    game.apply_laser(TeamColor.red)


Serialization
-------------
There is ample support to serializing the state of objects as dictionaries. Useful for easy storage as json.

.. code-block:: python

    from pykhet.components.types import TeamColor, Piece
    from pykhet.games.game_types import ClassicGame
    import random
    from pykhet.solvers.minmax import MinmaxSolver

    # Create a game with classic piece placement
    game = ClassicGame()

    # Serialize the board (list of serialized piece positions, orientations, and colors)
    squares = game.to_serialized_squares()

    # Deserialize the board
    Game.from_serialized_squares(squares)

    # Serialize a pieces
    p1 = Piece(PieceType.scarab, TeamColor.silver, Orientation.down).to_dictionary()
    # Deserialize a piece
    same_piece = Piece.from_dictionary(p1)


Board Layout
------------

The khet board and piece layout is represented below:

.. image:: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/board-khet.png
    :target: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/board-khet.png

