from read import EntryReader

import numpy as np

class Element:

    def __init__(self,x_cord_1, y_cord_1, x_cord_2, y_cord_2, A, E, nodes):
        self.x = x_cord_2 - x_cord_1
        self.y = y_cord_2 - y_cord_1

        self.l = np.sqrt(self.x**2+self.y**2)
        self.a = A
        self.e = E

        self.s = self.y/self.l
        self.c = self.x/self.l

        self.dof     = [nodes[0]*2-2, nodes[0]*2-1,nodes[1]*2-2,nodes[1]*2-1]

    def generate_matrix(self):
        matrix_ke = np.matrix([[self.c**2, self.c*self.s, -self.c*2, -self.c*self.s],
                               [self.c*self.s, self.s**2, -self.c*self.s, -self.s**2], 
                               [-self.c**2, -self.c*self.s, self.c**2, self.c*self.s],
                               [-self.c*self.s, -self.s**2, self.c*self.s, self.s**2]])
        return matrix_ke

    def calculate_k(self):
        self.k = (((self.e*self.a)/self.l) * self.generate_matrix())
        return self.k

class Bridge:

    def __init__(self, elements, loading_vector,n_nodes,restriction_vector,u):
        self.elements = elements
        self.u = u
        self.n_nodes = n_nodes
        self.restriction_vector = restriction_vector
        self.loading_vector = loading_vector
        self.matrix_g = np.zeros([n_nodes*2, n_nodes*2])

    def generate_matrix_g(self):

        # Consctructing the global matrix for the bridge 
        # taking into account the degrees of freedom of each of the elements
        # and grouping each matrix of the elements into matrixes of 2x2 elements

        for element in self.elements:
            self.matrix_g[element.dof[0]:element.dof[1] + 1, element.dof[0]:element.dof[0]+1] +=element.k[0:2, 0:2]
            self.matrix_g[element.dof[2]:element.dof[3] + 1, element.dof[2]:element.dof[3]+1] +=element.k[2:4, 2:4]
            self.matrix_g[element.dof[0]:element.dof[1] + 1, element.dof[2]:element.dof[3]+1] +=element.k[0:2, 2:4]
            self.matrix_g[element.dof[2]:element.dof[3] + 1, element.dof[0]:element.dof[0]+1] +=element.k[2:4, 0:2]
    
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
        tempList = []
        tempVar = 0
        final_restriction_vector = np.linalg.solve(self.matrix_g, self.loading_vector)
        for i in self.restriction_vector:
            if i == 0:
                tempList.append(0)
            else:
                tempList.append(final_restriction_vector[tempVar])
                tempVar = tempVar + 1
        self.restriction_vector = tempList

    def support_reaction(self):
        self.generate_matrix_g()
        return np.matmul(self.matrix_g, self.restriction_vector)

    def system_distortion(self):
        temp_distortion = []
        for elements in self.elements:
            temp_matrix = np.array([-elements.c, -elements.s, elements.c, elements.s])
            temp_global_restriction = []
            i = 0
            while i < len(elements.dof):
                temp_global_restriction.append(self.restriction_vector[elements.dof[i]])
                i += 1
            temp_global_restriction = np.array(temp_global_restriction)
            temp_distortion.append(np.matmul(temp_matrix, temp_global_restriction)/elements.L)

        return temp_distortion

    def system_strain_and_internal_forces(self):
        temp_strain = []
        temp_area = []
        for elements in self.elements:
            temp_matrix = np.array([-elements.c, -elements.s, elements.c, elements.s])
            temp_global_restriction = []
            i = 0
            while i < len(elements.dof):
                temp_global_restriction.append(self.restriction_vector[elements.dof[i]])
                i += 1
            temp_global_restriction = np.array(temp_global_restriction)
            temp_strain.append(elements.e*np.matmul(temp_matrix, temp_global_restriction)/elements.L)
        for elements in self.elements:
            temp_area.append(elements.a)
        return temp_strain, np.array(temp_strain)* np.array(temp_area)



class App:

    def __init__(self, entry):
        self.reader = EntryReader(entry)

    def generate_list_nodes(self):
        list_nodes = []
        for i in self.reader.incidence_matrix:
            list_nodes.append(np.array([int(i[0]),int(i[1])]))
            
        return list_nodes
        
    def numerate_dof(self):
        list_dof = []
        for i in range (1, self.reader.n_nodes+1):
            if len(list_dof) < 1:
                list_dof.append([i,1, 2])
            else:
                list_dof.append([i,list_dof[-1][2] + 1, list_dof[-1][2] + 2])

        return list_dof


app = App("entrada.xlsx")
print(app.generate_list_nodes())
print(app.numerate_dof())

elements_list = []

for element in app.numerate_dof():
    print(element)

