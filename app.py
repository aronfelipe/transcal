from read import EntryReader

import numpy as np

class Element:

    def __init__(self, x_cord_1, y_cord_1, x_cord_2, y_cord_2, A, E, list_nodes):
        self.x = x_cord_2 - x_cord_1
        self.y = y_cord_2 - y_cord_1

        self.l = np.sqrt(x**2+y**2)
        self.a = A
        self.e = E

        self.s = y/self.l
        self.c = x/self.l

        self.gol = [nodes[0]*2-2, nodes[0]*2-1,nodes[1]*2-2,nodes[1]*2-1]

    def generate_matrix(self):
        matrix_ke = np.matrix([[self.c**2, self.c*s, -self.c*2, -self.c*self.s],
                               [self.c*self.s, self.s**2, -self.c*self.s, -self.s**2], 
                               [-self.c**2, -self.c*self.s, self.c**2, self.c*self.s],
                               [-self.c*self.s, -self.s**2, self.c*self.s, self.s**2]])
        return matrix_ke

    def calculate_k(self):
        self.k = (((self.e*self.a)/self.l) * self.gerar_matrix_ke())
        return ke

class Bridge:

    def __init__(self, elements, loading_vector, ):
        self.elements = elements
        self.u = u
        self.n_nodes = n_nodes
        self.restriction_vector = restriction_vector
        self.loading_vector = loading_vector

    def generate_matrix_g(self):

        # Generating matrix with dimensions n_nodes*2Xn_nodes*2

        matrix_g = np.zeros([self.n_nodes*2, self.n_nodes*2])

        # Consctructing the global matrix for the bridge 
        # taking into account the degrees of freedom of each of the elements
        # grouping each matrix of the elements into matrixes of 2x2 elements

        for element in self.elements:
            matrix_g[element.gol[0]:element.gol[1] + 1, element.gol[0]:element.gol[0]+1] += element.k[0:2, 0:2]
            matrix_g[element.gol[2]:element.gol[3] + 1, element.gol[2]:element.gol[3]+1] += element.k[2:4, 2:4]
            matrix_g[element.gol[0]:element.gol[1] + 1, element.gol[2]:element.gol[3]+1] += element.k[0:2, 2:4]
            matrix_g[element.gol[2]:element.gol[3] + 1, element.gol[0]:element.gol[0]+1] += element.k[2:4, 0:2]

        return matrix_g

    def contornate_matrix_g(self, matrix_g):

        matrix_g_c = np.delete(matrix_g, self.restriction_vector, 0)
        matrix_g_c = np.delete(matrix_g_c, self.restriction_vector, 1)

        loading_vector_c = np.delete(self.loading_vector, self.restriction_vector, 0)

        for force in loading_vector:
            self.loading_vector_c.append(i[0])

class App:

    def __init__(self, entry):
        self.reader = EntryReader(entry)

    def generate_list_nodes(self):
        list_nodes = []
        for i in self.reader.incidence_matrix:
            list_nodes.append(np.array([int(i[0]),int(i[1])]))
            
        return list_nodes
        
    def numerate_gol(self):
        list_gol = []
        for i in range (1, self.reader.n_nodes+1):
            if len(list_gol) < 1:
                list_gol.append([i,1, 2])
            else:
                list_gol.append([i,list_gol[-1][2] + 1, list_gol[-1][2] + 2])

        return list_gol


app = TreApp("entrada.xlsx")
print(app.generate_list_nodes())
print(app.numerate_gol())

elements_list = []

for element in app.numerate_gol():
    print(element)

