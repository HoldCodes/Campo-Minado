import random
import numpy as np
from tkinter import *


class Terreno:
    def __init__(self, btn):
        self.botao = btn
        self.bombas_em_volta = 0
        self.bomba = False
        self.clickado = False

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
        self.n_bombas = 20

        self.window.title("Campo Minado")
        self.window.eval('tk::PlaceWindow . center')
        self.window.resizable(False, False)

        self.container1 = Frame(self.window)
        self.container2 = Frame(self.window)
        self.container1.grid(column=0, row=0)
        self.container2.grid(column=0, row=1, pady=10)

        self.txt1 = Label(self.container1, text="Campo Minado")
        self.txt1.grid()

        self.lista = []

        self.k = 0

        for i in range(0, self.tab_x):
            for j in range(0, self.tab_y):
                self.k += 1
                self.btn = Button(self.container2, width=5, height=3, command=lambda x = i, y = j: self.analisa(x, y), text=f'{self.k}')
                self.btn.grid(column=j, row=i)
                self.instancia = Terreno(self.btn)
                self.tabuleiro[i][j] = self.instancia

    def encerra_jogo(self, vitoria):
        print()

    def analisa(self, x, y):

        if not self.tabuleiro[x][y].bomba:
            self.tabuleiro[x][y].clickado = True
            self.tabuleiro[x][y].botao.configure(state=DISABLED)
            self.tabuleiro[x][y].botao.configure(text=self.tabuleiro[x][y].bombas_em_volta)

        else:
            self.tabuleiro[x][y].botao.configure(text="BOMBA")
            self.encerra_jogo(False)

    def analisa_entorno(self, x, y):

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
        return bombas

    def jogo(self):

        # Muda o nome de todos os botoes
        for i in range(self.tab_x):
            for j in range(self.tab_y):
                self.tabuleiro[i][j].botao.configure(text="")

        # Gera bombas
        for i in range(0, self.n_bombas):
            x = random.randint(0,self.tab_x-1)
            y = random.randint(0,self.tab_y-1)

            self.tabuleiro[x][y].bomba = True

        #Coloca 1 nas bombas
        for i in range(self.tab_x):
            for j in range(self.tab_y):
                if self.tabuleiro[i][j].bomba:
                    self.tabuleiro[i][j].botao.configure(text="")

        for i in range(self.tab_x):
            for j in range(self.tab_y):
                self.tabuleiro[i][j].bombas_em_volta = self.analisa_entorno(i, j)

    def run(self):
        self.jogo()
        self.window.mainloop()


def main():
    instancia = Campo()
    instancia.run()


main()
