from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constantes import *

class UI_Compra(QMainWindow):
    
    switch_Inventario = QtCore.pyqtSignal()
    switch_Venta = QtCore.pyqtSignal()
    switch_Usuario = QtCore.pyqtSignal()
    

    def __init__(self, productos,parent=None):
        super(UI_Compra, self).__init__()
        loadUi('UI/templates/Compra.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        self.a.addItems(['Alejadro','12312','2312323','213123123'])
    #-----------------sets-----------------
    def setLEfecha(self,tmp):
        return self.lineEditFecha.setText(tmp)
    #-----------------gets-----------------        
    
    #-----------------throwMsg-----------------
    def throwMsgProcesoTerminado(self):
        QMessageBox.information(self, "Mensaje", "Proceso terminado", QMessageBox.Ok)
    def throwMsgErrorProceso(self):
        QMessageBox.information(self, "Mensaje", "Proceso interrumpido, corriga los valores ingresados",
                                            QMessageBox.Ok)
    def throwMsgErrorRepetido(self):
        QMessageBox.information(self, "Mensaje", "Algunos codigos estan repetidos", QMessageBox.Ok)
    def throwMsgErrorIngreso(self):
        QMessageBox.information(self, "Mensaje", "Proceso interrumpido, Ingrese codigos", QMessageBox.Ok)
    #-----------------takes-----------------
   
    #-----------------inserts-----------------
    
    # -----------------Triggers-----------------
    def abrirInventario(self):
        self.switch_Inventario.emit()
        self.close()
    def abrirVentas(self):
        self.switch_Venta.emit()
        self.close()
    def ingresarCodigos(self):
        self.sigIngresarCodigos.emit()
    
    def editar(self):
        self.sigEditar.emit()
    def aceptar(self):
        self.sigAceptar.emit()   
    def eliminar(self):
        self.sigEliminar.emit()
    def eliminarTodo(self):
        self.sigEliminarTodo.emit()