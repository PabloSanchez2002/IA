from ast import literal_eval
import numpy as np

#calculo MinMax
f = open("medidasMinMax.txt", 'r')
medidasMinMax = f.readlines()
new_list1 = []
for line in medidasMinMax:
    new_list1.append(literal_eval(line)) 
averageMinMax = str(np.mean(new_list1))

#calculo AlfaBeta
f = open("medidasAlfaBeta.txt", 'r')
medidasAlfaBeta = f.readlines()
new_list2 = []
for line in medidasAlfaBeta:
    new_list2.append(literal_eval(line))
averageAlfaBeta = str(np.mean(new_list2))


print("averageMinMax = " + averageMinMax )
print("averageAlfaBeta = " + averageAlfaBeta)
print("cociente averageMinMax/averageAlfaBeta = " +
      str(np.mean(new_list1)/np.mean(new_list2)))
