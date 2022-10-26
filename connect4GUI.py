from tkinter import *
from tkinter import messagebox


# source : https://stackoverflow.com/questions/17985216/simpler-way-to-draw-a-circle-with-tkinter
# fonction pour placer cercle avec seulement x, y, et r (rayon)
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


# fonction pour chercher 4 pieces de suite du meme type dans le tableau
def verGagnant(tab):
    global boardCanvas
    tabReverse = [t[::-1] for t in tab]
    
    def checkHorizontal(l): # recherche un gagnant sur les rang horizontals
        
        for i in range(len(l)): # pur chaque list de list
            for j in range(0,len(l[i])-3): # pour chaque indice de list de list
                
                stLst = set(l[i][j:j+4])
                
                if (len(stLst) == 1) and list(stLst)[0] in ("o","x"):
                    boardCanvas.create_line( ((j+1)*64)-24, ((i+1)*64)-24, ((j+4)*64)-24, ((i+1)*64)-24,fill="orange",width=5)
                    return list(stLst)[0] # retourn la piece gagnant
        
        return None
    
    
    def checkVertical(l): # recherche un gagnant sur les columns
        
        for col in range(len(l[0])): # pour chaque colomn col de list
            colLst = [l[i][col] for i in range(len(l))] # cree une list du colomn
            for i in range(len(colLst)-3):
                stLst = set(colLst[i:i+4])

                if (len(stLst) == 1) and list(stLst)[0] in ("o","x"):
                    boardCanvas.create_line( ((col+1)*64)-24, ((i+1)*64)-24, ((col+1)*64)-24, ((i+4)*64)-24,fill="orange",width=5)
                    return list(stLst)[0] # retourn la piece gagnant
        
        return None # Si rien
    
    
    def checkDiagonal(l,lR): # recherche un gagnant sur les diagonals du tableu
        
        for currLst in (l, lR):
            for i in range(len(currLst)-3): # rangs du lst
                for j in range(len(currLst)-2): # colomns du lst
                    
                    lst = []
                    for k in range(4):# regard chaque diagonal de 4 vers le bas
                        lst.append(currLst[i+k][j+k])
                    stLst = set(lst)
                    if (len(stLst) == 1) and list(stLst)[0] in ("o", "x"):
                        if currLst == lR:
                            
                            
                            boardCanvas.create_line( ((7-(j))*64)-24, ((i+1)*64)-24, ((7-(j)-3)*64)-24, ((i+1+k)*64)-24,fill="orange",width=5)
                        else:
                            boardCanvas.create_line( ((j+1)*64)-24, ((i+1)*64)-24, ((j+1+k)*64)-24, ((i+1+k)*64)-24,fill="orange",width=5)
                        return list(stLst)[0] # retourn la piece gagnant
        
        return None # si rien

    
    
    def checkDraw(l): # verifie si il y a egalité
        
        if "-" not in l[0]:
            return "DRAW"
        
        return None # si il n'y a pas egalité
    
    
    drawReturn = checkDraw(tab)
    vertReturn = checkVertical(tab)
    horizReturn = checkHorizontal(tab)
    diagReturn = checkDiagonal(tab, tabReverse)
    
    for result in (vertReturn, horizReturn, diagReturn,drawReturn):
        if result:
            return result
    
    return None




# ajoute une piece a cette column
def addToCol(column): 
    global tour, columnRempliLabel, joueurCourant
    i = -1
    
    # columnRempli.set("")
    columnRempliLabel.pack_forget()
    if column[0] == "-": # cherche l'indice du prochain rang libre dans le colomn
        while column[i] != "-":
            i -=1
    else:
        
        # columnRempli.set("Vous ne pouvez pas placer \n un piece ici!")
        columnRempliLabel.pack()
        return column
    

    if tour: # choisi a placer un X ou un O par raport a qui joue
        column[i] = "x"
    else:
        column[i] = "o"
        
    tour = not tour # change de joueur
    
    if tour: # change le message de a quel couleur c'est de jouer
        joueurCourant.set("Joueur Courant: ROUGE")
    else:
        joueurCourant.set("Joueur Courant: JAUNE")
    #print(column)
    return column


# fonction qui appele tout apres avoir choisi un column
def choix(col): 
    global lst
    

    currentCol = [lst[i][col] for i in range(len(lst))] # cree list du column "col"
    currentCol_new = addToCol(currentCol) # ajoute un piece au column (ou pas si elle est rempli)
    
    
    for i in range(len(lst)):
        lst[i][col] = currentCol_new[i] # met a jour le liste du tableau
    
    createGrid(lst)
    
    
    resultat = verGagnant(lst)
 
    # print(resultat)
    if resultat: # affiche boit message si gagné ou egalité
        choix = ""
        if resultat == "DRAW":
            choix = messagebox.askquestion("Resultat", "Personne a gagné, c'est egalité! \n\n Voulais vous rejouer?")
        else:
            choix = messagebox.askquestion("Resultat", "BRAVO, le joueur {} a gagné!! \n\n Voulais vous rejouer?".format("ROUGE" if resultat=="x" else "JAUNE"))
        
        # choix pour rejouer
        if (choix == "yes"):
            start()
        elif (choix == "no"):
            root.destroy()


def start(first=False): # dedruit le fenetre et recree a nouveau pour rejouer
    global root, boardCanvas
    if not first: root.destroy() # si c'est la premier fois de tourner le jeu

    root = Tk()
    root.configure(bg="#bcdd7c")
    root.wm_title("Puissance4")
    root.geometry("466x640")
    root.resizable(False, False)
    root.focus_force()
    boardCanvas = Canvas(root, width=462, height=396, bg="#1b6cfb")
    boardCanvas.place(y=100)
    
    
    main()

    root.mainloop()

def createGrid(gridList):
    global root, boardCanvas
        
    for y in range(1,len(gridList)+1): # place les cercles des pieces
        for x in range(1,len(gridList[0])+1):
            currLst = lst[y-1][x-1]
            
            if (currLst == "o"):
                boardCanvas.create_circle((x*64)-24, (y*64)-24, 24, fill="yellow")
            elif (currLst == "x"):
                boardCanvas.create_circle((x*64)-24, (y*64)-24, 24, fill="red")




def main():
    global lst, l, tour, boardCanvas,columnRempliLabel,joueurCourant
    lst = [ # tableau qui tien tout les pieces ("-" veut dire vide)
        ["-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-"],
    ]
    
#    lst = [ # set as draw game so That I can test
#         ["o", "o", "o", "-", "o", "o", "o"],
#         ["x", "x", "x", "o", "x", "x", "x"],
#         ["o", "o", "x", "x", "x", "o", "x"],
#         ["x", "x", "o", "o", "x", "x", "o"],
#         ["o", "o", "x", "x", "o", "o", "x"],
#         ["o", "o", "x", "x", "o", "x", "o"],
#     ]
    
    for y in range(0,len(lst)+1): # cree les lignes du canvas
        boardCanvas.create_line(0, (y*64)+8, 462, (y*64)+8, fill="#1b58a3", width=12)
    
    for x in range(0,len(lst[0])+1):
        boardCanvas.create_line((x*64)+8, 0, (x*64)+8, 400, fill="#1b58a3", width=12)

    for y in range(1,len(lst)+1): # Place les cercles blancs (les trous) du canvas
        for x in range(1,len(lst[0])+1):

            boardCanvas.create_circle((x*64)-24, (y*64)-24, 24, fill="white")
    
#    createGrid(lst) # decomenter si utilisation de tableau avec pirces predefinis
    
    ############################ variables
    
    columnRempli = StringVar()
    columnRempli.set("Vous ne pouvez plus placer \n de piece ici!")
    
    l = StringVar()
    
    joueurCourant = StringVar()
    joueurCourant.set("Joueur Courant: ROUGE")
    
    tour = True # True = X(rouge), False = O(jaune)
    ############################
    
    # boutton pour quitter
    exitButton = Button(root, text="Quitter", command=root.destroy, bg="red", fg="white").place(x=5, y=5) # ferme le jeu
    
    # boutton pour recommencer
    resetbutton = Button(root, text = "Recommencer", command = start, bg="green", fg="white").place(x=60,y=5)
    
    # text pour si on ne peut pas plus remplire une colomn
    columnRempliLabel = Label(root, text=columnRempli.get(), textvariable=columnRempli, bg="red", fg="yellow")
    
    # text avec le joueur courant
    joueurCourantLabel = Label(root, text=joueurCourant.get(), textvariable=joueurCourant, font=("Arial", 20)).place(x=80,y=50)
    
    
    # button for collumn
    Button(root, text ="1", command=lambda: choix(0),width=4, height=2).place(x=26,y=505)
    Button(root, text ="2", command=lambda: choix(1),width=4, height=2).place(x=88, y=505)
    Button(root, text ="3", command=lambda: choix(2),width=4, height=2).place(x=154, y=505)
    Button(root, text ="4", command=lambda: choix(3),width=4, height=2).place(x=216, y=505)
    Button(root, text ="5", command=lambda: choix(4),width=4, height=2).place(x=280, y=505)
    Button(root, text ="6", command=lambda: choix(5),width=4, height=2).place(x=344, y=505)
    Button(root, text ="7", command=lambda: choix(6),width=4, height=2).place(x=408, y=505)
    
    # assigne un clef de clavier pour aussi designer un rang.
    # ne marche pas dans un boucle, jsp pourquoi.
    root.bind("1", lambda event: choix(0))
    root.bind("2", lambda event: choix(1))
    root.bind("3", lambda event: choix(2))
    root.bind("4", lambda event: choix(3))
    root.bind("5", lambda event: choix(4))
    root.bind("6", lambda event: choix(5))
    root.bind("7", lambda event: choix(6))
    
    
    
    
# commance le jeu pour le premier fois
start(True)
