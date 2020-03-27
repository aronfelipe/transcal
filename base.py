import numpy as np
import math

from xlsx import importa

E = 210*(10**9)

A = 2*10**(-4)

l1 = 0.4
l2 = 0.3
l3 = 0.5

class Beam:
    

def numerar_gdl(n_nos):
    lista_gdl = []
    for i in range (1, n_nos+1):
        if len(lista_gdl) < 1:
            lista_gdl.append([i,1, 2])
        else:
            lista_gdl.append([i,lista_gdl[-1][2] + 1, lista_gdl[-1][2] + 2])

    return lista_gdl

def ler_inc():
    [nn, N, nm, Inc, nc, F, nr, R] = importa("entrada.xlsx")
    return Inc

def ler_nos():
    [nn, N, nm, Inc, nc, F, nr, R] = importa("entrada.xlsx")
    return N

def gerar_matrix_ke(s, c):
    matrix_ke = np.matrix([[c**2, c*s, -c*2, -c*s], [c*s, s**2, -c*s, -s**2], [-c**2, -c*s, c**2, c*s], [-c*s, -s**2, c*s, s**2]])
    return matrix_ke

def calcular_l(ponto1, ponto2):
    l = math.sqrt((ponto2[0] - ponto1[0])**2 + (ponto2[1] - ponto2[1])**2)
    return l

def calcular_ke(matrix, l, E, A):
    ke = (((E*A)/l) * matrix)
    return ke

def gerar_matrix_kg(matrix_k1, matrix_k2, matrix_k3):

    dictionary_k1 = {}
    dictionary_k2 = {}
    dictionary_k3 = {}

    for idx, val in enumerate(matrix_k1):
        for i in range(0,4):
            key = str(idx+1) + " " + str(i+1)
            dictionary_k1[key] = val.item(i)
        
    for idx, val in enumerate(matrix_k2):
        for i in range(0,4):
            key = str(idx+1+2) + " " + str(i+1+2)
            dictionary_k2[key] = val.item(i)
    
    for idx, val in enumerate(matrix_k3):
        for i in range(0,4):
            if idx + 1 + 4 == 7 and i + 1 + 4 == 7:
                key = str(1) + " " + str(1)
            elif (idx + 1 + 4 == 7) and (i + 1 + 4 == 8):
                key = str(1) + " " +  str(2)
            elif idx + 1 + 4 == 8 and i + 1 + 4 == 7:
                key = str(2) + " " + str(1)
            elif idx + 1 + 4 == 8 and i + 1 + 4 == 8:
                key = str(2) + " " + str(2)
            elif idx + 1 + 4 == 7:
                key = str(1) + " " + str(i+1+4)
            elif i + 1 + 4 == 7:
                key = str(idx+1+4) + " " +  str(1)
            elif idx + 1 + 4 == 8:
                key = str(2) + " " + str(i+1+4)
            elif i + 1 + 4 == 8:
                key = str(idx+1+4) + " " + str(2)
            else:
                key = str(idx+1+4) + " " + str(i+1+4)
            
            dictionary_k3[key] = val.item(i)

    matrix_kg = np.zeros([6,6])   

    for i in dictionary_k1:
        split = i.split()        
        matrix_kg[int(split[0]) - 1, int(split[1]) - 1 ] = dictionary_k1[i]

    for i in dictionary_k2:
        split = i.split()
        matrix_kg[int(split[0]) - 1, int(split[1]) - 1 ] = dictionary_k2[i]

    for i in dictionary_k3:
        split = i.split()
        matrix_kg[int(split[0]) - 1, int(split[1]) - 1 ] = dictionary_k3[i]

    return matrix_kg

# node_one_sin = 1
# node_one_cos = 0

# hip = 0.5

# node_2_sin = calculate_sin(0.3, 0.5)

# matrix_ke1 = gerar_matrix_ke(1, 0)

# ke1 = calcular_ke(matrix_ke1, l1, E, A)

# matrix_ke2 = gerar_matrix_ke(0, 1)

# ke2 = calcular_ke(matrix_ke2, l2, E, A)

# matrix_ke3 = gerar_matrix_ke(-0.8, -0.6)

# ke3 = calcular_ke(matrix_ke3, l3, E, A)

# matrix_kg = gerar_matrix_kg(ke1, ke2, ke3)

# print(matrix_kg)

matrix_nos = ler_nos()

lista_gdl = numerar_gdl(len(matrix_nos[0,:]))

print(lista_gdl)

# matrix_kg = np.zeros([len(matrix_inc)*2,len(matrix_inc)*2])

# print(matrix_kg)

# for i in range(0, len(matrix_inc)):
    
