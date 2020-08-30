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

def peliculas_por_director(criteria, column, lst):
    peliculas_director=lt.newList("ARRAY_LIST",None)
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        iterator=it.newIterator(lst)
        while it.hasNext(iterator):
            element=it.next(iterator)
            if criteria.lower() in element[column].lower():
                lt.addLast(peliculas_director,element["id"])
    return peliculas_director


def conocer_director(criteria, column, lstC,lstD):
    t1_start = process_time() #tiempo inicial
    sum_average=0
    lista_director=lt.newList("ARRAY_LIST", None)
    peliculas_director=peliculas_por_director(criteria,"director_name",lstC)
    if (lstD["size"])==0:
        print("La lista esta vacía")  
        return 0
    else:
        iterator2=it.newIterator(lstD)
        while it.hasNext(iterator2):
            element=it.next(iterator2)
            if element["id"] in peliculas_director["elements"]:
                sum_average+=float(element["vote_average"])
                lt.addFirst(lista_director,element["original_title"])
        promedio=round((sum_average/lista_director["size"]),3)
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        return (lista_director,promedio)

def conocer_actor(criteria, column, lstC, lstD):
    t1_start = process_time()
    promedio = 0
    peli_actor = lt.newList("ARRAY_LIST", None)
    


def entender_genero(criteria,column,lstD):
    t1_start=process_time()#tiempo inicial
    sum_count=0
    lista_genero=lt.newList("ARRAY_LIST",None)
    if lstD["size"]==0:
        print("la lista esta vacía")
    else:
        iterator=it.newIterator(lstD)
        while it.hasNext(iterator):
            element=it.next(iterator)
            if criteria.lower() in element[column].lower():
                lt.addLast(lista_genero,element["original_title"])
                sum_count+=float((element["vote_average"]))
        promedio=round((sum_count/lista_genero["size"]),3)
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        return (lista_genero,promedio)


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

            elif int(inputs[0])==2: #opcion 2
                pass

            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                pass

            elif int(inputs[0])==3: #opcion 5
                pass

            elif int(inputs[0])==4: #opcion 6
                pass


            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()