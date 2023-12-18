# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):

#   Search the deepest nodes in the search tree first."""

#     Your search algorithm needs to return a list of actions that reaches the
#     goal. Make sure to implement a graph search algorithm.

#     To get started, you might want to try some of these simple commands to
#     understand the search problem that is being passed in:

#     print("Start:", problem.getStartState())
#     print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
#     print("Start's successors:", problem.getSuccessors(problem.getStartState()))
#     """
#     "*** YOUR CODE HERE ***"

    from game import Directions
   
    #Estados a explorar en stack (LIFO). Almacena nodos tipo (state, action)
    unexploredNodes = util.Stack()
    #Estados visitados recientemente (para checkear y evitar bucles), solo almacena states
    exploredNodes = []
    #Definimos nodo inicial
    initNode = (problem.getStartState(), [])

    unexploredNodes.push(initNode)

    while not unexploredNodes.isEmpty():
        #empezamos a explorar el nodo no explorado mas reciente añadido a la pila
        currentState, movements = unexploredNodes.pop()
        
        if currentState not in exploredNodes:
            #marcar nodo actual como visitado
            exploredNodes.append(currentState)
        
            if problem.isGoalState(currentState):
                return movements
            else:
                #obtiene lista de posibles sucesores del nodo
                #formato (successor, action, cost)
                succ = problem.getSuccessors(currentState)
                
                #pusheamos cada sucesor en unexploredNodes
                for succState, succMovement, succCost in succ:
                    newMovement = movements + [succMovement]
                    newNode = (succState, newMovement)
                    unexploredNodes.push(newNode)
                
    return None  

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #Estados a explorar en cola (FIFO). Almacena nodos tipo (state, action)
    unexploredNodes = util.Queue()
    #Estados visitados recientemente (para checkear y evitar bucles), solo almacena states
    exploredNodes = []
    #Definimos nodo inicial
    initNode = (problem.getStartState(), [])

    unexploredNodes.push(initNode)

    while not unexploredNodes.isEmpty():
        #empezamos a explorar el nodo no explorado mas reciente añadido a la pila
        currentState, movements = unexploredNodes.pop()
        
        if currentState not in exploredNodes:
            #marcar nodo actual como visitado
            exploredNodes.append(currentState)
        
            if problem.isGoalState(currentState):
                return movements
            else:
                #obtienelista de posibles sucesores del nodo
                #formato (successor, action, cost)
                succ = problem.getSuccessors(currentState)
                
                #pusheamos cada sucesor en unexploredNodes
                for succState, succMovement, succCost in succ:
                    newMovement = movements + [succMovement]
                    newNode = (succState, newMovement)
                    unexploredNodes.push(newNode)
                
    return None  
    
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    #Estados a explorar en cola (ordenados por coste de mayor a menor). Almacena nodos tipo (state, cost)
    unexploredNodes = util.PriorityQueue()
    #Estados visitados recientemente (para checkear y evitar bucles), almacena states 
    exploredNodes = {}
    #Definimos nodo inicial
    initNode = (problem.getStartState(), [], 0)   #tenemos que añadir el coste de este (state, movimiento, coste acumulado)

    unexploredNodes.push(initNode, 0)

    while not unexploredNodes.isEmpty():
        #empezamos a explorar el nodo no explorado mas reciente añadido a la pila
        currentState, movements, cost  = unexploredNodes.pop()
        
        if (currentState not in exploredNodes) or (cost < exploredNodes[currentState]): 
            #marcar nodo actual como visitado y guardamos su valor de costo
            exploredNodes[currentState] = cost
        
            if problem.isGoalState(currentState):
                return movements
            else:
                #obtienelista de posibles sucesores del nodo
                
                succ = problem.getSuccessors(currentState)
                
                #pusheamos cada sucesor en unexploredNodes
                for succState, succMovement, succCost in succ:
                    newMovement = movements + [succMovement]
                    newCost = cost + succCost

                    #formato (successor, action, cost)
                    newNode = (succState, newMovement, newCost)

                    unexploredNodes.update(newNode, newCost)
                
    return None  
    
    
    
     
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #Estados a explorar en cola (ordenados por coste (heuristica + coste) de mayor a menor). Almacena nodos tipo (state, cost)
    queue = util.PriorityQueue()

    #Definimos nodo inicial
    initNode = (problem.getStartState(), [], 0)

    #Estados visitados recientemente (para checkear y evitar bucles), almacena states 
    exploredNodes = {}

    queue.push(initNode, heuristic(initNode[0], problem))

    while not queue.isEmpty():
        #empezamos a explorar el nodo no explorado mas barato de la pila
        currentState, actions, cost = queue.pop()

        if (currentState not in exploredNodes) or (cost < exploredNodes[currentState]): 
            #marcar nodo actual como visitado y guardamos su valor de costo
            exploredNodes[currentState] = cost

            if problem.isGoalState(currentState):
                return actions
            else:
                succ = problem.getSuccessors(currentState)

            #obtienelista de posibles sucesores del nodo
            for succState, succMovement, succCost in succ:
                    newMovement = actions + [succMovement]
                    newCost = cost + succCost
                    
                    #Se calcula prioridad coste + heuristica
                    fn = newCost + heuristic(succState, problem)

                    #formato (successor, action, cost)
                    newNode = (succState, newMovement, newCost)

                    queue.update(newNode, fn)
    
    return None
                
            

    return 0
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
