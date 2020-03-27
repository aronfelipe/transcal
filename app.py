from read import EntryReader
import numpy as np

class Element:

    def __init__(x_cord_1, y_cord_1, x_cord_2, y_cord_2, A, E, list_nodes):
        self.x = x_cord_2 - x_cord_1
        self.y = y_cord_2 - y_cord_1

        self.l = np.sqrt(x**2+y**2)
        self.a = A
        self.e = E

        self.s = y/self.l
        self.c = x/self.l

        self.gol = [nodes[0]*2-2, nodes[0]*2-1,nodes[1]*2-2,nodes[1]*2-1]

class TreApp:

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
print(app.numerate_gdl())
