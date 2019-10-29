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
    
    sigEditar = QtCore.pyqtSignal()
    sigAceptar = QtCore.pyqtSignal()
    sigEliminarTodo = QtCore.pyqtSignal()
    sigEliminar = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super(UI_Compra, self).__init__()
        loadUi('UI/templates/Compra.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        # -----------------TABLA-----------------
        self.tablaProductos
        self.tablaProductos.setColumnCount(6)
        nombreColumnas = ("Referencia","Descripcion","Cantidad","Porcentaje","Valor Unitario","Valor Total")
        self.tablaProductos.setHorizontalHeaderLabels(nombreColumnas)
        self.tablaProductos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaProductos.verticalHeader().setVisible(False)
        self.tablaProductos.setAlternatingRowColors(True)
        self.tablaProductos.setDragDropOverwriteMode(False)
        self.tablaProductos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # -----------------Ancho columnas-----------------
        for indice, ancho in enumerate((168, 400, 100, 100, 150, 150), start=0):
            self.tablaProductos.setColumnWidth(indice, ancho)
        self.show()
    #-----------------sets-----------------
    def getLEIdProducto(self):
        return self.lineEditProducto.text()
    def getLEDescripcion(self):
        return self.lineEditDescripcion.text()
    def getLEValorUnitario(self):
        return self.lineEditValorUnitario.text()
    def getLEPorcentaje(self):
        return self.lineEditPorcentaje.text()
    def getCBDescripcion(self):
        return self.comboBoxDescripcion.currentText()
    def getSBcantidad(self):
        return self.spinBoxCantidad.value()
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
    # -----------------Upload-----------------
    def uploadTabla(self,tmp,row):
        self.tableWidget.setRowCount(row)
    
        self.tableWidget.setItem(row, 0, QTableWidgetItem(  tmp[0]  )) #REFERENCIA
        self.tableWidget.setItem(row, 1, QTableWidgetItem(  tmp[1]  )) #DESCRIPCION
        self.tableWidget.setItem(row, 2, QTableWidgetItem(  tmp[2]  )) #CANTIDAD
        self.tableWidget.setItem(row, 3, QTableWidgetItem(  tmp[3]  )) #PORCENTAJE
        self.tableWidget.setItem(row, 4, QTableWidgetItem(  tmp[4]  )) #VALOR UNITARIO
        self.tableWidget.setItem(row, 5, QTableWidgetItem(  tmp[5]  )) #VALOR TOTAL
    
    def editar(self):
        self.sigEditar.emit()
    def aceptar(self):
        self.sigAceptar.emit()   
    def eliminar(self):
        self.sigEliminar.emit()
    def eliminarTodo(self):
        self.sigEliminarTodo.emit()