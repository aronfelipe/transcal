import numpy as np

class Element:

    def __init__(self, x_cord_1, y_cord_1, x_cord_2, y_cord_2, A, E, nodes):
        self.x = x_cord_2 - x_cord_1
        self.y = y_cord_2 - y_cord_1

        self.l = np.sqrt(self.x**2+self.y**2)
        self.a = A
        self.e = E

        self.s = self.y/self.l
        self.c = self.x/self.l

        self.dof = [int(nodes[0]*2-2), int(nodes[0]*2-1), int(nodes[1]*2-2), int(nodes[1]*2-1)]

        print(self.dof)

    def generate_matrix(self):
        matrix_ke = np.matrix([[self.c**2, self.c*self.s, -self.c*2, -self.c*self.s],
                               [self.c*self.s, self.s**2, -self.c*self.s, -self.s**2], 
                               [-self.c**2, -self.c*self.s, self.c**2, self.c*self.s],
                               [-self.c*self.s, -self.s**2, self.c*self.s, self.s**2]])
        
        return matrix_ke

    def calculate_k(self):
        self.k = ((self.e*self.a)/self.l) * self.generate_matrix()
        return self.k