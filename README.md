# Tetris

I have implemented the classic game of tetris. The player is able to use keys to move shapes around (as well as rotate them) and then drop them onto the grid. Whenever a row is completely filled with blocks, it will be removed and the game score will be updated. The game ends when a shape hits the top of the game grid. When this happens, the game will close and the player will be able to see their final score in the console. There will also be a prompt to run scores.py so that the player can see their top scores.

## Running Instructions

The game can be played by going into the directory with the play.py and tetris.py files, and then running either of the following commands in the terminal: `$ python3 play.py` or `$ python3 play.py w h`, where w and h are the user specified width and height of the grid. Then to see the top scores, the user can run `$ python3 scores.py` and then go to their browser and open `localhost:5000/`.

## Packages

For this project, I learned PyGame to render the game for the user to play. Additionally, I have used the Argparse module to allow the user to enter their own dimensions for the grid if they wish to do so. Finally, I have used Flask to create a simple server that the user can run to see their top scores.

## Description of Code Structure

I have used two classes to create the game, as in the tetris.py file. One of the classes is specific to the current shape in play, and the other class corresponds to the game itself. This keeps track of the game state as well as the different methods required to run the game. The game itself runs in play.py, where the Pygame module has been used to render the game on a screen for the user to interact with. Everything related to rendering the top scores on the server is in the scores.py file.
