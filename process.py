from xlsx import importa
import numpy as np
nn,N,nm,Inc,nc,F,nr,R = importa('entrada.xlsx')

def read_inc():
    nn,N,nm,Inc,nc,F,nr,R = importa('entrada.xlsx')
    # matrix_inc_1 = Inc[:,0]
    # matrix_inc_2 = Inc[:,1]
    # matrix_inc = np.matrix([matrix_inc_1, matrix_inc_2])
    # return matrix_inc
    return Inc

def calculate_sin(co, hip):
    sin = co/hip
    return sin

def calculate_cos(ca, hip):
    cos = ca/hip
    return cos

matrix_inc = read_inc()

for i 

print(len(matrix_inc))



matrix_kg = np.zeros([len(matrix_inc)*2,len(matrix_inc)*2])

print(matrix_kg)

for i in range(0, len(matrix_inc)):

