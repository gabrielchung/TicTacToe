#
# Good ideas:
#   1. More than two players?
#   2. 3D TTT?
#
# API:
#   1. init ( board_size )              -> None
#   2. whose_turn ()                    -> player_index
#   3. get_board ()                     -> [[ Integer ]]
#   4. possible_moves ()                -> [tuple]
#   5. take ( x, y )                    -> Boolean win?

class TTT:
  EMPTY_SPACE = -1

  def __init_board(self, board_size):
    result = []
    row = [ self.EMPTY_SPACE ] * board_size
    for i in range(board_size):
      result.append(row.copy())
    return result

  def __init__(self, board_size=3):
    self.board_size = board_size
    self.curr_turn_player = 0
    self.board = self.__init_board(board_size)

  def whose_turn(self):
    return self.curr_turn_player

  def get_board(self):
    return self.board

  def possible_moves(self):
    result = []
    # return all empty spots
    for x in range(self.board_size):
      for y in range(self.board_size):
        if self.board[x][y] == self.EMPTY_SPACE:
          result.append((x, y))
    return result

  def __next_player(self):
    self.curr_turn_player = 1 if self.curr_turn_player == 0 else 0

  def __mark_board(self, x, y):
    self.board[x][y] = self.whose_turn()

  def take(self, x, y):
    if (x, y) in self.possible_moves():
      self.__mark_board(x, y)
      won = self.__win(self.whose_turn())
      self.__next_player()
      return won
    else:
      raise Exception('Move is not valid')

  def __win(self, player_index):
    return self.__win_vertical(player_index) or self.__win_horizontal(player_index) or self.__win_diagonal(player_index)

  def __win_vertical(self, player_index):
    for x in range(self.board_size):
      win = True
      for _x in range(self.board_size):
        for y in range(self.board_size):
          if self.board[x][y] != player_index:
            win = False
      if win:
        return True
    return False

  def __win_horizontal(self, player_index):
    for y in range(self.board_size):
      win = True
      for _y in range(self.board_size):
        for x in range(self.board_size):
          if self.board[x][y] != player_index:
            win = False
      if win:
        return True
    return False

  def __win_diagonal(self, player_index):
    return self.__win_diagonal_top_left_to_bottom_right(player_index) or self.__win_diagonal_bottom_left_to_top_right(player_index)

  def __win_diagonal_top_left_to_bottom_right(self, player_index):
    x, y = 0, 0
    # Move to the bottom right
    while x < self.board_size and y < self.board_size:
      if self.board[x][y] != player_index:
        return False
      x += 1
      y += 1
    return True

  def __win_diagonal_bottom_left_to_top_right(self, player_index):
    x, y = 0, (self.board_size - 1)
    # Move to the top right
    while x < self.board_size and y < self.board_size:
      if self.board[x][y] != player_index:
        return False
      x += 1
      y -= 1
    return True