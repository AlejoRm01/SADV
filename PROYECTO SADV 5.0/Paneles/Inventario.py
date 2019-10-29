import sys
from Utiles.Conexion import getInventario
from PyQt5 import QtCore, QtWidgets
from UI.UI_inventario import *

class Inventario():
    
    def __init__(self):
        
        inventario = getInventario()
        self.UIi = UI_Inventario(inventario)
    def show(self):
        self.UIi.show()
