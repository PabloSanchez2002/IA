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

def func_glob(n: int, state: TwoPlayerGameState) -> float:
  return n + simple_evaluation_function(state)

def player_score(board: dict, player_label) -> float:
  score = 0
  for x in range(0,8):
    for y in range(0,8):
      if board[x][y] == player_label:
        score = score + 1
  return score

class Solution1(StudentHeuristic):
  def get_name(self) -> str:
    return "catxo camino heuristica de los xavales"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    #valor heuristica
    h = 0

    #esquinas
    ccell = ((0,0), (0,7), (7,0), (7,7))
    
    #adyacente a esquinas 
    addadcells = ((0,2), (1,2), (2,2), (2,1), (5,0), (5,1), (5,2), (6,2), (6,1), (0,5), (1,5), (2,5), (2,6), (2,7), (5,5), (5,6), (5,7), (6,5), (7,5))
 
    #diagonal a esquinas
    dcells = ((1,1), (1,6), (6,1), (6,6))

    #adyacente a esquinas
    acells = ((0,1), (1,0), (0,6), (1,7), (6,0), (7,1), (6,7), (7,6))   
    

    board = reversi.from_dictionary_to_array_board(state.board, 8, 8)

    if (state.is_player_max(state.next_player)):
      player1 = state.next_player.label
      player2 = state.previous_player.label
    else:
      player1 = state.previous_player.label
      player2 = state.next_player.label
    
    # compara las puntuaciones de los jugadores para determinar movimiento mas conveniente

    h = (player_score(board, player2) - player_score(board, player1) ) / (player_score(board, player2) + player_score(board, player1))

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



class Solution2(StudentHeuristic):
  def get_name(self) -> str:
    return "pura transa d heuristk mejor ke wise old tree"
  def evaluation_function(self, state: TwoPlayerGameState) -> float:
    #valor heuristica
    h = 0

    #esquinas
    ccell = ((0,0), (0,7), (7,0), (7,7))
    
    #adyacente a esquinas 
    addadcells = ((0,2), (1,2), (2,2), (2,1), (5,0), (5,1), (5,2), (6,2), (6,1), (0,5), (1,5), (2,5), (2,6), (2,7), (5,5), (5,6), (5,7), (6,5), (7,5))
 
    #diagonal a esquinas
    dcells = ((1,1), (1,6), (6,1), (6,6))

    #adyacente a esquinas
    acells = ((0,1), (1,0), (0,6), (1,7), (6,0), (7,1), (6,7), (7,6))   
    
    #bordes
    bcells = ((0,2), (0,3), (0,4), (0,5), (2,0), (3,0), (4,0), (5,0), (7,2), (7,3), (7,4), (7,5), (2,7), (3,7), (4,7), (5,7))

    #addyacent to bcells
    addbcells = ((1,2), (1,3), (1,4), (1,5), (2,1), (3,1), (4,1), (5,1), (6,2), (6,3), (6,4), (6,5), (2,6), (3,6), (4,6), (5,6))
    
    #addyacent to addyacent to bcells
    addaddbcells = ((2,2), (2,3), (2,4), (2,5), (2,2), (3,2), (4,2), (5,2), (5,2), (5,3), (5,4), (5,5), (2,5), (3,5), (4,5), (5,5))

    board = reversi.from_dictionary_to_array_board(state.board, 8, 8)

    if (state.is_player_max(state.next_player)):
      player1 = state.next_player.label
      player2 = state.previous_player.label
    else:
      player1 = state.previous_player.label
      player2 = state.next_player.label
    
    # compara las puntuaciones de los jugadores para determinar movimiento mas conveniente

    h = (player_score(board, player2) - player_score(board, player1) ) / (player_score(board, player2) + player_score(board, player1))

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


class Solution3(StudentHeuristic):
  def get_name(self) -> str:
    return "transeando la transa transeante de la purta transa"

  #Evaluamos si es posible que las fichas que se situan mas hacia el centro del tablero pueden ser cambiadas tras el movimiento
  def aVerEstaTransa(self, x, y, playerP, board) -> int:
    i = 0
    if (x > 4 and y > 3):
      if (x-1 > 0 and board[x-1][y] != playerP):
        i = i+6
        if (x-2 > 0 and board[x-2][y] != playerP):
          i = i+6
      if (y+1 < 7 and board[x][y+1] != playerP):
        i = i+6
        if (y+2 < 7 and board[x][y+2] != playerP):
          i = i+6
    elif (x > 3 and y < 3):
      if (x+1 < 7 and board[x+1][y] != playerP):
        i = i+6
        if (x+2 < 7 and board[x+2][y] != playerP):
          i = i+6
      if (y+1 < 7 and board[x][y+1] != playerP):
        i = i+6
        if (y+2 < 7 and board[x][y+2] != playerP):
          i = i+6
    elif (x < 3 and y > 4):
      if (x+1 < 7 and board[x+1][y] != playerP):
        i = i+6
        if (x+2 < 7 and board[x+2][y] != playerP):
          i = i+6
      if (y-1 > 0 and board[x][y-1] != playerP):
        i = i+6
        if (y-2 > 0 and board[x][y-2] != playerP):
          i = i+6
    elif (x > 4 and y > 4):
      if (x-1 > 0 and board[x-1][y] != playerP):
        i = i+6
        if (x-2 > 0 and board[x-2][y] != playerP):
          i = i+6
      if (y-1 > 0 and board[x][y-1] != playerP):
        i = i+6
        if (y-2 > 0 and board[x][y-2] != playerP):
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
        if ((board[x][y] != player1) and (board[x][y] != player2)):
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
            self.aVerEstaTransa(cell[0], cell[1], player1, board) + Late
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
            self.aVerEstaTransa(cell[0], cell[1], player1, board) + Late
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




