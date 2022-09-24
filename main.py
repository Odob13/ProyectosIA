import pygame as p
import Functions.Read_Maze as rm
import collections
import numpy as np
p.init()


class DFSPath:

    def __init__(self,start,objective):
        self.start = tuple(np.subtract((Alto,Ancho),start))
        self.objective = objective

        self.actualPosition = self.start

        self.actualPath = collections.deque()
        self.actualPath.append(self.actualPosition)

        self.directions = collections.deque()


    def tryUp(self):
        nextMove = tuple(np.subtract(self.actualPosition,(verticalStep,0)))

        validMove = nextMove in validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    def tryDown(self):
        nextMove = tuple(np.add(self.actualPosition,(verticalStep,0)))

        validMove = nextMove in validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    def tryLeft(self):
        nextMove = tuple(np.subtract(self.actualPosition,(0,horizontalStep)))

        validMove =  nextMove in validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    def tryRight(self):
        nextMove = tuple(np.add(self.actualPosition,(0,horizontalStep)))

        validMove = nextMove in validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    def CheckObjective(self):
        return (self.actualPosition == self.objective)


    def explore(self):
        if not self.CheckObjective():
            if self.tryUp():
                self.actualPosition = tuple(np.subtract(self.actualPosition,(verticalStep,0)))
                self.directions.append("up")
                self.actualPath.append(self.actualPosition)

            elif self.tryLeft():
                self.actualPosition = tuple(np.subtract(self.actualPosition,(0,horizontalStep)))
                self.directions.append("left")
                self.actualPath.append(self.actualPosition)

            elif self.tryDown():
                self.actualPosition = tuple(np.add(self.actualPosition,(verticalStep,0)))
                self.directions.append("down")
                self.actualPath.append(self.actualPosition)

            elif self.tryRight():
                self.actualPosition = tuple(np.add(self.actualPosition,(0,horizontalStep)))
                self.directions.append("right")
                self.actualPath.append(self.actualPosition)

            else:
                if self.actualPath:
                    print(validPositions)
                    print(f"self.actualPath[-1] = {self.actualPath[-1]}")
                    validPositions.remove(self.actualPath.pop())
                    print(validPositions)
                    self.actualPosition = self.actualPath[-1]
                self.directions.pop()


            print(self.directions)
        else:
            print("Objective found")
            print("Path:")
            for action in self.directions:
                print(action)






#-------------------Muros------------------------
def construir_mapa(mapa, n):
    listaMuros = []
    x= 0
    y= 0
    for fila in mapa:
        for muro in fila:
            if muro == "X":
                listaMuros.append(p.Rect(x,y,Ancho/n,Alto/n))
            x+= Ancho/n
        x= 0
        y+=Alto/n
    return listaMuros
#-------------------Puntos-------------------------
def construir_puntos(mapa, n):
    listaPuntos = []
    x= (Ancho/n)/4
    y= (Alto/n)/4
    for fila in mapa:
        for muro in fila:
            if muro == " ":
                listaPuntos.append(p.Rect(x,y,(Ancho/n)/2,(Alto/n)/2))
            x+= Ancho/n
        x= (Ancho/n)/4
        y+=Alto/n
    return listaPuntos


def dibujar_muro ( superficie , rectangulo, color ) : #Dibujamos un rectángulo
   p.draw.rect( superficie , color , rectangulo )

def dibujar_mapa ( superficie , listaMuros , listaPuntos) : #Dibujamos ListaMuros con los rectángulos muro
    for muro in listaMuros :
        dibujar_muro ( superficie , muro , AZUL )
    for puntos in listaPuntos :
        dibujar_muro ( superficie , puntos , NEGRO )

ventana = p.display.set_mode((800,600), p.RESIZABLE)
Pantalla = p.display.get_surface()
Ancho = Pantalla.get_width()
Alto= Pantalla.get_height()

p.display.set_caption('Muro')
reloj = p.time.Clock()

AZUL=(0,0,128)
NEGRO=(0,0,0)
BLANCO=(255,255,255)

y=int(input("size of maze: "))

m= rm.ReadMaze(f"maze_{y}x{y}.csv")
mapa = rm.ConvertMatrixToMap(m)

gameOver = False

startPosition = (1 * (Alto/y),2 * (Ancho/y))
objecitvePosition = (0 + (Alto/y), 0 + (Ancho/y))

horizontalStep = Ancho/y
verticalStep = Alto/y



DFSagent = DFSPath(startPosition,objecitvePosition)


listaMuros = construir_mapa(mapa, y)
validPositions = [(muro[1],muro[0]) for muro in listaMuros]
listaPuntos = construir_puntos(mapa, y)

while not gameOver:

    reloj.tick(15)



    for event in p.event.get():
        if event.type == p.QUIT:
            gameOver=True

    #-------------Fondo------------------
    ventana.fill(BLANCO)
    #------------Dibujo------------------
    dibujar_mapa (ventana , listaMuros, listaPuntos)
    p.draw.rect(ventana,(0,255,0),p.Rect(Ancho-startPosition[1] + (Ancho/(4*y)),Alto-startPosition[0] + (Alto/(4*y)),(Ancho/y)/2,(Alto/y)/2))
    p.draw.rect(ventana,(255,0,0),p.Rect(objecitvePosition[1] + (Ancho/(4*y)),objecitvePosition[0] + (Alto/(4*y)),(Ancho/y)/2,(Alto/y)/2))

    DFSagent.explore()
    print(DFSagent.actualPosition)
    p.draw.rect(ventana,(255,255,0),p.Rect(DFSagent.actualPosition[1] + (Ancho/(4*y)),DFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    p.display.flip()




p.quit()

