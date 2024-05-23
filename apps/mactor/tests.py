from django.test import TestCase


# Clase auxiliar para la generacion de matrices, se asigna una posicion a un respectivo valor
class ValorPosicion:
    def __init__(self, posicion, valor, descripcion):
        self.posicion = posicion
        self.valor = valor
        self.descripcion = descripcion


# Devuelve el significado de cada valor de la matriz mid
def obtener_descripcion_mid(valor):

    descripcion = ""

    if valor == 0:
        descripcion = "Sin influencia"
    elif valor == 1:
        descripcion = "Procesos"
    elif valor == 2:
        descripcion = "Proyectos"
    elif valor == 3:
        descripcion = "Misión"
    elif valor == 4:
        descripcion = "Existencia"

    return descripcion


# Devuelve la descripcion de los valores de las matrices mao
def obtener_descripcion_mao(valor):

    if valor == 0:
        descripcion = "Neutro"
    elif valor > 0:
        descripcion = "Acuerdo"
    else:
        descripcion = "Desacuerdo"

    return descripcion
