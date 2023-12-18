"""Illustration of tournament.

Authors:
    Alejandro Bellogin <alejandro.bellogin@uam.es>

"""

from __future__ import annotations
from audioop import reverse
from sre_parse import State  # For Python 3.7

import numpy as np

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import simple_evaluation_function
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board,
)
from tournament import StudentHeuristic, Tournament

from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)

import reversi


class Heuristic1(StudentHeuristic):

    def get_name(self) -> str:
        return "dummy"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return self.dummy(123)

    def dummy(self, n: int) -> int:
        return n + 4


def player_score(board: dict, player_label) -> float:
    score = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if board[x][y] == player_label:
                score = score + 1
    return score
class Heuristic2(StudentHeuristic):

    def get_name(self) -> str:
        return "catxo"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        #valor heuristica
        h = 0

        #esquinas
        ccell = ((0, 0), (0, 7), (7, 0), (7, 7))

        #adyacente a esquinas
        addadcells = ((0, 2), (1, 2), (2, 2), (2, 1), (5, 0), (5, 1), (5, 2), (6, 2), (6, 1),
                    (0, 5), (1, 5), (2, 5), (2, 6), (2, 7), (5, 5), (5, 6), (5, 7), (6, 5), (7, 5))

        #diagonal a esquinas
        dcells = ((1, 1), (1, 6), (6, 1), (6, 6))

        #adyacente a esquinas
        acells = ((0, 1), (1, 0), (0, 6), (1, 7), (6, 0), (7, 1), (6, 7), (7, 6))

        board = reversi.from_dictionary_to_array_board(state.board, 8, 8)

        if (state.is_player_max(state.next_player)):
            player1 = state.next_player.label
            player2 = state.previous_player.label
        else:
            player1 = state.previous_player.label
            player2 = state.next_player.label

        # compara las puntuaciones de los jugadores para determinar movimiento mas conveniente

        h = (player_score(board, player2) - player_score(board, player1)) /  (player_score(board, player2) + player_score(board, player1))

        #movimiento más favorable
        for cell in ccell:
          if (board[cell[0]][cell[1]] == player1):
              h = h + 30
          elif (board[cell[0]][cell[1]] == player2):
              h = h - 30

        # movimiento que favorece movimientos desfavorables para el enemigo
        for cell in addadcells:
          if (board[cell[0]][cell[1]] == player1):
              h = h + 4
          elif (board[cell[0]][cell[1]] == player2):
              h = h - 4

        # movimientos que favorecen que el adversario consiga esquinas (por tanto desfavoreables)
        for cell in acells:
          if (board[cell[0]][cell[1]] == player1):
              h = h - 6
          elif (board[cell[0]][cell[1]] == player2):
              h = h + 6

        for cell in dcells:
          if (board[cell[0]][cell[1]] == player1):
              h = h - 15
          elif (board[cell[0]][cell[1]] == player2):
              h = h + 15

        return h


class Heuristic3(StudentHeuristic):

    def get_name(self) -> str:
        return "pura"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        #valor heuristica
      h = 0

      #esquinas
      ccell = ((0, 0), (0, 7), (7, 0), (7, 7))

      #adyacente a esquinas
      addadcells = ((0, 2), (1, 2), (2, 2), (2, 1), (5, 0), (5, 1), (5, 2), (6, 2), (6, 1),
                    (0, 5), (1, 5), (2, 5), (2, 6), (2, 7), (5, 5), (5, 6), (5, 7), (6, 5), (7, 5))

      #diagonal a esquinas
      dcells = ((1, 1), (1, 6), (6, 1), (6, 6))

      #adyacente a esquinas
      acells = ((0, 1), (1, 0), (0, 6), (1, 7), (6, 0), (7, 1), (6, 7), (7, 6))

      #bordes
      bcells = ((0, 2), (0, 3), (0, 4), (0, 5), (2, 0), (3, 0), (4, 0), (5, 0),
                (7, 2), (7, 3), (7, 4), (7, 5), (2, 7), (3, 7), (4, 7), (5, 7))

      #addyacent to bcells
      addbcells = ((1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (3, 1), (4, 1),
                  (5, 1), (6, 2), (6, 3), (6, 4), (6, 5), (2, 6), (3, 6), (4, 6), (5, 6))

      #addyacent to addyacent to bcells
      addaddbcells = ((2, 2), (2, 3), (2, 4), (2, 5), (2, 2), (3, 2), (4, 2),
                      (5, 2), (5, 2), (5, 3), (5, 4), (5, 5), (2, 5), (3, 5), (4, 5), (5, 5))

      board = reversi.from_dictionary_to_array_board(state.board, 8, 8)

      if (state.is_player_max(state.next_player)):
        player1 = state.next_player.label
        player2 = state.previous_player.label
      else:
        player1 = state.previous_player.label
        player2 = state.next_player.label

      # compara las puntuaciones de los jugadores para determinar movimiento mas conveniente

      h = (player_score(board, player2) - player_score(board, player1)) / \
          (player_score(board, player2) + player_score(board, player1))

      #movimiento más favorable
      for cell in ccell:
        if (board[cell[0]][cell[1]] == player1):
          h = h + 30
        elif (board[cell[0]][cell[1]] == player2):
          h = h - 30

      # movimiento que favorece movimientos desfavorables para el enemigo
      for cell in addadcells:
        if (board[cell[0]][cell[1]] == player1):
          h = h + 4
        elif (board[cell[0]][cell[1]] == player2):
          h = h - 4

      # bordes cunden
      for cell in bcells:
        if (board[cell[0]][cell[1]] == player1):
          h = h + 20
        elif (board[cell[0]][cell[1]] == player2):
          h = h - 20

      # obliga al enemigo a entregar borde
      for cell in addaddbcells:
        if (board[cell[0]][cell[1]] == player1):
          h = h + 2
        elif (board[cell[0]][cell[1]] == player2):
          h = h - 2

      # movimientos que favorecen que el adversario consiga esquinas (por tanto desfavoreables)
      for cell in acells:
        if (board[cell[0]][cell[1]] == player1):
          h = h - 6
        elif (board[cell[0]][cell[1]] == player2):
          h = h + 6

      for cell in dcells:
        if (board[cell[0]][cell[1]] == player1):
          h = h - 15
        elif (board[cell[0]][cell[1]] == player2):
          h = h + 15

      # entrega borde = malo
      for cell in addbcells:
        if (board[cell[0]][cell[1]] == player1):
          h = h - 10
        elif (board[cell[0]][cell[1]] == player2):
          h = h + 10

      return h


class Heuristic4(StudentHeuristic):
  def get_name(self) -> str:
    return "transeando"

  #Evaluamos si es posible que las fichas que se situan mas hacia el centro del tablero pueden ser cambiadas tras el movimiento
  def aVerEstaTransa(self, x, y, playerP, board) -> int:
    i = 0
    if (x > 4 and y > 3):
      if (x-1 > 0 and board[x-1][y] != playerP):
        i = i+6
        if (x-2 > 0 and board[x-2][y] != playerP  ):
          i = i+6
      if (y+1 < 7 and board[x][y+1] != playerP):
        i = i+6
        if (y+2 <7 and board[x][y+2] != playerP  ):
          i = i+6
    elif (x > 3 and y < 3):
      if (x+1 < 7 and board[x+1][y] != playerP):
        i = i+6
        if (x+2 < 7 and board[x+2][y] != playerP):
          i = i+6
      if (y+1 < 7 and board[x][y+1] != playerP):
        i = i+6
        if (y+2 < 7 and board[x][y+2] != playerP  ):
          i = i+6
    elif (x < 3 and y > 4):
      if (x+1 < 7 and board[x+1][y] != playerP):
        i = i+6
        if (x+2 < 7 and board[x+2][y] != playerP  ):
          i = i+6
      if (y-1 > 0 and board[x][y-1] != playerP):
        i = i+6
        if (y-2 > 0 and board[x][y-2] != playerP):
          i = i+6
    elif (x > 4 and y > 4):
      if (x-1 > 0 and board[x-1][y] != playerP  ):
        i = i+6
        if (x-2 > 0 and board[x-2][y] != playerP  ):
          i = i+6
      if (y-1 > 0 and board[x][y-1] != playerP  ):
        i = i+6
        if ( y-2 > 0 and board[x][y-2] != playerP ):
          i = i+6
    return i


  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    #valor heuristica
    h = 0

    #esquinas
    ccell = ((0, 0), (0, 7), (7, 0), (7, 7))

    #adyacente a esquinas
    addadcells = ((0, 2), (1, 2), (2, 2), (2, 1), (5, 0), (5, 1), (5, 2), (6, 2), (6, 1),
                  (0, 5), (1, 5), (2, 5), (2, 6), (2, 7), (5, 5), (5, 6), (5, 7), (6, 5), (7, 5))

    #diagonal a esquinas
    dcells = ((1, 1), (1, 6), (6, 1), (6, 6))

    #adyacente a esquinas
    acells = ((0, 1), (1, 0), (0, 6), (1, 7), (6, 0), (7, 1), (6, 7), (7, 6))

    #bordes
    bcells = ((0, 3), (0, 4), (3, 0), (4, 0), (7, 3), (7, 4), (3, 7), (4, 7))

    #addyacent to bcells
    addbcells = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (3, 1), (4, 1),
                 (5, 1), (6, 2), (6, 3), (6, 4), (6, 5), (2, 6), (3, 6), (4, 6), (5, 6))

    #addyacent to addyacent to bcells
    addaddbcells = ((2, 2), (2, 3), (2, 4), (2, 5), (2, 2), (3, 2), (4, 2),
                    (5, 2), (5, 2), (5, 3), (5, 4), (5, 5), (2, 5), (3, 5), (4, 5), (5, 5))

    board = reversi.from_dictionary_to_array_board(state.board, 8, 8)

    if (state.is_player_max(state.next_player)):
      player1 = state.next_player.label
      player2 = state.previous_player.label
    else:
      player1 = state.previous_player.label
      player2 = state.next_player.label

    #Comprobamos si nos encontrsamos en una partida "Early" o mas avanzada "Late"
    #En un estado mas joven de la partida es conveniente que se de prioridad a las casillas qeu den mas movilidad (esquinas y lados)
    turnsLeft = 0
    for x in range(0, 7):
      for y in range(0, 7):
        if ((board[x] [y] != player1) and (board[x][y] != player2)):
          turnsLeft = turnsLeft + 1

    if (turnsLeft < 24):
      Late = 0
    else:
      Late = 10
    # compara las puntuaciones de los jugadores para determinar movimiento mas conveniente

    h = (player_score(board, player2) - player_score(board, player1)) / \
        (player_score(board, player2) + player_score(board, player1))

    #movimiento más favorable
    for cell in ccell:
      if (board[cell[0]][cell[1]] == player1):
        h = h + 30 + \
            self.aVerEstaTransa( cell[0], cell[1], player1, board) + Late
      elif (board[cell[0]][cell[1]] == player2):
        h = h - 30 - \
            self.aVerEstaTransa(cell[0], cell[1], player2, board) - Late

    # movimiento que favorece movimientos desfavorables para el enemigo
    for cell in addadcells:
      if (board[cell[0]][cell[1]] == player1):
        h = h + 4 + self.aVerEstaTransa(cell[0], cell[1], player1, board)
      elif (board[cell[0]][cell[1]] == player2):
        h = h - 4 - self.aVerEstaTransa(cell[0], cell[1], player2, board)

    # bordes cunden
    for cell in bcells:
      if (board[cell[0]][cell[1]] == player1):
        h = h + 20 + \
            self.aVerEstaTransa( cell[0], cell[1], player1, board) + Late
      elif (board[cell[0]][cell[1]] == player2):
        h = h - 20 - \
            self.aVerEstaTransa(cell[0], cell[1], player2, board) - Late

    # obliga al enemigo a entregar borde
    for cell in addaddbcells:
      if (board[cell[0]][cell[1]] == player1):
        h = h + 2 + \
            self.aVerEstaTransa(cell[0], cell[1], player1, board) + Late
      elif (board[cell[0]][cell[1]] == player2):
        h = h - 2 - \
            self.aVerEstaTransa(cell[0], cell[1], player2, board) - Late

    # movimientos que favorecen que el adversario consiga esquinas (por tanto desfavoreables)
    for cell in acells:
      if (board[cell[0]][cell[1]] == player1):
        h = h - 6
      elif (board[cell[0]][cell[1]] == player2):
        h = h + 6

    for cell in dcells:
      if (board[cell[0]][cell[1]] == player1):
        h = h - 15
      elif (board[cell[0]][cell[1]] == player2):
        h = h + 15

    # entrega borde = malo
    for cell in addbcells:
      if (board[cell[0]][cell[1]] == player1):
        h = h - 10
      elif (board[cell[0]][cell[1]] == player2):
        h = h + 10

    return h



def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:

    initial_board = None#np.zeros((dim_board, dim_board))
    initial_player = player1

    """game = TicTacToe(
        player1=player1,
        player2=player2,
        dim_board=dim_board,
    )"""

    initial_board = (
        ['.......',
        '...BW..',
        '.BWBB..',
        '...W...',
        '.......']
    )

    if initial_board is None:
        height, width = 8, 8
    else:
        height = len(initial_board)
        width = len(initial_board[0])
        try:
            initial_board = from_array_to_dictionary_board(initial_board)
        except ValueError:
            raise ValueError('Wrong configuration of the board')
        else:
            print("Successfully initialised board from array")

    game = Reversi(
        player1=player1,
        player2=player2,
        height=8,
        width=8
    )

    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_seconds_per_move=1000, gui=False)


tour = Tournament(max_depth=3, init_match=create_match)
# if the strategies are copy-pasted here:
strats = {'opt1': [Heuristic1], 'opt2': [Heuristic2]}
          #'opt3': [Heuristic3], 'opt4': [Heuristic4]}
# if the strategies should be loaded from files in a specific folder:
# folder_name = "folder_strat" # name of the folder where the strategy files are located
# strats = tour.load_strategies_from_folder(folder=folder_name, max_strat=3)

n = 1
scores, totals, names = tour.run(
    student_strategies=strats,
    increasing_depth=False,
    n_pairs=n,
    allow_selfmatch=False,
)

print(
    'Results for tournament where each game is repeated '
    + '%d=%dx2 times, alternating colors for each player' % (2 * n, n),
)

# print(totals)
# print(scores)

print('\ttotal:', end='')
for name1 in names:
    print('\t%s' % (name1), end='')
print()
for name1 in names:
    print('%s\t%d:' % (name1, totals[name1]), end='')
    for name2 in names:
        if name1 == name2 or name2 not in scores[name1]:
            print('\t---', end='')
        else:
            print('\t%d' % (scores[name1][name2]), end='')
    print()
