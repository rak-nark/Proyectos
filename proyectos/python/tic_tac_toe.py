import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Mejorado")

        # Inicializar variables
        self.jugador_actual = "X"
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.botones = []
        self.modo_vs_computadora = False
        self.puntaje = {"X": 0, "O": 0}

        # Crear interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Crear el tablero de botones
        for fila in range(3):
            fila_botones = []
            for col in range(3):
                boton = tk.Button(self.root, text=" ", font=("Arial", 24), width=5, height=2,
                                    bg="white", fg="black",
                                    command=lambda f=fila, c=col: self.realizar_movimiento(f, c))
                boton.grid(row=fila, column=col)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

        # Etiqueta para mostrar el jugador actual
        self.etiqueta_turno = tk.Label(self.root, text=f"Turno del jugador: {self.jugador_actual}",
                                        font=("Arial", 16))
        self.etiqueta_turno.grid(row=3, column=0, columnspan=3)

        # Mostrar puntaje
        self.etiqueta_puntaje = tk.Label(self.root, text=f"Puntaje - X: {self.puntaje['X']} | O: {self.puntaje['O']}",
                                            font=("Arial", 14), fg="blue")
        self.etiqueta_puntaje.grid(row=4, column=0, columnspan=3)

        # Botón para jugar contra la computadora
        self.boton_computadora = tk.Button(self.root, text="Jugar contra la computadora",
                                            font=("Arial", 12), bg="lightgray",
                                            command=self.activar_modo_computadora)
        self.boton_computadora.grid(row=5, column=0, columnspan=3, pady=10)

    def realizar_movimiento(self, fila, col):
        if self.tablero[fila][col] == " ":
            # Actualizar tablero y botón
            self.tablero[fila][col] = self.jugador_actual
            self.botones[fila][col].config(text=self.jugador_actual, state="disabled", bg="lightblue")

            # Verificar si hay un ganador
            if self.verificar_ganador():
                self.mostrar_ganador(self.jugador_actual)
                return

            # Verificar si es un empate
            if self.tablero_lleno():
                self.mostrar_ganador("Empate")
                return

            # Cambiar de jugador
            self.jugador_actual = "O" if self.jugador_actual == "X" else "X"
            self.etiqueta_turno.config(text=f"Turno del jugador: {self.jugador_actual}")

            # Si el modo contra computadora está activado y es el turno de la IA
            if self.modo_vs_computadora and self.jugador_actual == "O":
                self.movimiento_computadora()

        else:
            messagebox.showerror("Movimiento inválido", "Esta casilla ya está ocupada.")

    def verificar_ganador(self):
        # Verificar filas
        for fila in self.tablero:
            if fila[0] == fila[1] == fila[2] != " ":
                return True

        # Verificar columnas
        for col in range(3):
            if self.tablero[0][col] == self.tablero[1][col] == self.tablero[2][col] != " ":
                return True

        # Verificar diagonales
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != " " or \
            self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != " ":
            return True

        return False

    def tablero_lleno(self):
        return all(casilla != " " for fila in self.tablero for casilla in fila)

    def mostrar_ganador(self, ganador):
        if ganador == "Empate":
            messagebox.showinfo("Resultado", "¡Es un empate!")
        else:
            self.puntaje[ganador] += 1
            messagebox.showinfo("Resultado", f"¡Jugador {ganador} gana!")
        self.actualizar_puntaje()
        self.reiniciar_juego()

    def actualizar_puntaje(self):
        self.etiqueta_puntaje.config(text=f"Puntaje - X: {self.puntaje['X']} | O: {self.puntaje['O']}")

    def reiniciar_juego(self):
        self.jugador_actual = "X"
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        for fila in self.botones:
            for boton in fila:
                boton.config(text=" ", state="normal", bg="white")
        self.etiqueta_turno.config(text=f"Turno del jugador: {self.jugador_actual}")

    def activar_modo_computadora(self):
        self.modo_vs_computadora = not self.modo_vs_computadora
        modo = "activado" if self.modo_vs_computadora else "desactivado"
        messagebox.showinfo("Modo computadora", f"Modo contra la computadora {modo}.")
        self.reiniciar_juego()

    def movimiento_computadora(self):
        casillas_vacias = [(f, c) for f in range(3) for c in range(3) if self.tablero[f][c] == " "]
        fila, col = random.choice(casillas_vacias)
        self.realizar_movimiento(fila, col)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()


