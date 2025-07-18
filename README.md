Tiles Game - README
===================

Description:
------------
This is a simple color-matching puzzle game built with Pygame. The goal is to make all tiles on the board match the same color using the fewest moves possible.

Requirements:
-------------
- Python 3.x
- Pygame library (`pip install pygame`)
- Image files: `restartGame.png` and `newGame.png` (place in the same directory as tiles.py)

How to Run:
-----------
1. Ensure all requirements are installed and image files are present.
2. Run the game:
   > python tiles.py

Controls:
---------
- Click on any tile to change its color.
  - Left mouse button: Increment color.
  - Right mouse button: Decrement color.
- "NewGame" button (top right): Start a new random game.
- "Replay" button: Reset the current board to its initial state.

Scoring:
--------
- "YOUR SCORE" counts the number of moves made.
- "BEST SCORE" is the minimum moves required to solve the current board.

Winning & Losing:
-----------------
- Win: All tiles match the same color and your score is less than or equal to the best score.
- Lose: If your moves exceed the best score.

Enjoy the game!
