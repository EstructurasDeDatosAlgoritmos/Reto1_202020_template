"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt

from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")




def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1



def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("theMoviesdb/movies-small.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def loadDetails ():
    lst = loadCSVFile("themoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def ranking_genero (lista_Details, genero, No_peliculas, criteria_r, criteria_o):                  #Requerimiento 6
    buscar_genero = lt.newList('SINGLE_LINKED', None)
    #------------------------------------

    t1_start = process_time() #Inicio de cronometro 

    #Filtrar las peliculas por genero

    iter = it.newIterator(lista_Details)
    while it.hasNext(iter):
        c = it.next(iter)
        genero_separado = c["genres"].split("|")
        i = 0
        tam = len(genero_separado)
        while i < tam:
            if (genero_separado[i] == genero):
                lt.addFirst(buscar_genero, c)
            i += 1

    
    #Crear Ranking

    generos_ordenados = lt.newList('SINGLE_LINKED', None)
    PARAMETROS_NO = "Parametro no valido"         #Variable para comprobar que todos los parametros hayan sido procesados
    cont = 0                                      #Variable para contar las peliculas en el ranking
    if (criteria_o == "ascendente"and No_peliculas >= 10):
        mayor = 0
        if (criteria_r == "count"):
            iter2 = it.newIterator(buscar_genero)
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if (cont == No_peliculas):
                    break
                elif(int(d["vote_count"]) >= mayor):
                    lt.insertElement(generos_ordenados,d, mayor + 1)
                    mayor = int(d["vote_count"])
                else:
                    lt.insertElement(generos_ordenados,d, mayor - 1)
                cont += 1
        elif (criteria_r == "average"):
            iter2 = it.newIterator(buscar_genero)
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if (cont == No_peliculas):
                    break
                elif(float(d["vote_average"]) >= mayor):
                    lt.insertElement(generos_ordenados,d, mayor + 1)
                    mayor = float(d["vote_average"])
                else:
                    lt.insertElement(generos_ordenados,d, mayor - 1)
        else:
            return PARAMETROS_NO

    elif (criteria_o == "descendente"and No_peliculas >= 10):
        menor = 0
        if (criteria_r == "count"):
            iter2 = it.newIterator(buscar_genero)
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if (cont == No_peliculas):
                    break
                elif(int(d["vote_count"]) <= menor):
                    lt.insertElement(generos_ordenados,d, menor + 1)
                    menor = int(d["vote_count"])
                else:
                    lt.insertElement(generos_ordenados,d, menor - 1)
        elif (criteria_r == "average"):
            iter2 = it.newIterator(buscar_genero)
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if (cont == No_peliculas):
                    break
                elif(float(d["vote_average"]) <= menor):
                    lt.insertElement(generos_ordenados,d, menor + 1)
                    menor = float(d["vote_average"])
                else:
                    lt.insertElement(generos_ordenados,d, menor - 1)
        else:
            return PARAMETROS_NO
    else:
        return PARAMETROS_NO
    
    Peliculas_en_ranking = lt.size(generos_ordenados)
    Votos_totales = 0
    Votos_Promedio = 0.0
  
    #Imprimir ranking
 
    print("Película       ,  Genero  , Vote_Average , Vote_Count")
    iterfinal = it.newIterator(generos_ordenados)
    while it.hasNext(iterfinal):

        f = it.next(iterfinal)

        Votos_totales = Votos_totales + int(f["vote_count"])
        Votos_Promedio = Votos_Promedio + float(f["vote_average"])
        Pel = str(f["original_title"])
        Gen = str(f["genres"])
        Av = str(f["vote_average"])
        Co = str(f["vote_count"])

        print(Pel +" "+ Gen +" "+ Av +" "+ Co)

    Promedio = Votos_Promedio/Peliculas_en_ranking

    print("Promedio(Vote average): " + Promedio)
    print("Votos totales: " + Votos_totales)

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()
                lstDetails = loadDetails()

            elif int(inputs[0])==2: #opcion 2
                pass

            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                pass

            elif int(inputs[0])==5: #opcion 5
                pass

            elif int(inputs[0])==6: #opcion 6
                genero = input("Ingrese el nombre del genero:\n")
                No_peliculas = input("Ingrese el número de películas (Mínimo 10):\n")#------------------------------------
                criteria_r = input("Ingrese el criterio del ranking (count o average)::\n")#------------------------------------
                criteria_o = input("Ingrese el criterio de ordenamiento (ascendente o descendente):\n")#------------------------------------
    
                Crear_ranking = ranking_genero(lstDetails, genero, No_peliculas, criteria_r, criteria_o)


            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
             
if __name__ == "__main__":
    main()