import pygame as PyGame
import random

Blue = (135,206,250)
Window_Size = (1215,750)  #golden ratio
Buffer = 20
Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


Grid_OG = [[Grid[x][y] for y in range(len(Grid[0]))] for x in range(len(Grid))]
OG_Grid_Element_Color = (52,31,151)


def insert(Window, Position):
        
        MyFont = PyGame.font.SysFont('Comic Sans MS', 60)
        i,j = Position[1], Position[0]
        while True:
            for event in PyGame.event.get():
                if event.type == PyGame.QUIT:
                    return
            
                if event.type == PyGame.KEYDOWN:                       
                    if (Grid_OG[i][j] != 0):   #if original grid element is not empty, return. 
                        return
                    if (Grid[i][j] != 0) and (event.key != 48): #prevent overwrite
                        return    
                    if(event.key == 48):  #deleting input
                        Grid[i][j] = event.key - 48
                        PyGame.draw.rect(Window, PyGame.Color("white"), (Position[0]*80+21, Position[1]*80+20,70,70))
                        PyGame.display.update()
                        return
                    if(0 < event.key - 48 <10):  #check for valid input
                        PyGame.draw.rect(Window, PyGame.Color("white"), (Position[0]*80 + Buffer, Position[1]*80+ Buffer,80 -2*Buffer , 80 - 2*Buffer))
                        Element = MyFont.render(str(event.key-48), True, (0,0,0))
                        Window.blit(Element, (Position[0]*80 + 40, Position[1]*80+10))
                        Grid[i][j] = event.key - 48
                        PyGame.display.update()
                        return
                    return
                    
def SolverMethod(Row, Column, Numeros):
        global Grid
        
        for n in range(0,9):
                if Grid_OG[Row][n] == Numeros:#[Row][n] liste sabit, o listenin icindeki elemanlar denenir
                        return False
        for m in range(0,9):
                if Grid_OG[m][Column] == Numeros:#[m][Column]eleman sirasi sabit, listelerde ki o elemani dener
                        return False
        
        M0 = (Column // 3) * 3
        N0 = (Row // 3) * 3
        for n in range(0,3):
            for m in range(0,3):
                if Grid_OG[N0+m][M0+n] == Numeros:
                    return False

        return True

solved = 0

def solve(Window):
    
    global Grid
    for event in PyGame.event.get():
            if event.type == PyGame.KEYDOWN:
                if(event.key == 13):
                        Grid = Grid_OG
                        PyGame.display.update()
    G = [1,2,3,4,5,6,7,8,9]
    random.shuffle(G)# in order to generate/obtain unique grids everytime !!!
    MyFont = PyGame.font.SysFont('Comic Sans MS', 60)
    for Row in range(0,9):
        for Column in range(0,9):
            if Grid_OG[Row][Column] == 0:
                for Numeros in (G):
                    if SolverMethod(Row, Column, Numeros):
                        Grid_OG[Row][Column] = Numeros
                        PyGame.draw.rect(Window, PyGame.Color("white"), (Column*80+21, Row*80+20,70,70))
                        Element = MyFont.render(str(Numeros), True, (0,0,0))
                        Window.blit(Element, (Column*80 + 40, Row*80+10))
                        PyGame.display.update()
                        PyGame.time.delay(1)
                        solve(Window)
                        global solved
                        if (solved == 1):
                            return
                        
                        Grid_OG[Row][Column] = 0
                        PyGame.draw.rect(Window, PyGame.Color("white"), (Column*80+21, Row*80+20,70,70))
                        PyGame.display.update()

                return
    solved = 1
        
def main():
    PyGame.init()
    Window = PyGame.display.set_mode(Window_Size)
    PyGame.display.set_caption("Sudoku")
    Window.fill(PyGame.Color("white"))
    MyFont = PyGame.font.SysFont('Comic Sans MS', 60)

    for i in range(0,10):
        if i % 3 == 0:
            PyGame.draw.line(Window, PyGame.Color("black"), ((i*80)+15,15), ((i*80)+15,735), width=8)
            PyGame.draw.line(Window, PyGame.Color("black"), (15,(i*80)+15), (735,(i*80)+15), width=8)
        else:
            PyGame.draw.line(Window, PyGame.Color("black"), ((i*80)+15,15), ((i*80)+15,735), width=4)
            PyGame.draw.line(Window, PyGame.Color("black"), (15,(i*80)+15), (735,(i*80)+15), width=4)
        i+=1
    PyGame.display.update()

    for i in range(0, len(Grid[0])):
        for j in range(0, len(Grid[0])):
            if(0<Grid[i][j]<10):
                Element = MyFont.render(str(Grid[i][j]), True, OG_Grid_Element_Color)
                Window.blit(Element, ((j+1)*80-40,(i+1)*80-70))
    PyGame.display.update()

    while True: 
        for event in PyGame.event.get():
            if event.type == PyGame.MOUSEBUTTONUP and event.button == 1:
                coordinate = PyGame.mouse.get_pos()
                insert(Window, (coordinate[0]//80, coordinate[1]//80))
            if event.type == PyGame.KEYDOWN:
                if(event.key == 13):
                    solve(Window)
                    #return
            if event.type == PyGame.QUIT:
                PyGame.quit()
                return

main()


