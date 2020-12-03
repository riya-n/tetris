"""
Run this file to play the game.
$ python3 play.py
or
$ python3 play.py w h
where w and h are the player specified width and height of the grid
"""
from sys import exit
import pygame
import argparse

from tetris import Game


def draw_grid(game, screen):
  """
  Draws the grid into the screen.

  Args:
    game (Game): the current game in play.
    screen (pygame.Surface): the screen the game
      is being played on.

  Returns:
    None
  """
  block_size = 30
  for (x, y) in game:
    pygame.draw.rect(screen, game.grid[y][x], pygame.Rect(
        x * (block_size + 1) + 1, y * (block_size + 1) + 1,
        block_size, block_size
      ))
  pygame.display.flip()

def draw_shape(game, screen):
  """
  Draws the current shape in play.

  Args:
    game (Game): the current game in play.
    screen (pygame.Surface): the screen the game
      is being played on.

  Returns:
    None
  """
  if game.shape is not None:
    for x in range(4):
      for y in range(4):
        if (x, y) in game.shape:
          x_coord = x + game.shape.x
          y_coord = y + game.shape.y
          block_size = 30
          pygame.draw.rect(screen, game.shape.color, pygame.Rect(
              x_coord * (block_size + 1) + 1, y_coord * (block_size + 1) + 1,
              block_size, block_size
            ))
    pygame.display.flip()

def get_dimensions():
  """
  Parses in the player's specified dimensions, otherwise
  defaults to a 10x24 grid.

  Args:
    None

  Returns:
    (int, int): the width and height of the grid
  """
  parser = argparse.ArgumentParser(description="""Enter the size of the board 
    you wish to play on in the following format: width height""")
  parser.add_argument("w", help="the width of the grid", nargs='?',
    type=int, const=10)
  parser.add_argument("h", help="the height of the grid", nargs='?',
    type=int, const=24)
  args = parser.parse_args()

  w, h = 10, 24
  if args.w:
    w = args.w
  if args.h:
    h = args.h

  return w, h
  
def main():
  """
  The game runs here. The user has the option to enter the grid size, otherwise
  will play on a standard 10x24 grid.
  """
  pygame.init()

  w, h = get_dimensions()
  size = (w * 30) + (w + 1), (h * 30) + (h + 1)
  background_color = (50, 50, 50)

  count = 0
  right = False
  left = False
  down = False

  screen = pygame.display.set_mode(size)
  pygame.display.set_caption("Tetris")

  game = Game(w, h)

  while 1:
    if count == 100 or (count % 10 == 0 and down):
      game.drop_shape()
      count = 0
    elif count % 30 == 0:
      if right:
        game.move_right()
      elif left:
        game.move_left()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          game.rotate_shape()
        elif event.key == pygame.K_RIGHT:
          right = True
        elif event.key == pygame.K_DOWN:
          down = True
        elif event.key == pygame.K_LEFT:
          left = True
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
          down = False
        elif event.key == pygame.K_RIGHT:
          right = False
        elif event.key == pygame.K_LEFT:
          left = False

    if game.end_game():
      print("GAME OVER. Your Score: {}".format(game.score))
      print("Run '$ python3 scores.py' to see your top scores.")
      # save score to file
      with open("scores.txt", "a") as f:
        f.write(str(game.score) + "\n")
      exit()
    
    count += 1
    draw_shape(game, screen)
    screen.fill(background_color)
    draw_grid(game, screen)

main()
