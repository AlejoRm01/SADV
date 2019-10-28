import sys,time, locale, ast, re, os
from Conexion import obtenerInventario
from PyQt5 import QtCore, Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Constantes import *

class Inventario(QMainWindow):
    
    switch_Compra = QtCore.pyqtSignal()
    switch_Venta = QtCore.pyqtSignal()
    switch_Usuario = QtCore.pyqtSignal()
    def __init__(self):
        super(Inventario,self).__init__()
        loadUi('UI/Inventario.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        ##################TABLA##################
        # Numero de columnas y nombre de estas
        self.tablaInventario.setColumnCount(6)
        nombreColumnas = ("Cantidad", "Denominacion", "Acumulado", "Descripcion", "Stock Minimo", "Estado")
        self.tablaInventario.setHorizontalHeaderLabels(nombreColumnas)
        self.tablaInventario.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaInventario.verticalHeader().setVisible(False)
        
        self.tablaInventario.setAlternatingRowColors(True)
        self.tablaInventario.setDragDropOverwriteMode(False)
        self.tablaInventario.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Ancho columnas
        for indice, ancho in enumerate((70, 90, 87, 500, 90, 150), start=0):
            self.tablaInventario.setColumnWidth(indice, ancho)

        inventario = obtenerInventario()
        row = -1
        self.tablaInventario.setRowCount(row + 1)
        for dato in inventario:
            row += 1
            self.tablaInventario.setRowCount(row + 1)

            self.tablaInventario.setItem(row, 0, QTableWidgetItem(str(dato[0])))
            self.tablaInventario.setItem(row, 1, QTableWidgetItem(str(dato[1])))
            self.tablaInventario.setItem(row, 2, QTableWidgetItem(str(dato[2])))
            self.tablaInventario.setItem(row, 3, QTableWidgetItem(str(dato[3])))
            self.tablaInventario.setItem(row, 4, QTableWidgetItem(str(dato[4])))
            self.tablaInventario.setItem(row, 5, QTableWidgetItem(str(dato[5])))

        ##################BOTONES##################

        self.botonCompras.clicked.connect(self.abrirCompras)
        self.botonVentas.clicked.connect(self.abrirVentas)
        self.Usuarios.clicked.connect(self.abrirUsuarios)

        ##################FUNCIONES##################

    def ver(self):
        if self.Admin:
            self.Usuarios.setEnabled(True)
        else:
            self.Usuarios.setEnabled(False)

    
    def abrirCompras(self):
        self.switch_Compra.emit()
    def abrirVentas(self):
        self.switch_Venta.emit()
    def abrirUsuarios(self):
        self.switch_Usuario.emit()