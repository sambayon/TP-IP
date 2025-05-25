import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]
def longitud(lista: list[Any]) -> int:
    counter = 0
    for i in lista:
        counter += 1
    return counter
def esMatriz(lista: list[list[Any]]) -> bool:
    if len(lista) == 0:
        return False
    longitud_fila = longitud(lista[0])
    for fila in lista:
        if longitud(fila) != longitud_fila:
            return False
    return True
        
def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(0)
        matriz.append(fila)
    posiciones = []
    for i in range(filas):
        for j in range(columnas):
            posiciones.append((i, j))
    posiciones_minas = random.sample(posiciones, minas)

    for i, j in posiciones_minas:
        matriz[i][j] = -1
    return matriz
def pertenece(a: int, lista: list[Any]) -> bool:
    for i in lista:
        if i == a:
            return True
    return False

def calcular_numeros(tablero: list[list[int]]) -> None:
    filas = longitud(tablero)
    columnas = longitud(tablero[0])

    tablero_og = []
    for fila in tablero:
        fila_nueva = []
        for i in fila:
            fila_nueva.append(i)
        tablero_og.append(fila_nueva)
        

    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == -1:
                continue
            contador = 0
            marcas = [-1, 0, 1]
            for x in marcas:
                for y in marcas:
                    if x == 0 and y == 0:
                        continue
                    fila_vecina = i + x
                    columna_vecina = j + y
                    if 0 <= fila_vecina < filas and 0 <= columna_vecina < columnas:
                        if tablero_og[fila_vecina][columna_vecina] == -1:
                            contador += 1    
            tablero[i][j] = contador
#Es un Inout, me costó


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    return {}


def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    return [[]]


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def verificar_victoria(estado: EstadoJuego) -> bool:
    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False