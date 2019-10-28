import sys,time, locale, ast, re, os
from PyQt5.uic import loadUi
from PyQt5 import QtCore, Qt, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constantes import *
from Verificar import verificar

class Login(QMainWindow):
    
    switch_Inventario = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Login, self).__init__()
        loadUi('UI/Login.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        self.setContentsMargins(0, 0, 0, 0)
        self.ImagenLabel.setPixmap(QtGui.QPixmap(IMAGEN_RANDOM))
        self.label_3.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label_2.setAttribute(Qt.WA_TranslucentBackground, True)

        ##################COMBOBOX##################

        self.comboboxTipoCuenta.addItems(TIPO_CUENTA)

        ##################BOTONES##################

        self.botonIngresar.clicked.connect(self.abrirInventario)

    ##################FUNCIONES##################
    def abrirInventario(self):
        #self.switch_Inventario.emit()
        Contra_ing = self.lineEditContrasena.text()
        Usuario_ing = self.lineEditUsuario.text()
        Tipo_cuenta = True if (self.comboboxTipoCuenta.currentText() == ADMINISTRADOR) else False
        if verificar(Usuario_ing, Contra_ing, Tipo_cuenta):
           self.switch_Inventario.emit()
        else:
            QMessageBox.information(self, "Mensaje", "Contraseña incorrecta", QMessageBox.Ok)
        

