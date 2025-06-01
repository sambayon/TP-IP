import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]
 # Tipo para el tablero visible
def longitud(lista: list[Any]) -> int:
    counter = 0
    for i in lista:
        counter += 1
    return counter
def esMatriz(lista: list[list[Any]]) -> bool:
    if longitud(lista) == 0:
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

def estructura_y_tipos_validos(estado: EstadoJuego) -> bool:
    claves = ["filas", "columnas", "minas", "tablero", "juego_terminado", "tablero_visible"]

    for clave in claves:
        if clave not in estado:
            return False
    
    if longitud(list(estado.keys())) != 6:
        return False
    
    estado_filas = estado["filas"]
    if type(estado_filas) != int or estado_filas <= 0:
        return False
    
    estado_columnas = estado["columnas"]
    if type(estado_columnas) != int or estado_columnas <= 0:
        return False
    
    estado_minas = estado["minas"]
    if type(estado_minas) != int or estado_minas <= 0 or estado_minas >= estado_columnas * estado_filas:
        return False
    

    estado_juego_terminado = estado["juego_terminado"]

    if type(estado_juego_terminado) != bool :
        return False
    
    estado_tablero = estado["tablero"]
    estado_tablero_visible = estado["tablero_visible"]

    if not esMatriz(estado_tablero):
        return False
    if longitud(estado_tablero) != estado_filas or longitud(estado_tablero[0]) != estado_columnas:
        return False
    for fila in estado_tablero:
        for cell in fila:
            if type(cell) != int or cell < -1 or cell > 8:
                return False
            
    if not esMatriz(estado_tablero_visible):
        return False
    if longitud(estado_tablero_visible) != estado_filas or longitud(estado_tablero_visible[0]) != estado_columnas:
        return False
    
    for fila in estado_tablero_visible:
        for cell in fila:
            if cell not in [VACIO, BOMBA, BANDERA]:
                if type(cell) != str:
                    return False
                if cell not in [str(i) for i in range(9)]:
                    return False
    return True

def son_matriz_y_misma_dimension(t1: list[list[Any]], t2: list[list[Any]]) -> bool:
    if not esMatriz(t1) or not esMatriz(t2):
        return False
    if longitud(t1) != longitud(t2):
        return False
    if longitud(t1[0]) != longitud(t2[0]):
        return False

    return True

def estado_valido(estado: EstadoJuego) -> bool:
    if not estructura_y_tipos_validos(estado):
        return False
    contador = 0
    for fila in estado["tablero"]:
        for cell in fila:
            if cell == -1:
                contador += 1
    if contador != estado["minas"]:
        return False
    if not (todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]) or hay_bomba_visible(estado["tablero_visible"])): 
        return False
    if not estado.get("juego terminado") != (todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]) or hay_bomba_visible(estado["tablero_visible"])):
        return False
    if not son_bombas_esperadas(estado):
        return False
    if not visibles_esperadas(estado):
        return False
    if not tablero_esperado(estado):
        return False
    return True

def tablero_esperado(estado: EstadoJuego) -> bool:
    filas = longitud(estado["tablero"])
    columnas = longitud(estado["tablero"][0])

    tablero_basico = []
    for i in range(filas):
        fila_basica = []
        for j in range(columnas):
            if estado["tablero"][i][j] == -1:
                fila_basica.append(-1)
            else:
                fila_basica.append(0)
    tablero_calculado = calcular_numeros(tablero_basico)

    for i in range(filas):
        for j in range(columnas):
            if estado["tablero"][i][j] != tablero_calculado[i][j]:
                return False
    return True
def visibles_esperadas(estado: EstadoJuego) -> bool:
    filas = longitud(estado["tablero"])
    columnas = longitud(estado["tablero"][0])
    
    for i in range(filas):
        for j in range(columnas):
            valor_visible = estado["tablero_visible"][i][j]
            valor_tablero = estado["tablero"][i][j]

            if valor_visible == BOMBA and valor_tablero != -1:
                return False
            elif valor_visible not in [VACIO, BANDERA]:
                if valor_visible != str(valor_tablero):
                    return False
    return True

def son_bombas_esperadas(estado: EstadoJuego) -> int:
    for i in range(estado["filas"]):
        for j in range(estado["columnas"]):
            if estado["tablero_visible"][i][j] == BOMBA and estado["tablero"][i][j] != -1:
                return False
    return True

def hay_bomba_visible(tablero_visible: list[list[str]]) -> bool:
    for fila in tablero_visible:
        for cell in fila:
            if cell == BOMBA:
                return True
    return False

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    return 1

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