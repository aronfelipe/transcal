import xlsx as xl

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

    def calculate_knot(self):
        print(self.e)
        print(self.a)
        print(self.l)
        self.k = ((self.e[0]*self.a[0])/self.l) * self.generate_matrix()
        return self.k

class Bridge:

    def __init__(self, elements,n_nodes, loading_vector,restriction_vector):
        self.elements = elements
        self.n_nodes = n_nodes
        self.restriction_vector = restriction_vector
        self.loading_vector = loading_vector
        self.matrix_g = np.zeros([n_nodes*2, n_nodes*2])

    def generate_knots(self):
        for element in self.elements:
            element.calculate_knot()

    def generate_matrix_g(self):
        matrix_g = np.zeros([self.n_nodes*2, self.n_nodes*2])
        for element in self.elements:
            matrix_g[element.dof[0]:element.dof[1] + 1, element.dof[0]:element.dof[1]+1] +=element.k[0:2, 0:2]
            matrix_g[element.dof[2]:element.dof[3] + 1, element.dof[0]:element.dof[1]+1] +=element.k[0:2, 2:4]
            matrix_g[element.dof[0]:element.dof[1] + 1, element.dof[2]:element.dof[3]+1] +=element.k[2:4, 0:2]
            matrix_g[element.dof[2]:element.dof[3] + 1, element.dof[2]:element.dof[3]+1] +=element.k[2:4, 2:4]
        self.matrix_g = matrix_g
    
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
        print(self.matrix_g)
        print(self.loading_vector)
        final_restriction_vector = np.linalg.lstsq(self.matrix_g, self.loading_vector)
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
            temp_distortion.append(np.matmul(temp_matrix, temp_global_restriction)/elements.l)

        return temp_distortion

    def system_strain(self):
        temp_strain = []
        for elements in self.elements:
            temp_matrix = np.array([-elements.c, -elements.s, elements.c, elements.s])
            temp_global_restriction = []
            i = 0
            while i < len(elements.dof):
                temp_global_restriction.append(self.restriction_vector[elements.dof[i]])
                i += 1
            temp_global_restriction = np.array(temp_global_restriction)
            temp_strain.append(elements.e*np.matmul(temp_matrix, temp_global_restriction)/elements.l)
        return temp_strain

    def internal_forces(self,strain):
        temp_area = []
        for element in self.elements:
            temp_area.append(element.a)
        return np.array(strain)* np.array(temp_area)



class App:

    def __init__(self, nn, N, nm, Inc, nc, F, nr, R):
        self.knot_quant = nn
        self.knot_matrix = N
        self.elements_quant = nm
        self.Inc = Inc
        self.load_quant = nc
        self.load_vector = F
        self.restrictions_quant = nr
        self.restrictions_vector = R

    def generate_list_nodes(self):
        list_nodes = []
        for i in Inc:
            list_nodes.append(np.array([int(i[0]),int(i[1])]))
            
        return list_nodes

    def generate_list_A(self):
        list_A = []
        for i in Inc:
            list_A.append(np.array([int(i[3])]))
        return list_A

    def generate_list_E(self):
        list_E = []
        for i in Inc:
            list_E.append(np.array([int(i[2])]))
        return list_E

    def generate_list_knots(self):
        list_knots = []
        for i in Inc:
            list_knots.append(np.array([int(i[0]),int(i[1])]))
        return list_knots

    def generate_restriction_vector_origin(self):
        restrition_vector = []
        for i in range(self.restrictions_vector.shape[0]):
            restrition_vector.append(np.array([(self.restrictions_vector[i][0])]))
        return restrition_vector

    def generate_load_vector(self):
        load_vector = []
        for i in range(self.load_vector.shape[0]):
            load_vector.append(np.array([(self.load_vector[i][0])]))
        return load_vector

    def generate_restriction_vector(self,load_vector,restrition_vector_origin):
        restriction_vector = np.zeros(len(load_vector)) + 1
        for i in restrition_vector_origin:
            restriction_vector[int(i)] = 0
        return restriction_vector


    # vigas = []
    # for i in range(len(list_knots)):
    #     viga = Viga(list_nodes[int(list_knots[i][0]-1)], list_nodes[int(list_knots[i][1]-1)], list_A[i], list_E[i], list_knots[i])
    #     vigas.append(viga)

#Importing Excel
nn, N, nm, Inc, nc, F, nr, R = xl.importa("entrada.xlsx")

#Ploting Graph
xl.plota(N, Inc)

#Starting App
app = App(nn, N, nm, Inc, nc, F, nr, R)

#Constructing Lists and Vectors
list_nodes = app.generate_list_nodes()
list_A = app.generate_list_A()
print(list_A)
list_E = app.generate_list_E()
list_knots = app.generate_list_knots()
restriction_vector_origin = app.generate_restriction_vector_origin()
load_vector = app.generate_load_vector()
restriction_vector = app.generate_restriction_vector(load_vector,restriction_vector_origin)

#Constructing Elements
elements = []
for i in range(len(list_knots)):
    element = Element(list_nodes[int(list_knots[i][0]-1)][0],list_nodes[int(list_knots[i][0]-1)][1], list_nodes[int(list_knots[i][1]-1)][0],list_nodes[int(list_knots[i][1]-1)][1], list_A[i], list_E[i], list_knots[i])
    elements.append(element)

#Cronstructing Bridge
bridge = Bridge(elements, nn, load_vector, restriction_vector)

bridge.generate_knots()
bridge.generate_matrix_g()
bridge.boundary_conditions()
bridge.equation_solver_and_update()
support_reaction = bridge.support_reaction()
system_distortion = bridge.system_distortion()
system_strain = bridge.system_strain()
internal_forces = bridge.internal_forces(system_strain)

#Final Graph Ploting
# xl.plota(N,Inc)

xl.geraSaida("output",support_reaction,bridge.restriction_vector,system_distortion,internal_forces,system_strain)


# print(app.generate_list_nodes())
# print(app.numerate_dof())

# elements_list = []

# for element in app.numerate_dof():
#     print(element)

