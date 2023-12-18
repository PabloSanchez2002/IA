"""Strategies for two player games.

   Authors:
        Fabiano Baroni <fabiano.baroni@uam.es>,
        Alejandro Bellogin Kouki <alejandro.bellogin@uam.es>
        Alberto Suárez <alberto.suarez@uam.es>
"""

from __future__ import annotations  # For Python 3.7

from abc import ABC, abstractmethod
from typing import List

import numpy as np
import time

from game import TwoPlayerGame, TwoPlayerGameState
from heuristic import Heuristic


class Strategy(ABC):
    """Abstract base class for player's strategy."""

    def __init__(self, verbose: int = 0) -> None:
        """Initialize common attributes for all derived classes."""
        self.verbose = verbose

    @abstractmethod
    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""

    def generate_successors(
        self,
        state: TwoPlayerGameState,
    ) -> List[TwoPlayerGameState]:
        """Generate state successors."""
        assert isinstance(state.game, TwoPlayerGame)
        successors = state.game.generate_successors(state)
        assert successors  # Error if list is empty
        return successors


class RandomStrategy(Strategy):
    """Strategy in which moves are selected uniformly at random."""

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""
        successors = self.generate_successors(state)
        return np.random.choice(successors)


class ManualStrategy(Strategy):
    """Strategy in which the player inputs a move."""

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move"""
        successors = self.generate_successors(state)

        assert isinstance(state.game, TwoPlayerGame)
        if gui:
            index_successor = state.game.graphical_input(state, successors)
        else:
            index_successor = state.game.manual_input(successors)

        next_state = successors[index_successor]

        if self.verbose > 0:
            print('My move is: {:s}'.format(str(next_state.move_code)))

        return next_state


class MinimaxStrategy(Strategy):
    """Minimax strategy."""

    def __init__(
        self,
        heuristic: Heuristic,
        max_depth_minimax: int,
        verbose: int = 0,
    ) -> None:
        super().__init__(verbose)
        self.heuristic = heuristic
        self.max_depth_minimax = max_depth_minimax

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Computa el siguiente estado en el juego"""
        #EMPEZAMOS A CONTAR EL TIMPO DE EJECUCION DEL ALGORITMO
        start = time.process_time()
        minimax_value, minimax_successor = self._maxxd(
            state,
            self.max_depth_minimax,
        )

        if self.verbose > 0:
            if self.verbose > 1:
                print('\nGame state before move:\n')
                print(state.board)
                print()
            print('Minimax value = {:.2g}'.format(minimax_value))

        #GUARDAMOS LOS VALORES EN UN .TXT
        ejecucion = str(time.process_time() - start)
        with open('medidasMinMax.txt', 'a') as f:
            f.write(ejecucion)
            f.write("\n")
        return minimax_successor

    def _minxd(
        self,
        state: TwoPlayerGameState,
        depth: int,
    ) -> float:
        """Paso Min del algoritmo"""

        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)
            minimax_successor = None
        else:
            minimax_value = np.inf

            for successor in self.generate_successors(state):
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value, _ = self._maxxd(
                    successor,
                    depth - 1,
                )

                if (successor_minimax_value < minimax_value):
                    minimax_value = successor_minimax_value
                    minimax_successor = successor

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value, minimax_successor

    def _maxxd(
        self,
        state: TwoPlayerGameState,
        depth: int,
    ) -> float:
        """Paso Max del algoritmo"""

        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)
            minimax_successor = None
        else:
            minimax_value = -np.inf

            for successor in self.generate_successors(state):
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value, _ = self._minxd(
                    successor,
                    depth - 1,
                )
                if (successor_minimax_value > minimax_value):
                    minimax_value = successor_minimax_value
                    minimax_successor = successor

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value, minimax_successor


class MinimaxAlphaBetaStrategy(Strategy):
    """Minimax alpha-beta strategy."""

    def __init__(
        self,
        heuristic: Heuristic,
        max_depth_minimax: int,
        verbose: int = 0,
    ) -> None:
        super().__init__(verbose)
        self.heuristic = heuristic
        self.max_depth_minimax = max_depth_minimax

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Computa el siguiente estado en el juego"""
        #EMPEZAMOS A CONTAR EL TIMPO DE EJECUCION DEL ALGORITMO
        start = time.process_time()
        #Primero obtenemos lso sucesores del estado 
        succs = self.generate_successors(state)

        # Asignamos el valor mas pequeño para alpha y el maximo para beta
        alpha = -np.inf
        beta = np.inf

        # Para cada sucesor del estado raiz
        for succ in succs:
            if self.verbose > 1:
                print('{}: [{},{}]'.format(state.board, alpha, beta))

            min_value = self._minxd(succ, self.max_depth_minimax, alpha, beta) 

            # Obtenemos el valor maximo para beta
            if (min_value > alpha):
                alpha = min_value
                minimax_successor = succ

        if self.verbose > 0:
            if self.verbose > 1:
                print('\nGame state before move:\n')
                print(state.board)
                print()
            print('Alpha value = {:.2g}'.format(alpha))
        #GUARDAMOS LOS VALORES EN UN .TXT
        ejecucion = str(time.process_time() - start)
        with open('medidasAlfaBeta.txt', 'a') as f:
            f.write(ejecucion)
            f.write("\n")
        return minimax_successor



    def _maxxd(
        self,
        state: TwoPlayerGameState,
        depth: int,
        alpha: int,
        beta: int,
    ) -> float:

        # Alcazaos el nivel mas bajo del ultimo nodod        
        if state.end_of_game or depth == 0:
            maxxd = self.heuristic.evaluate(state)
        else:
            maxxd = -np.inf

            succs = self.generate_successors(state)
            for succ in succs:
                # En el caso de que el mas bajo sea mayor que el mas alto, podemos hacer "pruning"
                # de esta rama
                if beta <= alpha:
                    break

                if self.verbose > 1:
                    print('{}: {}'.format(state.board, maxxd))

                minxd = self._minxd(
                    succ, depth - 1, alpha, beta,
                )

                # Obtenemos el maximo valor de todos los descendientes
                if minxd > maxxd:
                    maxxd = minxd

                # Queremos que alfa tenga el valor mayor de todos
                if maxxd > alpha:
                    alpha = maxxd


        if self.verbose > 1:
            print('{}: {}'.format(state.board, maxxd))

        return maxxd


    def _minxd(
        self,
        state: TwoPlayerGameState,
        depth: int,
        alpha: int,
        beta: int,
    ) -> float:
    
        # Alcazaos el nivel mas bajo del ultimo nodod
        if state.end_of_game or depth == 0:
            minxd = self.heuristic.evaluate(state)
        else:
            minxd = np.inf

            succs = self.generate_successors(state)
            for succ in succs:
                # En el caso de que el mas bajo sea mayor que el mas alto, podemos hacer "pruning"
                # de esta rama
                if (beta <= alpha):
                    break

                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minxd))

                maxxd = self._maxxd(
                    succ, depth - 1, alpha, beta,
                )

                # Obtenemos el menor valor de todos los descendientes
                if (maxxd < minxd):
                    minxd = maxxd

                # Queremos que beta tenga el valor mas pequeño
                if (minxd < beta):
                    beta = minxd

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minxd))

        return minxd