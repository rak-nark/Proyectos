import tkinter as tk
from tkinter import messagebox

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.configure(bg="#2b2b2b")
        self.root.geometry("375x550")
        self.root.resizable(False, False)

        # Entrada de texto
        self.entrada = tk.Entry(
            root,
            width=17,
            font=("Arial", 28),
            borderwidth=0,
            relief="solid",
            bg="#2b2b2b",
            fg="white",
            justify='right'
        )
        self.entrada.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=10, pady=(10, 5))

        # Crear botones
        self.crear_botones()

    def crear_botones(self):
        # Lista de botones: (texto, número de columnas que ocupa)
        botones = [
            ('C', 1), ('←', 1), ('/', 1), ('*', 1),
            ('7', 1), ('8', 1), ('9', 1), ('-', 1),
            ('4', 1), ('5', 1), ('6', 1), ('+', 1),
            ('1', 1), ('2', 1), ('3', 1), ('=', 1),
            ('0', 2), ('.', 1),
        ]

        # Colores para diferentes tipos de botones
        colores_botones = {
            'numero': '#4d4d4d',
            'operador': '#fe9505',
            'igual': '#fe9505',
            'fondo': '#2b2b2b',
            'texto': '#ffffff',
            'reset': '#d32f2f',
            'borrar': '#f39505'
        }

        # Frame para los botones
        frame_botones = tk.Frame(self.root, bg=colores_botones['fondo'])
        frame_botones.grid(row=1, column=0, columnspan=4, pady=(0, 10))

        fila = 0
        columna = 0

        # Crear y posicionar botones
        for boton, span in botones:
            if boton in ['/', '*', '-', '+']:
                color_fondo = colores_botones['operador']
            elif boton == '=':
                color_fondo = colores_botones['igual']
            elif boton == 'C':
                color_fondo = colores_botones['reset']
            elif boton == '←':
                color_fondo = colores_botones['borrar']
            else:
                color_fondo = colores_botones['numero']

            # Crear botón
            btn = tk.Button(
                frame_botones,
                text=boton,
                width=5 * span,
                height=2,
                font=('Arial', 20),
                bg=color_fondo,
                fg=colores_botones['texto'],
                borderwidth=0,
                command=lambda b=boton: self.click_boton(b)
            )
            # Posicionar botón
            btn.grid(row=fila, column=columna, columnspan=span, padx=1, pady=1, sticky="nsew")

            # Actualizar posición
            columna += span
            if columna >= 4:  # Cambiar de fila cuando se llenan 4 columnas
                columna = 0
                fila += 1

        # Configurar expansión de filas y columnas
        for i in range(4):
            frame_botones.grid_columnconfigure(i, weight=1)
        for i in range(fila + 1):
            frame_botones.grid_rowconfigure(i, weight=1)

    def click_boton(self, valor):
        if valor == '=':
            try:
                resultado = str(eval(self.entrada.get()))
                self.entrada.delete(0, tk.END)
                self.entrada.insert(tk.END, resultado)
            except Exception as e:
                messagebox.showerror("Error", "Entrada no válida")
                self.entrada.delete(0, tk.END)
        elif valor == "C":
            self.entrada.delete(0, tk.END)
        elif valor == "←":
            contenido = self.entrada.get()
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, contenido[:-1])
        else:
            self.entrada.insert(tk.END, valor)

if __name__ == "__main__":
    root = tk.Tk()
    calculadora = Calculadora(root)
    root.mainloop()
