import random
import tkinter
import numpy as np
from tkinter import *


class Terreno:
    def __init__(self, btn):
        self.botao = btn
        self.bombas_em_volta = 0
        self.bomba = False
        self.clickado = False
        self.marcado = False

    def tem_bomba(self):
        self.bomba = True

    def foi_clickado(self):
        self.clickado = True


class Campo:
    def __init__(self):
        self.window = Tk()

        self.tab_x = 10
        self.tab_y = 20

        self.tabuleiro = np.zeros((self.tab_x, self.tab_y), dtype=Terreno)
        self.n_bombas = int((self.tab_x * self.tab_y)/8)
        self.quadrados = self.tab_x * self.tab_y
        self.marcas = 0

        self.window.title("Campo Minado")
        self.window.resizable(False, False)

        self.container1 = Frame(self.window)
        self.container2 = Frame(self.window)

        self.container1.grid(column=0, row=0)
        self.container2.grid(column=0, row=1, pady=10)

        Label(self.container1, text="Campo Minado", font=16).grid(column=1, row=0, padx=200)
        Label(self.container1, text=f"Bombas: {self.n_bombas}", font=16).grid(column=2, row=0, sticky=W)
        self.txt = Label(self.container1, text="Marcados: 0",font=16)
        self.txt.grid(column=0, row=0)

        for i in range(0, self.tab_x):
            for j in range(0, self.tab_y):
                self.btn = Button(self.container2, width=8, height=4, command=lambda x = i, y = j: self.analisa(x, y), bg="gainsboro")
                self.btn.grid(column=j, row=i)
                self.btn.bind("<Button-3>", lambda event, x = i, y = j: self.rightClick(x, y))
                self.instancia = Terreno(self.btn)
                self.tabuleiro[i][j] = self.instancia


    def rightClick(event, x, y):

        if event.tabuleiro[x][y].marcado and not event.tabuleiro[x][y].clickado:
            event.tabuleiro[x][y].botao.configure(text="", bg="gainsboro")

        if not event.tabuleiro[x][y].marcado and not event.tabuleiro[x][y].clickado:
            event.tabuleiro[x][y].botao.configure(text="", bg="red")
            event.tabuleiro[x][y].marcado = True
            event.marcas += 1

        elif event.tabuleiro[x][y].marcado and not event.tabuleiro[x][y].clickado:
            event.tabuleiro[x][y].marcado = False
            event.marcas -= 1

        event.txt.config(text=f"Marcados: {event.marcas}")

    def cor(self, i, j):

        if self.tabuleiro[i][j].bombas_em_volta == 0:
            self.tabuleiro[i][j].botao.configure(text="0", fg='black')

        elif self.tabuleiro[i][j].bombas_em_volta == 1:
            self.tabuleiro[i][j].botao.configure(text='1', fg='green')

        elif self.tabuleiro[i][j].bombas_em_volta == 2:
            self.tabuleiro[i][j].botao.configure(text="2", fg='brown')

        elif self.tabuleiro[i][j].bombas_em_volta == 3:
            self.tabuleiro[i][j].botao.configure(text="3", fg='orange')

        elif self.tabuleiro[i][j].bombas_em_volta == 4:
            self.tabuleiro[i][j].botao.configure(text="4", fg='red')

        elif self.tabuleiro[i][j].bombas_em_volta == 5:
            self.tabuleiro[i][j].botao.configure(text="5", fg='blue')

        elif self.tabuleiro[i][j].bombas_em_volta == 6:
            self.tabuleiro[i][j].botao.configure(text="6", fg='violet')

        else:
            self.tabuleiro[i][j].botao.configure(fg='black')

    def encerra_jogo(self, vitoria):

        newWindow = tkinter.Toplevel()

        label1 = Label(newWindow, font=("Courier", 12, "italic"), fg="blue")
        label1.pack()

        Button(newWindow, text="Reiniciar", command=lambda: [newWindow.destroy(), self.reinicio()]).pack(side=BOTTOM)

        newWindow.grab_set()

        if vitoria:
            label1.config(text="Vitoria")

        if not vitoria:
            label1.config(text="Derrota")

    def analisa(self, x, y):

        if not self.tabuleiro[x][y].bomba and not self.tabuleiro[x][y].clickado:
            self.tabuleiro[x][y].clickado = True
            #self.tabuleiro[x][y].botao.configure(state=DISABLED)
            self.tabuleiro[x][y].botao.configure(text=self.tabuleiro[x][y].bombas_em_volta)
            self.quadrados = self.quadrados - 1
            self.cor(x, y)
            print(self.quadrados)

            if self.quadrados == self.n_bombas:
                self.encerra_jogo(True)

            #if self.tabuleiro[x][y].bombas_em_volta == 0:
                #self.analisa_entorno(x, y, True)

        if self.tabuleiro[x][y].bomba:
            self.tabuleiro[x][y].botao.configure(text="BOMBA")
            self.encerra_jogo(False)

    def analisa_entorno(self, x, y, limpa_area):

        bombas = 0

        if not self.tabuleiro[x][y].bomba:

            x -= 1
            y -= 1

            for i in range(0, 3):
                for j in range(0, 3):
                    if i + x >= 0 and j + y >= 0:
                        if i + x <= self.tab_x - 1 and j + y <= self.tab_y - 1:
                            if self.tabuleiro[i+x][j+y].bomba:
                                bombas += 1

                                #para quando for 0
                            if limpa_area:
                                if not self.tabuleiro[x + i][y + j].clickado:
                                    self.quadrados = self.quadrados - 1
                                    print(self.quadrados)
                                self.tabuleiro[x+i][y+j].clickado = True
                                self.tabuleiro[x+i][y+j].botao.configure(state=DISABLED)
                                self.tabuleiro[x+i][y+j].botao.configure(text=self.tabuleiro[x+i][y+j].bombas_em_volta)
        return bombas

    def reinicio(self):
        self.window.destroy()
        main()
        #for i in range(self.tab_x):
            #for j in range(self.tab_y):
                #self.tabuleiro[i][j].botao.configure(text="")
                #self.tabuleiro[i][j].bombas_em_volta = 0
                #self.tabuleiro[i][j].bomba = False
                #self.tabuleiro[i][j].clickado = False

        #self.jogo()

    def jogo(self):

        # Gera bombas
        k = 0
        while k != self.n_bombas:
            k += 1
            x = random.randint(0, self.tab_x-1)
            y = random.randint(0, self.tab_y-1)

            if self.tabuleiro[x][y].bomba:
                k -= 1

            self.tabuleiro[x][y].bomba = True

        for i in range(self.tab_x):
            for j in range(self.tab_y):
                self.tabuleiro[i][j].bombas_em_volta = self.analisa_entorno(i, j, False)

    def run(self):
        self.jogo()
        self.window.mainloop()


def main():
    instancia = Campo()
    instancia.run()


main()
