import tkinter as tk
# si tenes ubuntu y NO tenes tkinter instalado, instalarlo con:
# sudo apt-get install python3-tk
# si usas chocolate en windows, instalarlo con:
# choco install python-tk

# Si no podes instalarlo, buscá en internet y consultá en clases a algún docente.
from tkinter import messagebox
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                        reiniciar_juego, verificar_victoria, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO)


class InterfazBuscaminas:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscaminas")
        self.estado_juego = crear_juego(8, 8, 10)
        self.botones = []
        self.crear_interfaz()
        self.actualizar_interfaz()

    def crear_interfaz(self):
        """Crea los elementos de la interfaz gráfica con los nuevos botones"""
        # Frame superior con controles
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=15)

        # Botón para guardar estado
        tk.Button(
            self.control_frame,
            text="Guardar Estado",
            command=self.guardar_estado
        ).pack(side=tk.LEFT, padx=5)

        # Botón para cargar estado
        tk.Button(
            self.control_frame,
            text="Cargar Estado",
            command=self.cargar_estado
        ).pack(side=tk.LEFT, padx=5)

        # Botón para reiniciar juego
        tk.Button(
            self.control_frame,
            text="Reiniciar",
            command=self.reiniciar_juego
        ).pack(side=tk.LEFT, padx=5)

        # Frame para el tablero
        self.tablero_frame = tk.Frame(self.root)
        self.tablero_frame.pack()

        # Crear botones del tablero
        for i in range(self.estado_juego['filas']):
            fila_botones = []
            for j in range(self.estado_juego['columnas']):
                btn = tk.Button(
                    self.tablero_frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Courier", 12, "bold"),
                    command=lambda i=i, j=j: self.manejar_clic_izquierdo(i, j)
                )
                btn.bind("<Button-3>", lambda event, i=i,
                         j=j: self.manejar_clic_derecho(i, j))
                btn.grid(row=i, column=j)
                fila_botones.append(btn)
            self.botones.append(fila_botones)

    def actualizar_interfaz(self):
        """Actualiza la interfaz según el estado del juego"""
        estado = obtener_estado_tablero_visible(self.estado_juego)
        for i in range(self.estado_juego['filas']):
            for j in range(self.estado_juego['columnas']):
                texto = str(estado[i][j])
                fg = self.obtener_color_texto(texto)
                bg = self.obtener_color_fondo(texto)
                self.botones[i][j].config(
                    text=texto,
                    fg=fg,
                    bg=bg,
                    state="normal",
                    relief="sunken" if texto != VACIO and texto != BANDERA else "raised"
                )

    def obtener_color_texto(self, valor: str) -> str:
        colores = {
            '1': 'blue',
            '2': 'green',
            '3': 'red',
            '4': 'darkblue',
            '5': 'brown',
            '6': 'teal',
            '7': 'black',
            '8': 'gray',
            BOMBA: 'black',
            BANDERA: 'white'
        }
        return colores[valor] if valor in colores else 'black'

    def obtener_color_fondo(self, valor: str) -> str:
        if valor == BOMBA:
            return 'red'
        elif valor == BANDERA:
            return 'gray'
        elif valor.isdigit():
            return 'lightgray'
        else:
            return 'gray85'  # fondo por defecto

    def manejar_clic_izquierdo(self, fila: int, columna: int):
        """Maneja el evento de clic izquierdo en una celda"""
        if self.estado_juego['tablero_visible'][fila][columna] != VACIO or self.estado_juego['juego_terminado']:
            return

        descubrir_celda(self.estado_juego, fila, columna)
        self.actualizar_interfaz()

        if self.estado_juego['juego_terminado']:
            if verificar_victoria(self.estado_juego):
                messagebox.showinfo(
                    "¡Ganaste!", "¡Felicidades! Has ganado el juego.")
            else:
                messagebox.showinfo(
                    "¡Perdiste!", "¡Has pisado una BOMBA! Mejor suerte la próxima.")

    def manejar_clic_derecho(self, fila: int, columna: int):
        """Maneja el evento de clic derecho en una celda"""
        marcar_celda(self.estado_juego, fila, columna)
        self.actualizar_interfaz()

    def reiniciar_juego(self):
        """Reinicia el juego"""
        reiniciar_juego(self.estado_juego)
        self.actualizar_interfaz()

    def guardar_estado(self):
        """Guarda el estado actual del juego en un archivo"""
        try:
            if self.estado_juego['juego_terminado']:
                messagebox.showwarning(
                    "Juego Terminado", "No se puede guardar un juego terminado.")
                return
            guardar_estado(self.estado_juego, ".")
            messagebox.showinfo("Guardado", "Juego guardado correctamente")
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo guardar el juego: {str(e)}")

    def cargar_estado(self):
        """Carga un estado guardado del juego"""

        resultado = cargar_estado(self.estado_juego, ".")

        if resultado:
            self.actualizar_interfaz()
            messagebox.showinfo("Cargado", "Juego cargado correctamente")
        else:
            messagebox.showinfo("Error", "No se pudo cargar el juego.")


def main():
    root = tk.Tk()
    InterfazBuscaminas(root)
    root.mainloop()


if __name__ == "__main__":
    main()
