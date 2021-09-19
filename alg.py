import numpy as np
n = 20

class array:
    def __init__(self, n):
        """
        Initializes a square of size n.
        """
        self.n = n
        self.array = np.zeros([3,n* n], dtype=int)
        self.flips = []

        self.s = []
        self.f = []

        for i in range(self.n * self.n):
            self.array[0,i] = np.ceil((i + 1) / self.n - 1)
            self.array[1,i] = i % self.n

    def add(self, elements):
        """
        Adds elements to the array.
        """
        for e in elements:
            for i in range(self.n * self.n):
                element = [j[i] for j in self.array]
                if element[0] == e[0] and element[1] == e[1]:
                    self.array[2,i] = e[2]
                    break
                if i == len(self.array[0]) - 1:
                    print("element " + str(e) + " could not be added")

    def find(self, e):
        """
            Finds the element e in the array. e is described by the row and
            collumn in the table.
        """
        for i in range(self.n * self.n):
            element = [j[i] for j in self.array]
            if element[0] == e[0] and element[1] == e[1]:
                return element

    def show(self):
        """
            Displays the array as a square.
        """

        #finds every element and stores it in order
        elements = [[0 for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n * self.n):
            elements[self.array[0,i]][self.array[1,i]] = self.array[2,i]

        #prints the table
        for i in range(self.n):
            line = ""
            for j in range(self.n):
                line += str(elements[i][j])
                if j != self.n - 1:
                    line += "|"
            print(line)
        print()

    def permute(self, e, write=False):
        """
            permutes the array by applying the switch e
            Switches are of form [0,0,1], where the first element chooses whether
            to swap two columns or two rows or to renumber,
            0 for rows, 1 for columns, 2 for renumbering.
            Write determines is the permutations are remembered.
        """
        for i in range(self.n * self.n):
            if self.array[e[0],i] == e[1]:
                self.array[e[0],i] = e[2]
            elif self.array[e[0],i] == e[2]:
                self.array[e[0],i] = e[1]
        if write == True:
            self.flips.append(e)

    def permute_rows(self, e, write=False):
        """
            permutes the rows given in e
        """
        e.insert(0, 0)
        self.permute(e, write)

    def permute_cols(self, e, write=False):
        """
            permutes the columns given in e
        """
        e.insert(0, 1)
        self.permute(e, write)

    def renumber(self, e, write=False):
        """
            renumbers the elements given in e
        """
        e.insert(0, 2)
        self.permute(e, write)

    def exchange(self, e):
        """
            Switches 2 elements in the array.
        """
        e0 = []
        e1 = []

        e0 = self.find(e[0])
        e1 = self.find(e[1])

        for i in range(self.n * self.n):
            element = [j[i] for j in self.array]
            if element[0] == e[0][0] and element[1] == e[0][1]:
                self.array[2,i] = e1[2]
            if element[0] == e[1][0] and element[1] == e[1][1]:
                self.array[2,i] = e0[2]

    def reverse(self):
        """
            reverses the changes made by the permutations
        """
        self.flips.reverse()
        for e in self.flips:
            self.permute(e, False)
        self.flips = []

    def firststep(self):
        """
            The first step of the algorithm. Calculates s and f, and
            renumbers the biggest element, which it moves to the top.
        """
        appearances = [0 for i in range(self.n)]
        min_row = self.n - 1

        #counts how many times each number appears
        for i in range(self.n * self.n):
            e = self.array[2,i]
            if e != 0:
                appearances[e - 1] += 1
                if self.array[0,i] < min_row:
                    min_row = self.array[0,i]

        #renumbers if there is no or there are multiple instances of self.n
        if appearances[self.n - 1] != 1:
            for i in range(len(appearances)):
                if appearances[i] == 1:
                    self.renumber([i + 1, self.n], True)
                    break

        #permutes the rows so the largest number is in the first row with numbers
        for i in range(self.n * self.n):
            if self.array[2,i] == self.n:
                row = self.array[0,i]
                if row != min_row:
                    self.permute_rows([min_row, row], True)
                break

        #finds the amount of numbers in each row with numbers
        rows = [[] for i in range(self.n)]
        for i in range(self.n * self.n):
            if self.array[2,i] != 0:
                rows[self.array[0,i]].append(self.array[2,i])

        #calculates s and f
        for i in range(self.n):
            if rows[i] != []:
                self.s.append(i)
                self.f.append(len(rows[i]))


    def secondstep(self):
        """
            The second step of the algorithm. Makes sure all elements are in the
            lower triangle and only the element size.n is on the diagonal,
            in the highest row where there are numbers.
        """

        if self.s != []:

            #permutes the rows so they are at the right place
            self.permute_rows([self.s[0],self.f[0]-1], True)
            for i in range(1,len(self.s)):
                dest = sum(self.f[:i+1])
                self.permute_rows([self.s[i], dest], True)

            #permutes the columns so every number is in the lower triangle.
            for j in range(self.n):
                for i in range(self.n * self.n):
                    #puts self.n on the diagonal
                    if self.array[0,i] == j and self.array[2,i] == self.n:
                        self.permute_cols([j,self.array[1,i]], True)
                    #puts the other numbers in the lower triangle
                    elif self.array[0,i] == j and self.array[2,i] != 0 and self.array[1,i] >= self.array[0,i]:
                        self.permute_cols([j-1,self.array[1,i]], True)

    def solve(self):
        """
            Solves the Latin square by the algorithm from Proofs.
        """
        print(self.n)
        self.firststep()
        self.secondstep()

        to_add = []
        #base case
        if self.n == 1:
            self.complete()
            to_add = [[0,0,1]]
        #induction step
        else:
            #makes a smalller latin square with every element except self.n
            smaller = array(self.n-1)
            for i in range(self.n * self.n):
                if self.array[0,i] != 0 and self.array[1,i] != self.n - 1 and self.array[2,i] != self.n:
                    e = [self.array[0,i] - 1, self.array[1,i], self.array[2,i]]
                    to_add.append(e)
            smaller.add(to_add)

            #solves the smaller square and adds the solved numbers into the array
            to_add = smaller.solve()
            to_add = [[to_add[i][0] + 1, to_add[i][1], to_add[i][2]] for i in range(len(to_add))]
            self.add(to_add)

            #creates the last column by the swap algorithm and solves the first row
            self.swap()
            self.complete()

            #reverse the swaps of the first and second step
            self.reverse()

            #sends all numbers to a larger square
            to_add = []
            for i in range(self.n * self.n):
                    e = [self.array[0,i], self.array[1,i], self.array[2,i]]
                    to_add.append(e)
        print(self.n)
        return to_add

    def swap(self):
        """
            Executes the swapping algortihm from Proofs.
        """
        last_col = [0 for i in range(self.n)]
        for i in range(1,self.n - 1):
            #puts self.n on the place in the last column on row i and
            #swaps it with the number on the diagonal
            self.add([[i, self.n - 1, self.n]])
            self.exchange([[i, self.n - 1], [i, i]])


            e = self.find([i, self.n - 1])
            #swaps elements until the last column is solved upto row i
            while(e[2] in last_col[0:e[0]] or e[2] in last_col[e[0] + 1:]):
                #perform a swap and update the last column
                row = last_col.index(e[2])
                self.exchange([[row, self.n - 1], [row, i]])
                last_col = [self.find([j, self.n - 1])[2] for j in range(self.n)]

                #next element to check uniqueness of in the last column
                e = self.find([row, self.n - 1])

            last_col[i] = self.find([i, self.n - 1])[2]


    def complete(self):
        """
            Completes the square by filling in the first row and the last element.
        """
        self.add([[self.n - 1, self.n - 1, self.n]])

        #looks which elements are in which columns
        columns = [[] for i in range(self.n)]
        for i in range(self.n * self.n):
            columns[self.array[1,i]].append(self.array[2,i])

        #add the missing element to every column
        for i in range(len(columns)):
            for j in range(1,self.n + 1):
                if j not in columns[i]:
                    self.add([[0, i, j]])
                    break

    def check(self):
        """
            checks if the object is a latin square
        """
        rows = [[] for i in range(self.n)]
        cols = [[] for i in range(self.n)]

        for i in range(self.n * self.n):
            rows[self.array[0,i]].append(self.array[2,i])
            cols[self.array[1,i]].append(self.array[2,i])

        il = True
        for i in range(self.n):
            for j in range(self.n):
                if j+1 not in rows[i] or j+1 not in cols[i]:
                    il = False
        if il:
            print("Is a Latin square!")
        else:
            print("Is not a Latin square.")





square = array(n)
square.check()
square.add([[0,0,1],[0,1,5]])
square.show()
square.solve()
square.check()
square.show()