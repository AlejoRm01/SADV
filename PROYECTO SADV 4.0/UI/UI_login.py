from PyQt5.uic import loadUi
from PyQt5 import QtCore, Qt, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constantes import *

class UI_login(QMainWindow):
    
    switch_Inventario = QtCore.pyqtSignal()
    
    sigValidar = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(UI_login, self).__init__()
        loadUi('UI/templates/Login.ui', self)
        
        self.setWindowIcon(QIcon(ICONO))
        self.setContentsMargins(0, 0, 0, 0)
        self.ImagenLabel.setPixmap(QtGui.QPixmap(IMAGEN_RANDOM))
        self.label_3.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)
        self.label_2.setAttribute(Qt.WA_TranslucentBackground, True)
       
        # -----------------COMBOBOX-----------------
        self.comboboxTipoCuenta.addItems(TIPO_CUENTA)

        # -----------------Trigger-----------------
        self.botonIngresar.clicked.connect(self.validar)
    
    def validar(self):
        self.sigValidar.emit()
    def abrirInventario(self):
        self.switch_Inventario.emit()
    # -----------------gets-----------------
    def getUsuario(self):
        return self.lineEditUsuario.text()
    def getContrasena(self):
        return self.lineEditContrasena.text()
    def getTipoCuenta(self):
        return self.comboboxTipoCuenta.currentText()
    # -----------------throwMsg-----------------
    def throwMsgErrorProceso(self):
        QMessageBox.information(self, "Mensaje", "Contraseña incorrecta", QMessageBox.Ok)