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
    filas = len(tablero)
    columnas = len(tablero[0])

    tablero_og = []
    for fila in tablero:
        fila_nueva = []
        for i in fila:
            fila_nueva.append(i)
        tablero_og.append(fila_nueva)

    tablero_calculado = []
    for fila in tablero_og:
        fila_copia = []
        for celda in fila:
            fila_copia.append(celda)
        tablero_calculado.append(fila_copia)

    for i in range(filas):
        for j in range(columnas):
            if tablero_og[i][j] == -1:  # -1 es mina
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
            tablero_calculado[i][j] = contador

    return tablero_calculado
#Es un Inout, me costó


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    if type(filas) != int or filas <= 0:
        return {}
    if type(columnas) != int or columnas <= 0:
        return {}
    if minas <= 0 or minas >= filas * columnas:
        return {}
    
    tablero = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero)

    tablero_visible = []
    for i in range(filas):
        fila_visible = []
        for j in range(columnas):
            fila_visible.append(VACIO)
        tablero_visible.append(fila_visible)
    
    estado = {
        "filas": filas,
        "columnas": columnas,
        "minas": minas,
        "tablero": tablero,
        "juego_terminado": False,
        "tablero_visible": tablero_visible
    }

    if not estado_valido(estado):
        return {}
    return estado

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
    if estado == {}:
        return False
    if not estructura_y_tipos_validos(estado):
        return False
    
    contador = 0
    for fila in estado["tablero"]:
        for cell in fila:
            if cell == -1:
                contador += 1
    if contador != estado["minas"]:
        return False
    
    fin_de_juego = todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"]) or hay_bomba_visible(estado["tablero_visible"])
    
    if estado.get("juego_terminado") != fin_de_juego:
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
        tablero_basico.append(fila_basica)

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

def son_bombas_esperadas(estado: EstadoJuego) -> bool:
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
    filas = longitud(tablero)
    columnas = longitud(tablero[0])

    for i in range(filas):
        for j in range(columnas):
            cell = tablero[i][j]
            visible = tablero_visible[i][j]

            if cell != -1:  
                if visible != str(cell):
                    return False
            else:
                if visible not in [VACIO, BANDERA]:
                    return False
    return True

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    copia_estado = []
    for fila in estado["tablero_visible"]:
        fila_copia = []
        for cell in fila:
            fila_copia.append(cell)
        copia_estado.append(fila_copia)
    return copia_estado


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if estado_valido(estado):
        if fila >= 0:
            if fila < estado["filas"]:
                if columna >= 0:
                    if columna < estado["columnas"]:
                       if not estado["juego_terminado"]:
                           celda = estado["tablero_visible"][fila][columna]
                           if celda == VACIO:
                               estado["tablero_visible"][fila][columna] = BANDERA
                           elif celda == BANDERA:
                               estado["tablero_visible"][fila][columna] = VACIO
                    


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if estado_valido(estado):
       if not estado["juego_terminado"]:
           if estado["tablero_visible"][fila][columna] == VACIO:
               if estado["tablero"][fila][columna] == -1:
                   estado["juego_terminado"] = True
                   for i in range(estado["filas"]):
                       for j in range(estado["columnas"]):
                           if estado["tablero"][i][j] == -1:
                               estado["tablero_visible"][i][j] = BOMBA
               else:
                   descubiertas = []
                   por_descubrir = []
                   por_descubrir.append((fila, columna))
                   while len(por_descubrir) > 0:
                       posicion = por_descubrir.pop(0)
                       fila_actual = posicion[0]
                       columna_actual = posicion[1]

                       ya_descubierta = False

                       for par in descubiertas:
                           if par[0] == fila_actual and par[1] == columna_actual:
                                 ya_descubierta = True
                       if not ya_descubierta:
                           descubiertas.append((fila_actual, columna_actual))
                    
                           if estado["tablero_visible"][fila_actual][columna_actual] == VACIO:
                               val = estado["tablero"][fila_actual][columna_actual]
                               estado["tablero_visible"][fila_actual][columna_actual] = str(val)
                               if val == 0:
                                   i = fila_actual - 1
                                   while i <= fila_actual + 1:
                                       j = columna_actual - 1
                                       while j <= columna_actual + 1:
                                           if 0 <= i < estado["filas"] and 0 <= j < estado["columnas"]:
                                               if estado["tablero_visible"][i][j] == VACIO:
                                                   ya_descubierta_adyacente = False
                                                   for par in descubiertas:
                                                       if par[0] == i and par[1] == j:
                                                           ya_descubierta_adyacente = True
                                                   por_descubrir_todavia = False
                                                   for par in por_descubrir:
                                                       if par[0] == i and par[1] == j:
                                                           por_descubrir_todavia = True
                                                   if not ya_descubierta_adyacente and not por_descubrir_todavia:
                                                         por_descubrir.append((i, j))
                                           j += 1
                                       i += 1
                                   todas_descubiertas = True
                                   i = 0
                                   while i < estado["filas"]:
                                       j = 0
                                       while j < estado["columnas"]:
                                           if estado["tablero_visible"][i][j] == VACIO and estado["tablero"][i][j] != -1:
                                               todas_descubiertas = False
                                           j += 1
                                       i += 1
                                   if todas_descubiertas:
                                       estado["juego_terminado"] = True
            


def verificar_victoria(estado: EstadoJuego) -> bool:
    if not estado_valido(estado):
        return False
    
    tablero = estado["tablero"]
    tablero_visible = estado["tablero_visible"]

    i = 0
    for i in range(estado["filas"]):
        for j in range(estado["columnas"]):
            if tablero[i][j] != -1:
                if tablero_visible[i][j] == VACIO or tablero_visible[i][j] == BOMBA:
                    return False

    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    estado_filas = estado["filas"]
    estado_columnas = estado["columnas"]
    estado_minas = estado["minas"]

    estado["juego_terminado"] = False

    tablero_nuevo = []
    for i in range(estado_filas):
        fila_nueva = []
        for j in range(estado_columnas):
            fila_nueva.append(0)
        tablero_nuevo.append(fila_nueva)

    minas_colocadas = 0
    while minas_colocadas < estado_minas:
        filas = random.randint(0, estado_filas - 1)
        columnas = random.randint(0, estado_columnas - 1)
        if tablero_nuevo[filas][columnas] != -1:
            tablero_nuevo[filas][columnas] = -1
            minas_colocadas += 1
    
    for i in range(estado_filas):
        for j in range(estado_columnas):
            if tablero_nuevo[i][j] != -1:
                contador = 0
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x == 0 and y == 0:
                            continue
                        fila_vecina = i + x
                        columna_vecina = j + y
                        if 0 <= fila_vecina < estado_filas and 0 <= columna_vecina < estado_columnas:
                            if tablero_nuevo[fila_vecina][columna_vecina] == -1:
                                contador += 1
                tablero_nuevo[i][j] = contador
    estado["tablero"] = tablero_nuevo
    tablero_visible_nuevo = []
    for i in range(estado_filas):
        fila_visible_nueva = []
        for j in range(estado_columnas):
            fila_visible_nueva.append(VACIO)
        tablero_visible_nuevo.append(fila_visible_nueva)
    estado["tablero_visible"] = tablero_visible_nuevo


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    if (not estado["juego_terminado"]) and os.path.exists(ruta_directorio):
        estado_filas = estado["filas"]
        estado_columnas = estado["columnas"]
        tablero_path = os.path.join(ruta_directorio, "tablero.txt")
        tablero_file = open(tablero_path, "w")
        for i in range(estado_filas):
            valores = []
            for j in range(estado_columnas):
                val = estado["tablero"][i][j]
                valores.append(str(val))
            linea = ",".join(valores)
            tablero_file.write(linea + "\n")
        tablero_file.close()

        tablero_visible_path = os.path.join(ruta_directorio, "tablero_visible.txt")
        tablero_visible_file = open(tablero_visible_path, "w")
        for i in range(estado_filas):
            valores = []
            for j in range(estado_columnas):
                val = estado["tablero_visible"][i][j]
                if val == BANDERA:
                    valores.append("*")
                elif val == VACIO:
                    valores.append("?")
                else:
                    valores.append(val)
            linea = ",".join(valores)
            tablero_visible_file.write(linea + "\n")    
        tablero_visible_file.close()


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    if not existe_archivo(ruta_directorio, "tablero.txt") or not existe_archivo(ruta_directorio, "tablero_visible.txt"):
        return False

    # Cargar líneas de tablero.txt
    tablero_path = os.path.join(ruta_directorio, "tablero.txt")
    tablero_lines = []
    with open(tablero_path, "r") as tablero_file:
        for line in tablero_file:
            line = line.strip()
            if longitud(line) > 0:
                tablero_lines.append(line)

    # Cargar líneas de tablero_visible.txt
    tablero_visible_path = os.path.join(ruta_directorio, "tablero_visible.txt")
    tablero_visible_lines = []
    with open(tablero_visible_path, "r") as tablero_visible_file:
        for line in tablero_visible_file:
            line = line.strip()
            if longitud(line) > 0:
                tablero_visible_lines.append(line)

    filas = longitud(tablero_lines)
    if filas == 0 or longitud(tablero_visible_lines) != filas:
        return False

    columnas = longitud(tablero_lines[0].split(","))
    for line in tablero_lines:
        if longitud(line.split(",")) != columnas:
            return False
    for line in tablero_visible_lines:
        if longitud(line.split(",")) != columnas:
            return False

    # Reconstruir tablero
    tablero = []
    minas_cantidad = 0
    numeros_string = ["-1", "0", "1", "2", "3", "4", "5", "6", "7", "8"]
    for i in range(filas):
        fila_valores = tablero_lines[i].split(",")
        fila = []
        for val in fila_valores:
            if val not in numeros_string:
                return False
            if val == "-1":
                fila.append(-1)
                minas_cantidad += 1
            else:
                fila.append(int(val))
        tablero.append(fila)

    if minas_cantidad == 0:
        return False

    # Verificar consistencia de las pistas numéricas
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] != -1:
                minas_adyacentes = 0
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x == 0 and y == 0:
                            continue
                        xx = i + x
                        yy = j + y
                        if 0 <= xx < filas and 0 <= yy < columnas:
                            if tablero[xx][yy] == -1:
                                minas_adyacentes += 1
                if tablero[i][j] != minas_adyacentes:
                    return False
    tablero_visible = []
    for i in range(filas):
        fila_valores = tablero_visible_lines[i].split(",")
        fila_visible = []
        for j in range(columnas):
            val = fila_valores[j]
            if val == "*":
                fila_visible.append(BANDERA)
            elif val == "?":
                fila_visible.append(VACIO)
            elif val in numeros_string:
                if int(val) != tablero[i][j]:
                    return False
                fila_visible.append(int(val))
            else:
                return False
        tablero_visible.append(fila_visible)
    estado["filas"] = filas
    estado["columnas"] = columnas
    estado["minas"] = minas_cantidad
    estado["tablero"] = tablero
    estado["tablero_visible"] = tablero_visible
    estado["juego_terminado"] = False

    return estado_valido(estado)