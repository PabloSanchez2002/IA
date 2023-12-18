#Estados a explorar en stack (LIFO). Almacena nodos tipo (state, action)
unexploredNodes = util.Stack()
#Estados visitados recientemente (para checkear y evitar bucles), solo almacena states
exploredNodes = []
#Definimos nodo inicial
initNode = (problem.getStartState(), [])

unexploredNodes.push(initNode)

while not unexploredNodes.isEmpty():
    #empezamos

