from element import Element
from reader import Reader

import numpy as np

class App:

    def __init__(self, entry):
        self.reader = Reader(entry)

    def generate_list_segments(self):
        self.list_segments = []
        for i in self.reader.incidence_matrix:
            self.list_segments.append(np.array([int(i[0]),int(i[1]), i[2], i[3]]))
        
    def generate_list_coordinates(self):
        self.list_coordinates = []
        for j in range(0, len(self.reader.nodes_matrix[0])):
            self.list_coordinates.append([i[j] for i in self.reader.nodes_matrix])

    def crete_elements(self):
        self.list_elements = []
        for element in self.list_segments:
            element = Element(
            x_cord_1=self.list_coordinates[int(element[0] - 1)][0],
            y_cord_1 = self.list_coordinates[int(element[0] - 1)][1],
            x_cord_2 = self.list_coordinates[int(element[1] - 1)][0],
            y_cord_2 = self.list_coordinates[int(element[1] - 1)][1],
            A = element[3], E = element[2], nodes=[element[0], element[1]])
            self.list_elements.append(element)   

    def generate_matrixes_k(self):
        list_matrixes_k = []
        for element in self.list_elements:
            list_matrixes_k.append(element.calculate_k())

app = App("entrada.xlsx")
app.generate_list_segments()
app.generate_list_coordinates()
app.crete_elements()
app.generate_matrixes_k()