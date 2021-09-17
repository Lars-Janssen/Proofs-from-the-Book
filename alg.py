import numpy as np
n = 4


class array:
    def __init__(self, n):
        """
        initializes a square of size n
        """
        self.n = n
        self.array = np.zeros([3,n* n])
        self.flips = []
        for i in range(self.n * self.n):
            self.array[0,i] = np.ceil((i + 1) / self.n - 1)
            self.array[1,i] = i % self.n

    def add(self, elements):
        """
        adds elements to the array
        """
        for e in elements:
            for i in range(self.n * self.n):
                if self.array[0,i] == e[0] and self.array[1,i] == e[1]:
                    self.array[2,i] = e[2]
                    break
                if i == len(self.array[0]) - 1:
                    print("element " + str(e) + " could not be added")

    def show(self):
        """
        displays the array as a square
        """
        for i in range(self.n):
            line = ""
            for j in range(self.n):
                for e in range(len(self.array[0])):
                    if self.array[0,e] == i and self.array[1,e] == j:
                        line += str(int(self.array[2,e]))
                if j != n - 1:
                    line += "|"
            print(line)
        print()

    def permute(self, switches=[], write=True):
        """
            permutes the array by applying the switches
            Switches are of form [0,0,1], where the first element chooses whether
            to swap two columns or two rows, 0 for columns, 1 for rows
        """
        for e in switches:
            for i in range(self.n * self.n):
                if self.array[e[0],i] == e[1]:
                    self.array[e[0],i] = e[2]
                elif self.array[e[0],i] == e[2]:
                    self.array[e[0],i] = e[1]
            if write == True:
                self.flips.append(e)


    def reverse(self):
        self.flips.reverse()
        self.permute(self.flips, False)
        self.flips = []


square = array(n)
square.add([[0,0,2],[1,1,3]])
square.permute([[1,0,1]])
square.permute([[0,2,1]])
square.reverse()
square.show()
