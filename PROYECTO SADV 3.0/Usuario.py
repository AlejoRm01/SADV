import sys,time, locale, ast, re, os
from Conexion import borrarUs, agregarUs, obtenerUsuarios
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constantes import *


class Usuario(QMainWindow):
    
    switch_Inventario = QtCore.pyqtSignal()
    switch_Compra = QtCore.pyqtSignal()
    switch_Venta = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(Usuario, self).__init__()
        loadUi('UI/Usuario.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        self.comboBoxTipoCuenta.addItems(TIPO_CUENTA)
        us = obtenerUsuarios()
        self.comboBoxUsuarios.addItems(us)
        ##################BOTONES##################

        self.botonInventario.clicked.connect(self.abrirInventario)
        self.botonCompras.clicked.connect(self.abrirCompras)
        self.botonVentas.clicked.connect(self.abrirVentas)
        self.botonVentasAceptarE.clicked.connect(self.borrarUsuario)
        self.botonVentasAceptarA.clicked.connect(self.aggUsuario)

        ##################FUNCIONES##################
    def ver(self):
        if self.Admin:
            self.Usuarios.setEnabled(True)
        else:
            self.Usuarios.setEnabled(False)

    def borrarUsuario(self):
        usuario = self.comboBoxUsuarios.currentText()
        buttonReply = QMessageBox.question(self, 'Eliminar', "¿Esta seguro que desea eliminar este usuario?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            try:
                borrarUs(usuario)
                QMessageBox.question(self, 'Eliminar', "Proceso completado con exito", QMessageBox.Ok)
            except:
                QMessageBox.question(self, 'Eliminar', "No fue posible eliminar esta cuenta", QMessageBox.Ok)

    def aggUsuario(self):
        usu = self.lineEditUsuario.text()
        con = self.lineEditContrasena.text()
        tipo = True if (self.comboBoxTipoCuenta.currentText() == "Administrador/a") else False
        agregarUs(usu, con, tipo)
    
    def abrirInventario(self):
	    self.switch_Inventario.emit()
    def abrirCompras(self):
        self.switch_Compra.emit()
    def abrirVentas(self):
        self.switch_Venta.emit()