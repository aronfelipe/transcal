from element import Element
from reader import Reader

import xlsx as xl
import numpy as np

class App:

    def __init__(self, entry):
        self.reader = Reader(entry)

    def plotStuff(self):
        return self.reader.nodes_matrix,self.reader.incidence_matrix

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
        self.list_matrixes_k = []
        for element in self.list_elements:
            self.list_matrixes_k.append(element.calculate_k())

    def generate_restriction_vector_origin(self):
        restrition_vector = []
        for i in range(self.reader.restrictions_vector.shape[0]):
            restrition_vector.append(np.array([(self.reader.restrictions_vector[i][0])]))
        return restrition_vector

    def generate_load_vector(self):
        load_vector = []
        for i in range(self.reader.loading_vector.shape[0]):
            load_vector.append(np.array([(self.reader.loading_vector[i][0])]))
        return load_vector
        
    def generate_restriction_vector(self,load_vector, restrition_vector_origin):
        restriction_vector = np.zeros(len(load_vector)) + 1
        for i in restrition_vector_origin:
            restriction_vector[int(i)] = 0
        return restriction_vector

class Bridge:

    def __init__(self, entry, elements, restriction_vector, loading_vector):
        self.restriction_vector = restriction_vector
        self.loading_vector = loading_vector
        self.list_elements = elements
        self.reader = Reader(entry)

    def generate_matrix_g(self):
        matrix_g = np.zeros([self.reader.n_nodes*2, self.reader.n_nodes*2])
        for element in self.list_elements:
            matrix_g[element.dof[0]:element.dof[1] + 1, element.dof[0]:element.dof[1]+1] += element.k[0:2, 0:2]
            matrix_g[element.dof[2]:element.dof[3] + 1, element.dof[0]:element.dof[1]+1] += element.k[0:2, 2:4]
            matrix_g[element.dof[0]:element.dof[1] + 1, element.dof[2]:element.dof[3]+1] += element.k[2:4, 0:2]
            matrix_g[element.dof[2]:element.dof[3] + 1, element.dof[2]:element.dof[3]+1] += element.k[2:4, 2:4]
        self.matrix_g = matrix_g
        self.matrix_g_copy = self.matrix_g
    # Até aqui OK

    def boundary_conditions(self):
        temp_var = []
        for i in range(self.restriction_vector.shape[0]):
            if self.restriction_vector[i] == 0:
                temp_var.append(i)
            
        #Making Restrictions
        self.matrix_g = np.delete(self.matrix_g, obj=temp_var, axis=0)
        self.matrix_g = np.delete(self.matrix_g, obj=temp_var, axis=1)
        self.loading_vector = np.delete(self.loading_vector, obj=temp_var, axis=0)

    def equation_solver_and_update(self):

        restriction_matrix = np.zeros((len(self.restriction_vector),1))

        temp = 0
        final_restriction_vector = np.linalg.pinv(self.matrix_g).dot(self.loading_vector)

        for i in range(len(restriction_matrix)):
            if self.restriction_vector[i] == 0:
                restriction_matrix[i] = 0
            else:
                restriction_matrix[i] = final_restriction_vector[temp]
                temp = temp + 1
        
        self.restriction_vector = restriction_matrix

    def support_reaction(self):
        self.reader.loading_vector = np.matmul(self.matrix_g_copy, self.restriction_vector)

        self.reactions = np.zeros((self.reader.n_restrictions,1))
        for e in range(self.reader.n_restrictions):
            self.reactions[e] = self.reader.loading_vector[int(self.reader.restrictions_vector[e])] 
    
        return self.reactions

    def system_distortion(self):
        temp_distortion = []
        for element in self.list_elements:
            temp_matrix = np.array([-element.c, -element.s, element.c, element.s])
            temp_global_restriction = []
            i = 0
            while i < len(element.dof):
                temp_global_restriction.append(self.restriction_vector[element.dof[i]])
                i += 1
            temp_global_restriction = np.array(temp_global_restriction)
            temp_distortion.append(np.matmul(temp_matrix, temp_global_restriction)/element.l)

        return np.array(temp_distortion)

    def system_strain(self):
        temp_strain = []
        for element in self.list_elements:
            temp_matrix = [-element.c, -element.s, element.c, element.s]
            temp_global_restriction = []
            i = 0
            while i < len(element.dof):
                temp_global_restriction.append(self.restriction_vector[element.dof[i]])
                i += 1
            temp_global_restriction = temp_global_restriction
            temp_strain.append(element.e*np.matmul(temp_matrix, temp_global_restriction)/element.l)
        return np.array(temp_strain)

    def internal_forces(self,strain):
        intern_forces = np.zeros([len(self.list_elements), 1])

        for element in range(len(self.list_elements)):
            intern_forces[element] = self.list_elements[element].a * system_strain[element]

        return intern_forces

    def checkLimits(self,strain,desloc,deform):
        """
            Checa se a estrutura está dentro das limitações.
        """

        for element in self.list_elements:
            if (element.l > 0.11):
                print(f"Um elemento tem comprimento maior que 110mm")
                return 1

        for i in range(len(strain)):
            if (abs(strain[i]) > 18.3E6):
                print(f"Tensao no elemento {i} acima do limite: {strain[i]}")
                return 1

        for i in range(len(deform)):
            if (abs(deform[i]) > 0.05):
                print(f"Deformacao no elemento {i} acima do limite: {deform[i]}")
                return 1

        for i in range(len(desloc)):
            if (abs(desloc[i]) > 0.02):
                print(f"Deslocamento no elemento {i} acima do limite: {desloc[i]}")
                return 1
        return 0

app = App("ponte_final_grupo5.xlsx")
N, Inc = app.plotStuff()
xl.plota_ponte(N,Inc)
app.generate_list_segments()
app.generate_list_coordinates()
app.crete_elements()
app.generate_matrixes_k()

restriction_vector_origin = app.generate_restriction_vector_origin()
loading_vector = app.generate_load_vector()
restriction_vector = app.generate_restriction_vector(loading_vector,restriction_vector_origin)

bridge = Bridge("ponte_final_grupo5.xlsx", app.list_elements, restriction_vector, loading_vector)

bridge.generate_matrix_g()
bridge.boundary_conditions()
bridge.equation_solver_and_update()

system_strain = bridge.system_strain()

print(system_strain)

system_distortion = bridge.system_distortion()

internal_forces = bridge.internal_forces(system_strain)

support_reaction = bridge.support_reaction()

checkLimits = bridge.checkLimits(system_strain,bridge.restriction_vector,system_distortion)

if checkLimits==1:
    print("Deu ruim")

xl.geraSaida("output", support_reaction, bridge.restriction_vector,system_distortion,internal_forces,system_strain)
