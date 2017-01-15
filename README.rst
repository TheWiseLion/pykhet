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
    # Create a game with classic piece placement
    game = ClassicGame()

    # Get all valid silver moves
    silver_moves = game.get_available_moves(TeamColor.silver)

    # Randomly Play One
    game.apply_move(random.choice(silver_moves))

    # Finish the turn by applying the laser
    game.apply_laser(TeamColor.silver)

Board Layout
------------

The khet board and piece layout is represented below:

.. image:: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/board-khet.png
    :target: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/board-khet.png

Adversarial Search
------------------

Provided is a very basic adversarial search algorithm that works with a low number of iterations.
Iteration 1:
.. image:: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/Iter1.png
    :target: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/Iter1.png
Iteration 2:
.. image:: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/Iter2.png
    :target: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/Iter2.png
Iteration 3:
.. image:: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/Iter3.png
    :target: https://raw.githubusercontent.com/TheWiseLion/pykhet/master/docs/Iter3.png
