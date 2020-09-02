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
    lst = loadCSVFile("theMoviesdb/MoviesCastingRaw-small.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def loadDetails():
    lst=loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds)
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def comparacion_m1 (element1, element2):
    return element1[1]["promedio"] > element2[1]["promedio"]

def comparacion_me1 (element1, element2):
    return element1[1]["promedio"] < element2[1]["promedio"]

def comparacion_m_v1 (element1, element2):
    return element1[1]["votos"] < element2[1]["votos"]

def comparacion_me_v2 (element1, element2):
    return element1[1]["votos"] > element2[1]["votos"]

def ranking_peliculas (num_peli, v_p, as_des, lstD):                          #Requerimiento 2
    ranking = lt.newList('SINGLE_LINKED', None)
    t1_start = process_time()
    if (lstD["size"])==0:
        print("La lista esta vacía")  
        return 0
    num_peli = int()
    pelis = []
    conta = 0
    while num_peli >= 10:
        nombre = ""
        if v_p.lower() == "promedio" and as_des.lower() == "ascendente":
            for i in range(1, lt.size(lstD)):
                element = lt.getElement(lstD, i)
                if float(element["vote_average"]) > 0 and element["title"] not in pelis:
                    x = float(element["vote_average"])
                    nombre = element["title"]
            lt.addFirst(ranking,[nombre,x])
            pelis.append(nombre)
            conta = conta + 1
        
        if v_p.lower() == "promedio" and as_des.lower() == "descendente":
            for i in range(1, lt.size(lstD)):
                element = lt.getElement(lstD, i)
                if float(element["vote_average"]) < 10  and element["title"] not in pelis:
                    y = float(element["vote_average"])
                    nombre = element["title"]
            lt.addFirst(ranking,[nombre,y])
            pelis.append(nombre)
            conta = conta + 1
        
        if v_p.lower() == "votos" and as_des.lower() == "ascendente":
            for i in range(1, lt.size(lstD)):
                element = lt.getElement(lstD, i)
                if float(element["vote_count"]) > 0 and element["title"] not in pelis:
                    x = float(element["vote_count"])
                    nombre = element["title"]
            lt.addFirst(ranking,[nombre,x])
            pelis.append(nombre)
            conta = conta + 1
        
        if v_p.lower() == "votos" and as_des.lower() == "descendente":
            for i in range(1, lt.size(lstD)):
                element = lt.getElement(lstD, i)
                if float(element["vote_count"]) < 13000  and element["title"] not in pelis:
                    y = float(element["vote_count"])
                    nombre = element["title"]
            lt.addFirst(ranking,[nombre,y])
            pelis.append(nombre)
            conta = conta + 1
    
    if v_p.lower() == "promedio" and v_p.lower() == "ascendente":
        lt.insertion(ranking, comparacion_m1)
    if v_p.lower() == "promedio" and v_p.lower() == "descendente":
        lt.insertion(ranking, comparacion_me1)
    if v_p.lower() == "votos" and v_p.lower() == "ascendente":
        lt.insertion(ranking, comparacion_m_v1)
    if v_p.lower() == "votos" and v_p.lower() == "descendente":
        lt.insertion(ranking, comparacion_me_v2)
    
    t1_stop = process_time()
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

    return (ranking)

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

def conocer_director(criteria, column, lstC,lstD): #Requerimiento 3
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

def peliculas_por_actor1(criteria, column, lst):
    peliculas_actor = lt.newList("ARRAY_LIST",None)
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        iterador=it.newIterator(lst)
        while it.hasNext(iterador):
            element = it.next(iterador)
            if criteria.lower() in element[column].lower():
                lt.addLast(peliculas_actor,element["id"])
    return peliculas_actor

def peliculas_por_actor2(criteria, column, lst):
    peliculas_actor2 = lt.newList("ARRAY_LIST",None)
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        iterador=it.newIterator(lst)
        while it.hasNext(iterador):
            element = it.next(iterador)
            if criteria.lower() in element[column].lower():
                lt.addLast(peliculas_actor2,element["id"])
    return peliculas_actor2

def peliculas_por_actor3(criteria, column, lst):
    peliculas_actor3 = lt.newList("ARRAY_LIST",None)
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        iterador=it.newIterator(lst)
        while it.hasNext(iterador):
            element = it.next(iterador)
            if criteria.lower() in element[column].lower():
                lt.addLast(peliculas_actor3,element["id"])
    return peliculas_actor3

def peliculas_por_actor4(criteria, column, lst):
    peliculas_actor4 = lt.newList("ARRAY_LIST",None)
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        iterador=it.newIterator(lst)
        while it.hasNext(iterador):
            element = it.next(iterador)
            if criteria.lower() in element[column].lower():
                lt.addLast(peliculas_actor4,element["id"])
    return peliculas_actor4

def peliculas_por_actor5(criteria, column, lst):
    peliculas_actor5 = lt.newList("ARRAY_LIST",None)
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        iterador=it.newIterator(lst)
        while it.hasNext(iterador):
            element = it.next(iterador)
            if criteria.lower() in element[column].lower():
                lt.addLast(peliculas_actor5,element["id"])
    return peliculas_actor5

def conocer_actor(criteria, lstC, lstD): #Requerimiento 4
    t1_start = process_time()
    suma = 0
    peli_actor = lt.newList("ARRAY_LIST", None)
    peliculas_actor = peliculas_por_actor1(criteria, "actor1_name", lstC)
    peliculas_actor2 = peliculas_por_actor2(criteria, "actor2_name", lstC)
    peliculas_actor3 = peliculas_por_actor3(criteria, "actor3_name", lstC)
    peliculas_actor4 = peliculas_por_actor4(criteria, "actor4_name", lstC)
    peliculas_actor5 = peliculas_por_actor5(criteria, "actor5_name", lstC)

    if (lstD["size"]) == 0:
        print("La Lista esta vacía")
        return 0
    
    else:
        iterador = it.newIterator(lstD)
        while it.hasNext(iterador):
            element = it.next(iterador)
            if element["id"] in peliculas_actor["elements"]:
                suma = suma + float(element["vote_average"])
                lt.addFirst(peli_actor, element["original_title"])
            elif element["id"] in peliculas_actor2["elements"]:
                suma = suma + float(element["vote_average"])
                lt.addFirst(peli_actor, element["original_title"])
            elif element["id"] in peliculas_actor3["elements"]:
                suma = suma + float(element["vote_average"])
                lt.addFirst(peli_actor, element["original_title"])
            elif element["id"] in peliculas_actor4["elements"]:
                suma = suma + float(element["vote_average"])
                lt.addFirst(peli_actor, element["original_title"])
            elif element["id"] in peliculas_actor5["elements"]:
                suma = suma + float(element["vote_average"])
                lt.addFirst(peli_actor, element["original_title"])

        prom = round((suma/peli_actor["size"]),3)
        t1_stop = process_time()
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        return (peli_actor, prom)

def entender_genero(criteria,column,lstD): #Requerimiento 5
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
    cont = 0                                      #Variable para contar las peliculas
    mayor = lt.firstElement(buscar_genero)
    menor = lt.lastElement(buscar_genero)
    if lt.isEmpty(buscar_genero):
        print("No se encontraron peliculas de ese genero")
    elif (criteria_o == "ascendente"and No_peliculas >= 10):
        
        
        if (criteria_r == "count"):
            ma = mayor["vote_count"]
            me = menor["vote_count"]
            print(ma)
            iter2 = it.newIterator(buscar_genero)
            
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if(int(d["vote_count"]) >= int(ma)):
                    lt.addFirst(generos_ordenados,d)
                    ma = int(d["vote_count"])
                if(int(d["vote_count"]) <= int(me)):
                    lt.addLast(generos_ordenados,d)
                    me = int(d["vote_count"])
                

        elif (criteria_r == "average"):
            ma = mayor["vote_average"]
            me = menor["vote_average"]
            print(ma)
            iter2 = it.newIterator(buscar_genero)
            
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if(float(d["vote_average"]) >= float(ma)):
                    lt.addFirst(generos_ordenados,d)
                    ma = float(d["vote_average"])
                if(float(d["vote_average"]) <= float(me)):
                    lt.addLast(generos_ordenados,d)
                    me = float(d["vote_average"])
                
                    
        else:
            return PARAMETROS_NO

    elif (criteria_o == "descendente"and No_peliculas >= 10):
        
        if (criteria_r == "count"):
            ma = mayor["vote_count"]
            me = menor["vote_count"]
            print(ma)
            iter2 = it.newIterator(buscar_genero)
            
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if(int(d["vote_count"]) >= int(ma)):
                    lt.addLast(generos_ordenados,d)
                    ma = int(d["vote_count"])
                if(int(d["vote_count"]) <= int(me)):
                    lt.addFirst(generos_ordenados,d)
                    me = int(d["vote_count"])
                
             
        elif (criteria_r == "average"):
            ma = mayor["vote_average"]
            me = menor["vote_average"]
            print(ma)
            iter2 = it.newIterator(buscar_genero)
            
            while it.hasNext(iter2):
                d = it.next(iter2)
                
                if(float(d["vote_average"]) >= float(ma)):
                    lt.addLast(generos_ordenados,d)
                    ma = float(d["vote_average"])
                if(float(d["vote_average"]) <= float(me)):
                    lt.addFirst(generos_ordenados,d)
                    me = float(d["vote_average"])
                
        else:
            return PARAMETROS_NO
    else:
        return PARAMETROS_NO
    
    Peliculas_en_ranking = lt.size(generos_ordenados)
    Votos_totales = 0
    Votos_Promedio = 0.0
  
    #Imprimir ranking
 
    print("Película                       ,            Genero             , Vote_Average , Vote_Count")
    iterfinal = it.newIterator(generos_ordenados)
    while it.hasNext(iterfinal):

        f = it.next(iterfinal)
        if (cont == No_peliculas):
            break
        Votos_totales = Votos_totales + int(f["vote_count"])
        Votos_Promedio = Votos_Promedio + float(f["vote_average"])
        Pel = str(f["original_title"])
        Gen = str(f["genres"])
        Av = str(f["vote_average"])
        Co = str(f["vote_count"])

        print(Pel +" I "+ Gen +" I "+ Av +" I "+ Co)
        cont += 1

    Promedio = Votos_Promedio/Peliculas_en_ranking

    print("Promedio(Vote average): " + str(Promedio))
    print("Votos totales: " + str(Votos_totales))
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lstmovies = {"size":0}
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()
                lstdetails = loadDetails()

            elif int(inputs[0])==2: #opcion 2
                if lstmovies == None or lstmovies['size'] == 0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   #(num_peli, v_p, as_des, elemento1, elemento2, lstD)
                    num_peli = input('Ingrese el número de peliculas, mínimo 10: \n')
                    v_p = input("Ingrese la cantidad por la que se quiere ordenar (promedio o votos): \n")
                    as_des = input("Ingrese el orden en el que se quiere ordenar (ascendente o descendente): \n")

                    x = ranking_peliculas(num_peli, v_p, as_des, lstmovies) #filtrar una columna por criterio  
                    print("El ranking es el siguiente: ",x)

            elif int(inputs[0])==3: #opcion 3
                if lstmovies == None or lstmovies['size'] == 0 and lstdetails == None or lstdetails['size'] == 0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria = input('Ingrese el nombre del director: \n')
                    x = conocer_director(criteria, "director_name" ,lstmovies, lstdetails) #filtrar una columna por criterio  
                    print("Coinciden ",x," elementos con el director: ",criteria)

            elif int(inputs[0])==4: #opcion 4
                if  lstdetails == None or lstdetails['size']==0 and lstmovies==None or lstmovies['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria = input('Ingrese el nombre del actor: \n')
                    x = conocer_actor(criteria,lstmovies, lstdetails) #filtrar una columna por criterio  
                    print("Coinciden ",x," elementos con el actor: ",criteria)
            elif int(inputs[0])==5: #opcion 5
                if lstmovies == None or lstmovies['size'] == 0 and lstdetails == None or lstdetails['size'] == 0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    criteria = input('Ingrese el género: \n')
                    x = entender_genero(criteria, "genres" ,lstdetails) #filtrar una columna por criterio  
                    print("Coinciden ",x," elementos con el género: ",criteria)

            elif int(inputs[0])==6: #opcion 6
                if lstdetails == None or lstdetails['size'] == 0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    genero = input("Ingrese el nombre del genero:\n")
                    No_peliculas = int(input("Ingrese el número de películas (Mínimo 10):\n"))#------------------------------------
                    criteria_r = input("Ingrese el criterio del ranking (count o average)::\n")#------------------------------------
                    criteria_o = input("Ingrese el criterio de ordenamiento (ascendente o descendente):\n")#------------------------------------
                    x = ranking_genero(lstdetails, genero, No_peliculas, criteria_r, criteria_o)
                    print("Gracias")

            elif int(inputs[0])==0: #opcion 0, salir
                print("Vuelva pronto")
                sys.exit(0)
             
if __name__ == "__main__":
    main()