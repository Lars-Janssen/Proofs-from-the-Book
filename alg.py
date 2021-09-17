import numpy as np
n = 4

def init(n):
    array = np.zeros([3,n* n])
    for i in range(n * n):
        array[0,i] = np.ceil((i + 1) / n - 1)
        array[1,i] = i % n
    return array

def add(array, elements):
    for e in elements:
        for i in range(len(array[0])):
            if array[0,i] == e[0] and array[1,i] == e[1]:
                array[2,i] = e[2]
                break
            if i == len(array[0]) - 1:
                print("element " + str(e) + " could not be added")
    return array

def show(array, n):
    for i in range(n):
        line = ""
        for j in range(n):
            for e in range(len(array[0])):
                if array[0,e] == i and array[1,e] == j:
                    line += str(int(array[2,e]))
            if j != n - 1:
                line += "|"
        print(line)



array = init(n)
array = add(array, [[1,0,2],[3,3,4]])
show(array, n)