import csv
import os
import time
import random
from os import system

folder = 'D:\\Things\\'    #   DIRECCION DEL FOLDER "\\low-dimensional"
datos = []

system("cls")   #   LIMPIA LA TERMINAL

#LEE LAS INSTANCIAS DEL ARCHIVO
def asignar_Instancias(filename):
   print('____________________________________________________'+filename+' ____________________________________________________')
   nodo = []
   peso = []
   beneficio = []
   capacidad = []
   n = 0
   with open(folder+ 'low-dimensional\\' + filename, 'rt') as f:
      reader = csv.reader(f)
      peso.append("0")
      beneficio.append("0")
      nodo.append(n)
      for row in reader:
         if(len(row)>0):
            if(row[0] != ''):
               n += 1
               nodo.append(n)
               peso.append(row[0])
               beneficio.append(row[1])
               if(row[2] != ''):
                capacidad.append(row[2])
   return(list([nodo, peso, beneficio, capacidad]))


def beneficio_peso(datos):
    indice= []

    for nodos in range(1, len(datos[0]), 1):
        x = float(datos[2][nodos]) / float(datos[1][nodos])
        indice.append(x)
        
    return indice

#SE REALIZA EL ALGORITMO
def algoritmo(indice, datos):
    
    capacidad_Maxima = float(datos[3][0])   #   CAPACIDAD MAXIMA DEL PROBLEMA
    nodos_Factibles = []                    #   NODOS QUE YA SE VISITARON Y SON FACTIBLES
    nodos = datos[0]                        #   NODOS QUE AUN NO SE VISITAN
    nodo_Aceptado = 0                       #   NODO ACEPTADO EN LA ITERACION
    iteraciones = len(datos[0])             #   NO. DE ITERACIONES POSIBLES DE HACER
    capacidad_Actual = 0                    #   OBTENER LA CAPACIDAD QUE TENEMOS DURANTE LA EJECUCION
    beneficio = 0                           #   BENEFICIO AL MOMENTO
    x = 0
    nodos_Fac = []
    for i in range(0,iteraciones):
        nodos_Fac.append(0); 
        i+=i

    #VERIFICA SI YA PASO DE LA CAPACIDAD
    if(capacidad_Maxima <= capacidad_Actual):

        #TERMINA EL ALGORITMO
        return (list([capacidad_Actual, beneficio, nodos_Factibles]))

    #PREPROCESAMIENTO
    for iteracion in range (0, len(indice),1): 
        #MENOR VALOR DE INDICE DE SENCIBILIDAD PARA Xo
        if(indice[nodos[iteracion]] > indice[nodo_Aceptado]):
            nodo_Aceptado = nodos[iteracion]   
            x = iteracion
    
    nodos_Fac[x] = 1

    #FASE CONSTRUCTIVA
    for _ in range(0, iteraciones, 1):
        min = 1000
        max = 0
        alfa = 0.5
        aux = []
        candidatos = []

        #VERIFICA SI SE PUEDE MOVER AL NODO
        for i in range (1, len(nodos_Fac),1):  
            if(nodos_Fac[i - 1] == 0):
                ayuda = float(datos[2][i]) / float(datos[1][i])
                aux.append(ayuda)
                if(min > ayuda):
                    min = ayuda
                if(max < ayuda):
                    max = ayuda
            else: 
                aux.append(-1)
        
        for i in range (1, len(nodos_Fac),1):  
            if(aux[i - 1] > 0 and aux[i - 1] >= (float(max) - alfa*(float(max) - float(min)))):
                candidatos.append((i - 1))
        
        if(len(candidatos)):
            nodo_Aceptado = random.choice(candidatos)

            if((capacidad_Actual + float(datos[2][nodo_Aceptado]) <= capacidad_Maxima)):
                nodos_Fac[nodo_Aceptado] = 1

                nodos_Factibles.append(nodo_Aceptado)
                nodos.remove(nodo_Aceptado)

                beneficio += float(datos[1][nodo_Aceptado])
                capacidad_Actual += float(datos[2][nodo_Aceptado])

                nodo_Aceptado = 0
            else:
                for i in range (1, len(nodos_Fac),1):  
                  if(nodos_Fac[i - 1] == 0 and (capacidad_Actual + float(datos[2][nodo_Aceptado]) <= capacidad_Maxima)):
                    nodos_Fac[i] = 1

                    nodos_Factibles.append(i)
                    nodos.remove(i)

                    beneficio += float(datos[1][i])
                    capacidad_Actual += float(datos[2][i])

                    nodo_Aceptado = 0
                    return (list([capacidad_Actual, beneficio, nodos_Factibles, nodos_Fac]))
                  
                
    return (list([capacidad_Actual, beneficio, nodos_Factibles, nodos_Fac]))    


start_time = time.time()
#REALIZA n ITERACIONES
for iteraciones in range(0,1,1):
    
    for filename in os.listdir(folder + 'low-dimensional\\'):
        if filename.endswith("P0.csv"):
            nombre = filename.split('_')
            datos = asignar_Instancias(filename)    #  PASAMOS LAS INSTANCIAS A UNA VARIABLE
            
            resultado = algoritmo(beneficio_peso(datos), datos)
            #SE IMPRIME LOS RESULTADOS
            #psrint("-------------------------------------------------------------------------")
            print("Capacidad: " + str("{:.4f}".format(resultado[0])) + "      Beneficio: " + str("{:.4f}".format(resultado[1])) + "       Nodos: "
                  + str(resultado[3]))
            
            datos = []
runtime = time.time() - start_time
print("Runtime: " + str("{:.15f}".format(runtime)) + "\n")