# !/usr/bin/env python
# -*- coding: utf-8 -*-
# App Main


import sys
from Node import Node
from AStarAlgorithm import AStarAlgorithm
from math import radians, cos, sin, asin, sqrt
import csv
    
def distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))    
    r = 6371
      
    return(c * r)

class App(object):

    def __init__(self):
        print("Creando nodos: ", end = '')
        """
        self.i = Node("I", 7)
        self.a = Node("A", 6)
        self.b = Node("B", 2)
        self.c = Node("C", 1)
        self.f = Node("F", 0)
        self.i.addChild(self.a, 1)
        self.i.addChild(self.b, 4)
        print("I ", end ='')
        self.a.addChild(self.b, 2)
        self.a.addChild(self.c, 5)
        self.a.addChild(self.f, 12)
        print("A ", end ='')
        self.b.addChild(self.c, 2)
        print("B ", end ='')
        self.c.addChild(self.f, 3)
        print("C ", end ='')
        print("F ", end ='')
        """
        # coyoacan -> lazaro cardenas
        # lazaro cardenas: 19.40696, -99.144874
        #origen-destino
        #self.coyoacan = Node("Coyoacan", distance(19.361417, -99.170709, 19.40696, -99.144874))
        #self.lazaro = Node("LazaroCardenas", 0)
        LClat = 19.40696
        LClot = -99.144874
        i = 0
        with open("./LineasMetro.csv", 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:                
                _, _, n, lat, lon, _ = row
                if n != "nombre":
                    st = ''.join(n.split()).lower()
                    print(st)
                    setattr(self, st, Node(st, distance(float(lat), float(lon), LClat, LClot)))
                    
        with open("./metro.csv", 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                _, u, v, l = row
                if u != "origen":
                    origen = ''.join(u.split()).lower()
                    destino = ''.join(v.split()).lower()                    
                    #self.childNodes.append(getattr(self, destino))
                    #self.childNodes.append(getattr(self, destino))
                    #getattr(self, origen).childNodes.append(getattr(self, destino))
                    getattr(self, origen).childNodes.append(getattr(self, destino))
                    setattr(self, origen+'.childNodesRealCost[self.'+destino+".name]", float(l))
                    #self.coyoacan.addChild(self.zapata, 100)
                    getattr(self, destino).childNodes.append(getattr(self, origen))
                    setattr(self, destino+'.childNodesRealCost[self.'+origen+".name]", float(l))
        
    def searchAStarAlgorithm(self):
        print("\nBuscando ruta optima con Algoritmo A*")
        astar = AStarAlgorithm(getattr(self, "coyoacan"), getattr(self,"lazarocardenas"))
        print("Nodo Inicial: %s -----> Nodo Final %s" % (self.coyoacan.name, self.lazarocardenas.name))
        astar.run()


if __name__ == "__main__":
    try:
        app = App()
        #print(app.Oceania.name)
        app.searchAStarAlgorithm()
    except (ValueError, FileNotFoundError, AttributeError) as ex:
        print(ex)
