"""
A simple tetris game.
"""
import random

class Shape:
  """
  Imagine a 4x4 grid with these coordinates as the filled ones (centered).
  """
  shapes = [
    [(1, 0), (1, 1), (1, 2), (1, 3)],
    [(1, 0), (2, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(1, 0), (2, 0), (1, 1), (2, 1)],
    [(1, 1), (2, 1), (0, 2), (1, 2)],
    [(1, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 1), (1, 2), (2, 2)],
  ]

  """
  These are the different possible rotations for each shape above.
  """
  rotations = [2, 4, 4, 1, 2, 4, 2]

  """
  Colors corresponding to the shapes above.
  """
  colors = [
    (64, 224, 208),
    (100, 149, 237),
    (255, 191, 0),
    (223, 255, 0),
    (159, 226, 191),
    (204, 204, 255),
    (222, 49, 99)
  ]

  def __init__(self, x, y):
    """
    Construct an instance of the Shape class.

    Attributes:
      - self.x (int): the x coordinate of the shape in the grid
      - self.y (int): the y coordinate of the shape in the grid
      - self.shape (array): the specific shape of the piece
      - self.color (tuple): the color of the shape (rgb)
      - self.rotation (int): the number of rotations on the shape

    Args:
      x (int): the x coordinate of the shape
      y (int): the y coordinate of the shape
    """
    self.x = x
    self.y = y
    i = random.randint(0, len(self.shapes) - 1)
    self.shape = self.shapes[i]
    self.color = self.colors[i]
    self.rotation = 0

  def rotate(self):
    """
    Rotates the shape clockwise. Updates the rotation and shape attributes.

    Args:
      None
    
    Returns:
      None
    """
    index = self.colors.index(self.color)
    self.rotation = (self.rotation + 1) % self.rotations[index]

    if self.rotation == 0:
      self.shape = self.shapes[index]
    else:
      shape = []
      for (x, y) in self.shape:
        # using (1, 1) as rotation point
        shape.append((y, 2 - x))
      self.shape = shape

  def __contains__(self, item):
    return item in self.shape


class Game:
  def __init__(self, w, h):
    """
    Construct an instance of the game.

    Attributes:
      - self.w (int): the width of the grid
      - self.h (int): the height of the grid
      - self.grid (array): the grid itself (of colors)
      - self.score (int): the current score of the game
    
    Args:
      w (int): the width of the grid
      h (int): the height of the grid
    """
    self.w = w
    self.h = h

    self.grid = []
    for _ in range(h):
      row = []
      for _ in range(w):
        row.append((0, 0, 0))
      self.grid.append(row)
    
    self.score = 0
    self.shape = None

  def next_shape(self):
    """
    Creates the next shape (centered at the top).

    Args:
      None

    Returns:
      None
    """
    self.shape = Shape(3, 0)

  def drop_shape(self):
    """
    Moves the shape down the grid.

    Args:
      None

    Returns:
      None
    """
    self.shape.y += 1
    if self.check_collision():
      self.update_grid()

  def rotate_shape(self):
    """
    Rotates the shape if space allows.

    Args:
      None

    Returns:
      None
    """
    rotation = self.shape.rotation
    shape = self.shape.shape
    self.shape.rotate()
    if self.check_collision():
      self.shape.rotation = rotation
      self.shape.shape = shape

  def move_left(self):
    """
    Moves the shape to the left if space allows.

    Args:
      None

    Returns:
      None
    """
    x = self.shape.x
    self.shape.x -= 1
    if self.check_collision():
      self.shape.x = x
  
  def move_right(self):
    """
    Moves the shape to the right if space allows.

    Args:
      None

    Returns:
      None
    """
    x = self.shape.x
    self.shape.x += 1
    if self.check_collision():
      self.shape.x = x

  def check_collision(self):
    """
    Checks when the shape has collided with the shapes already on the
    grid or with the edge of the grid.

    Args:
      None

    Returns:
      bool: whether there has been a collision. 
    """
    for x in range(4):
      for y in range(4):
        if (x, y) in self.shape:
          x_coord = x + self.shape.x
          y_coord = y + self.shape.y
          if (y_coord >= self.h - 1 or
              x_coord >= self.w or x_coord < 0 or
              self.grid[y_coord + 1][x_coord] != (0, 0, 0)):
            return True

    return False

  def remove_rows(self):
    """
    Removes a row when the entire row is filled with blocks
    and moves everything above it down. Multiple rows may be
    removed in one go if they are all filled.

    Args:
      None

    Returns:
      None
    """
    rows = []
    for row in range(self.h):
      if (0, 0, 0) not in self.grid[row]:
        rows.append(row)

    for row in rows:
      # remove row
      for col in range(self.w):
        self.grid[row][col] = (0, 0, 0)
      
      # move all above down
      for x in range(self.w):
        for y in range(row, 0, -1):
          if y == 0:
            self.grid[y][x] = (0, 0, 0)
          else:
            self.grid[y][x] = self.grid[y - 1][x]

      self.score += 1

  def update_grid(self):
    """
    Updates the grid when a new shape is added.

    Args:
      None

    Returns:
      None
    """
    for x in range(4):
      for y in range(4):
        if (x, y) in self.shape:
          x_coord = x + self.shape.x
          y_coord = y + self.shape.y
          if self.grid[y_coord][x_coord] == (0, 0, 0):
            self.grid[y_coord][x_coord] = self.shape.color
    self.remove_rows()
    self.next_shape()

  def end_game(self):
    """
    Checks if the game is over (i.e., we have reached the
    top of the screen).

    Args:
      None
    
    Returns:
      bool: whether the game is over or not.
    """
    return self.shape.y == 0 and self.check_collision()

  def __iter__(self):
    for x in range(self.w):
      for y in range(self.h):
        yield (x, y)
