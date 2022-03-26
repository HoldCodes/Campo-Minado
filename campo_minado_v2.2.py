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
        self.cont = 0

        self.tabuleiro = np.zeros((self.tab_x, self.tab_y), dtype=Terreno)
        self.n_bombas = int((self.tab_x * self.tab_y)/8)
        self.quadrados = self.tab_x * self.tab_y
        self.marcas = 0

        self.window.title("Campo Minado")
        self.window.geometry(f"+{int((self.window.winfo_screenwidth()/2) - (46*self.tab_y/2))}+"
                             f"{int((self.window.winfo_screenheight()/2) - (((46*self.tab_x)+44)/2))}")
        self.window.resizable(False, False)

        self.container1 = Frame(self.window)
        self.container2 = Frame(self.window)

        self.container1.grid(column=0, row=0)
        self.container2.grid(column=0, row=1, pady=10)

        Label(self.container1, text="Campo Minado", font=16).grid(column=1, row=0, padx=200)
        Label(self.container1, text=f"Bombas: {self.n_bombas}", font=16).grid(column=2, row=0, sticky=W)
        self.txt = Label(self.container1, text="Marcados: 0", font=16)
        self.txt.grid(column=0, row=0)

        for i in range(0, self.tab_x):
            for j in range(0, self.tab_y):
                self.btn = Button(self.container2, width=4, height=2, command=lambda x=i, y=j: self.analisa(x, y),
                                  bg="gainsboro", font="BOLD")
                self.btn.grid(column=j, row=i)
                self.btn.bind("<Button-3>", lambda event, x=i, y=j: self.rightClick(x, y))
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

    def reinicio(self):
        self.window.destroy()
        main()

    def encerra_jogo(self, vitoria):

        for i in range(self.tab_x):
            for j in range(self.tab_y):
                if self.tabuleiro[i][j].bomba:
                    self.tabuleiro[i][j].botao.configure(text="X", bg="red")

        newWindow = tkinter.Toplevel()

        newWindow.geometry(f"200x50+{int(newWindow.winfo_screenwidth()/2)}+{int(newWindow.winfo_screenheight()/2)}")

        label1 = Label(newWindow, font=("Courier", 12, "italic"), fg="blue")
        label1.pack()

        Button(newWindow, text="Reiniciar", command=lambda: [newWindow.destroy(), self.reinicio()]).pack(side=BOTTOM)

        newWindow.grab_set()

        if vitoria:
            label1.config(text="Vitoria")

        if not vitoria:
            label1.config(text="Derrota", fg="red")

    def limpa_zero(self, x, y):

        self.cont += 1

        for i in range(0, 3):
            for j in range(0, 3):
                if i + x >= 0 and j + y >= 0:
                    if i + x <= self.tab_x - 1 and j + y <= self.tab_y - 1:
                        if not self.tabuleiro[x + i][y + j].clickado:
                            self.tabuleiro[x + i][y + j].clickado = True
                            self.quadrados -= 1
                            self.cor(x+i, y+j)
                            self.tabuleiro[x+i][y+j].botao.configure(text=self.tabuleiro[x+i][y+j].bombas_em_volta,
                                                                     bg="gainsboro")

                            if self.tabuleiro[x + i][y + j].bombas_em_volta == 0:
                                self.quadrados += 1
                                self.limpa_zero(x+i-1, y+j-1)

        self.quadrados = self.quadrados - 1

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

    def analisa(self, x, y):

        if not self.tabuleiro[x][y].bomba and not self.tabuleiro[x][y].clickado:
            self.tabuleiro[x][y].clickado = True
            self.tabuleiro[x][y].botao.configure(text=self.tabuleiro[x][y].bombas_em_volta, bg="gainsboro")
            self.quadrados = self.quadrados - 1
            self.cor(x, y)

            if self.quadrados == self.n_bombas:
                self.encerra_jogo(True)

            if self.tabuleiro[x][y].bombas_em_volta == 0:
                self.quadrados += 1
                self.limpa_zero(x-1, y-1)

        if self.tabuleiro[x][y].bomba:
            self.tabuleiro[x][y].botao.configure(text="X")
            self.encerra_jogo(False)

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
                self.tabuleiro[i][j].bombas_em_volta = self.analisa_entorno(i, j)

    def run(self):
        self.jogo()
        self.window.mainloop()


def main():
    instancia = Campo()
    instancia.run()


main()
