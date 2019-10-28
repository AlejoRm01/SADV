import sys,time, locale, ast, re, os
from Conexion import obtenerProductos, verificarCodigos, enviarCompra, enviarCodigos
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constantes import *

"""
Clase Compra
En esta clase se realiza  toda la actividad de realizar una compra, confirmar comprar
confirmar envio de correos y confirmar la genereacion de facturas.
"""
class Compra(QMainWindow):
    
    switch_Inventario = QtCore.pyqtSignal()
    switch_Venta = QtCore.pyqtSignal()
    switch_Usuario = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(Compra, self).__init__()
        loadUi('UI/Compra.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        self.comboBoxDescripcion.addItems(obtenerProductos())

        ##################BOTONES##################

        self.botonInventario.clicked.connect(self.abrirInventario)
        self.botonVentas.clicked.connect(self.abrirVentas)
        self.botonIngresar.clicked.connect(self.ingresarCodigos)
        self.botonEditar.clicked.connect(self.editar)
        self.botonEliminar.clicked.connect(self.eliminar)
        self.botonEliminarTodo.clicked.connect(self.eliminarTodo)
        self.botonAceptar.clicked.connect(self.Aceptar)
        self.Usuarios.clicked.connect(self.abrirUsuarios)

    ##################FUNCIONES##################

    def ver(self):
        if self.Admin:
            self.Usuarios.setEnabled(True)
        else:
            self.Usuarios.setEnabled(False)

    def ingresarCodigos(self):
        codigos = self.lineEditCodigos.text()
        self.lineEditCodigos.clear()
        codigos = codigos.split(" ")
        codigos = [item for item in codigos if item]
        self.listWidget.addItems(codigos)

    def Aceptar(self):

        repetido = False
        locale.setlocale(locale.LC_ALL, '')
        factura = self.lineEditFactura.text()
        descripcion = self.comboBoxDescripcion.currentText()
        codigos = []
        for index in range(self.listWidget.count()):
            codigos.append(self.listWidget.item(index).text())
        socio = self.lineEditSocio.text()
        moneda = self.lineEdit_Moneda.text()
        tasa = self.lineEditTasa.text()
        fecha = self.calendarWidget.selectedDate().toString()

        aux = []
        aux = self.verificarRepetido(codigos)
        
        if(len(aux)>= 3):
            QMessageBox.information(self, "Mensaje", "Codigos Repetidos", QMessageBox.Ok)
            self.listWidget.clear()
            self.listWidget.addItems(aux)
            repetido = True
        else:
            repetido = False
        
        aux = []
        
        if (codigos != aux and repetido == False):

            verificacion = []
            verificacion = verificarCodigos(codigos)

            if (verificacion[0] == 'False'):
                try:
                    valor = float(moneda) * float(tasa)
                    valor = str(locale.currency(valor, grouping=True))
                    enviarCompra(factura, descripcion, socio, moneda, tasa, fecha, valor, codigos)
                    enviarCodigos(codigos, descripcion)
                    self.listWidget.clear(), self.lineEditSocio.clear(), self.lineEdit_Moneda.clear(), self.lineEditTasa.clear(), self.lineEditFactura.clear()

                    QMessageBox.information(self, "Mensaje", "Proceso terminado", QMessageBox.Ok)
                except:
                    QMessageBox.information(self, "Mensaje", "Proceso interrumpido, corriga los valores ingresados",
                                            QMessageBox.Ok)
            else:
                self.listWidget.clear()
                self.listWidget.addItems(verificacion)
                QMessageBox.information(self, "Mensaje", "Algunos codigos estan repetidos", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Mensaje", "Proceso interrumpido, Ingrese codigos", QMessageBox.Ok)

    def verificarRepetido(self, valores):
        repetido = ['Codigos repetidos','No se agregaron codigos']
        unico = []
        for x in valores:
            if x not in unico:
                unico.append(x)
            else:
                if x not in repetido:
                    repetido.append(x)
        if(len(repetido)>= 3):
            return repetido
        else:
            return ['']
    
    def editar(self):
        self.row = self.listWidget.currentRow()
        self.listWidget.takeItem(self.row)
        self.listWidget.insertItem(self.row, self.lineEditCodigos.text())

    def eliminar(self):
        self.row = self.listWidget.currentRow()
        self.listWidget.takeItem(self.row)

    def eliminarTodo(self):
        self.listWidget.clear()

    def abrirInventario(self):
        self.switch_Inventario.emit()
    def abrirVentas(self):
        self.switch_Venta.emit()
    def abrirUsuarios(self):
        self.switch_Usuario.emit()