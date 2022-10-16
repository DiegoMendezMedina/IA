#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tarea_1.py
----------------

Codigo que resuelve las preguntas: 
        + 2. Agentes.
        + 3. Busqueda no informada.
        + 4. Busqueda informada.
"""

import entornos_f
import copy
from random import choice # Para agente aleatorio
from collections import defaultdict # Para gráficas


"""
  2. Agentes
"""
class SeisCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de seis cuartos. 

    El estado se define como (robot, A, B, C, D, E, F)
    donde robot puede tener los valores "A", "B", "C", "D",
    "E", "F";
    Cada uno de los cuartos puede tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son 
        ("ir_*", "limpiar", "nada"), donde * son los cuartos 
    validos para cada otro cuarto. Cuartos validos:
     
    A -> B, F // Se lee los cuartos validos para ir partiendo de A son B y F.
    B -> A, C
    C -> B, D
    D -> E, C
    E -> D, F
    F -> E, A

    Consideramos "subir" como ir del cuarto F al A, y del D al C, tienen costo 2.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    """
    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "ir_C", "ir_D", "ir_E", "ir_F",
                          "limpiar", "nada")

    def transición(self, estado, acción):
        robot, a, b, c, d, e, f = estado

        c_local = 0
        if acción != "nada":
            c_local = 1
        if(robot == "A" and acción == "ir_F") or (robot == "C" and acción == "ir_D"):
            c_local = 2
        
        return ((estado, c_local) if acción == "nada" else
                (("A", a, b, c, d, e, f), c_local) if acción == "ir_A" else
                (("B", a, b, c, d, e, f), c_local) if acción == "ir_B" else
                (("C", a, b, c, d, e, f), c_local) if acción == "ir_C" else
                (("D", a, b, c, d, e, f), c_local) if acción == "ir_D" else
                (("E", a, b, c, d, e, f), c_local) if acción == "ir_E" else
                (("F", a, b, c, d, e, f), c_local) if acción == "ir_F" else
                ((robot, "limpio", b, c, d, e, f), c_local) if robot == "A" and acción == "limpiar" else
                ((robot, a, "limpio", c, d, e, f), c_local) if robot == "B" and acción == "limpiar" else
                ((robot, a, b, "limpio", d, e, f), c_local) if robot == "C" and acción == "limpiar" else
                ((robot, a, b, c, "limpio", e, f), c_local) if robot == "D" and acción == "limpiar" else
                ((robot, a, b, c, d, "limpio", f), c_local) if robot == "E" and acción == "limpiar" else
                ((robot, a, b, c, d, e, "limpio"), c_local))

    def percepción(self, estado):
        return estado[0], estado[" ABCDEF".find(estado[0])]


class AgenteAleatorio(entornos_f.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        robot, situacion = percepcion
        return (choice(["ir_B", "limpiar", "nada", "ir_F"]) if robot == "A" else
                choice(["ir_A", "limpiar", "nada", "ir_C"]) if robot == "B" else
                choice(["ir_B", "limpiar", "nada", "ir_D"]) if robot == "C" else
                choice(["ir_C", "limpiar", "nada", "ir_E"]) if robot == "D" else
                choice(["ir_F", "limpiar", "nada", "ir_D"]) if robot == "E" else
                choice(["ir_A", "limpiar", "nada", "ir_E"]) 
                )


class AgenteReactivoSeiscuartos(entornos_f.Agente):
    """
    Un agente reactivo simple
    """
    def programa(self, percepción):
        robot, situación = percepción
        return ('limpiar' if situación == 'sucio' else
                'ir_B' if robot == "A" else
                'ir_C' if robot == "B" else
                'ir_D' if robot == "C" else
                'ir_E' if robot == "D" else
                'ir_F' if robot == "E" else
                'ir_A')


class AgenteReactivoModeloSeisCuartos(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio','sucio','sucio','sucio','sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4],self.modelo[5], self.modelo[6]
        return ('nada' if a == b == c == d == e == f == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_B' if robot == 'A' else
                'ir_C' if robot == 'B' else
                'ir_D' if robot == 'C' else
                'ir_E' if robot == 'D' else
                'ir_F' if robot == 'E' else
                'ir_A')


def prueba_agente(agente):
    entornos_f.imprime_simulación(
        entornos_f.simulador(
            SeisCuartos(),
            agente,
            ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"],
            100),
        ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    )

def test_Agentes():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['ir_A', 'ir_B','ir_C','ir_D','ir_E','ir_F',
                                   'limpiar', 'nada']))

    print("Prueba del entorno con un agente reactivo")
    prueba_agente(AgenteReactivoSeiscuartos())

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloSeisCuartos())
    

""" 
   2. Busqueda Ciega.
      A continuación se encuentra todo el codigo que resuelve el 
      ejercicio 2.
"""
class Graph:
    """
    Clase Graph, nos permite abstraer una gráfica, una 
    gráfica es una lista de aristas y una lista de vertices.
    """
    def __init__(self):
        self.graph = {}
        self.vertices = []
        
    def estoy_enG(self, v):
        """
        similar a v in self.vertices
        """
        for w in self.vertices:
            if w == v:
                return True
        return False
    
    def addEdge(self, tupla):
        """
        addEdge: nos permite construir la gráfica
        """
        u, v = tupla
        vertices = []
        estoy = self.estoy_enG(u)
            
        if u not in self.graph:
            self.graph[u] = [v]            
        else:
            self.vertices.append(u)            
            self.graph[u].append(v)

        if self.estoy_enG(v) == False:
            self.vertices.append(v)
            
    def hasIncoming(self, v):
        """
        hasIncoming: nos dice si v es destino en alguna de 
        las aristas de la gráfica.
        """
        incoming = False
        for u in self.graph:
            for w in self.graph[u]:
                    if w == v:
                        return True
        return False
    
    def topologicalSort(self):
        """
        topologicaSort: solucion a la tarea, modifica a la 
        gráfica tal que ahora esta "ordenada" de acuerdo 
        a su topología.
        """
        solucion = []
        vertices = []
        
        for v in self.vertices:
            incoming = False
            for w in self.graph:
                incoming = v in self.graph[w]
                if incoming:
                    break
            if not incoming:
                vertices.append(v)
            
        while vertices:
            n = vertices.pop(0)
            if n not in solucion:
                solucion.append(n)
            if n in self.graph:
                lis = copy.deepcopy(self.graph[n])
                for m in lis:
                    self.graph[n].remove(m)
                    if not self.hasIncoming(m):
                        vertices.append(m)
        return solucion            
        
def test_BusquedaCiega():
    """
    Creamos el ejemplar descritó en la tarea, aplicamos 
    e imprimimos la solución.
    """
    tempGraph = Graph()
    tempGraph.addEdge(("B", "E"))
    tempGraph.addEdge(("B", "C"))
    tempGraph.addEdge(("E", "C"))
    tempGraph.addEdge(("E", "A"))
    tempGraph.addEdge(("A", "C"))
    tempGraph.addEdge(("A", "D"))
    tempGraph.addEdge(("C", "D"))

    print("Gráfica original:")
    for v in tempGraph.graph:
        print(v+":")
        for w in tempGraph.graph[v]:
            print("\t"+ w)

    print("Topological Sort:")
    print(tempGraph.topologicalSort())
    

if __name__ == "__main__":
    test_Agentes()
    test_BusquedaCiega()
    
