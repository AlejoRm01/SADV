import sys,time, locale, ast, re, os
from Conexion import verificarCodigos, enviarCodigos, enviarCompra, obtenerCodigosParaVender, enviarVenta, obtenerProductos
from Factura import fecha, generarFactura, hacerCodigos
from EnviarCorreo import mandarCorreoFactura, mandarCorreoHtml
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constantes import *

class Venta(QMainWindow):
    
    switch_Inventario = QtCore.pyqtSignal()
    switch_Compra = QtCore.pyqtSignal()
    switch_Usuario = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(Venta, self).__init__()
        loadUi('UI/Venta.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        self.comboBoxDescripcion.addItems(obtenerProductos())
        self.lineEditDescuento.setText('0')
        self.informacionCliente = []
        self.venta = []
        self.arrAux = []
        self.total = 0
        self.subtotal = 0
        self. descuento = 0
        ##################BOTONES##################

        self.botonInventario.clicked.connect(self.abrirInventario)
        self.botonCompras.clicked.connect(self.abrirCompras)
        self.botonVentasAceptar.clicked.connect(self.Aceptar)
        self.botonEliminar.clicked.connect(self.eliminar)
        self.botonEliminarTodo.clicked.connect(self.eliminarTodo)
        self.botonContinuarVenta.clicked.connect(self.abrirContinuarVenta)
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
    def abrirCompras(self):
        self.switch_Compra.emit()
    def abrirUsuarios(self):
        self.switch_Usuario.emit()
    
    def abrirContinuarVenta(self):
        cliente = self.lineEditCliente.text()
        identificacion = self.lineEditIdentificacion.text()
        celular = self.lineEditCelular.text()
        telefono = self.lineEditTelefono.text()
        direccion = self.lineEditDireccion.text()
        departamento = self.lineEditDepartamento.text()
        correo = self.lineEditEMAIL.text()
        descuento = self.lineEditDescuento.text()
        tipoPago = self.lineEditTipoPago.text()
        factura = self.lineEditFactura.text()

        # FECHA, NUMERO FACTURA, CLIENTE, IDENTIFICACION, CELULAR, DEPARTAMENTO, TELEFONO, DIRECCION, CORREO, DESCUENTO, TPAGO, VALOR DESCUENTO, TOTAL, SUBTOTAL
        self.informacionCliente.append(
            [fecha(), factura, cliente, identificacion, celular, departamento, telefono, direccion, correo, descuento,
             tipoPago, self.descuento, self.total, self.subtotal])

        if (identificacion != "" and correo != ""):
            otraVentana = VentanaVerificacionVenta(self)
            otraVentana.Admin = self.Admin
            self.hide()
            otraVentana.show()

            us = self.informacionCliente

            row = -1
            rtc = otraVentana.TablaClientes
            rtc.setRowCount(row + 1)

            for d in us:
                row += 1
                rtc.setRowCount(row + 1)

                rtc.setItem(row, 0, QTableWidgetItem(d[2]))
                rtc.setItem(row, 1, QTableWidgetItem(d[3]))
                rtc.setItem(row, 2, QTableWidgetItem(d[4]))

            row = -1
            rtc = otraVentana.TablaClientes_2
            rtc.setRowCount(row + 1)
            for d in us:
                row += 1
                rtc.setRowCount(row + 1)

                rtc.setItem(row, 0, QTableWidgetItem(d[6]))
                rtc.setItem(row, 1, QTableWidgetItem(d[7]))
                rtc.setItem(row, 2, QTableWidgetItem(d[5]))

            row = -1
            rtc = otraVentana.TablaClientes_3
            rtc.setRowCount(row + 1)
            for d in us:
                row += 1
                rtc.setRowCount(row + 1)

                rtc.setItem(row, 0, QTableWidgetItem(d[8]))
                rtc.setItem(row, 1, QTableWidgetItem(d[10]))
                rtc.setItem(row, 2, QTableWidgetItem(d[0]))

            rtc = otraVentana.ListaCodigos
            # producto, cantidad, precio
            venta = []
            for i in self.venta:
                codigos = obtenerCodigosParaVender(i[0], i[1])
                venta.append([i[0], codigos])
                rtc.addItem(i[0])
                rtc.addItems(codigos)

            rtc = otraVentana.listWidgetV
            for i in self.venta:
                rtc.addItem(str(i))

            rtc = otraVentana.listWidgetC
            for i in self.informacionCliente[0]:
                rtc.addItem(str(i))

        else:
            QMessageBox.information(self, "Mensaje", "Proceso interrumpido,  Ingrese una identificacion y un correo",
                                    QMessageBox.Ok)



class VentanaVerificacionVenta(QMainWindow):
    Admin = False

    def __init__(self, parent=None):
        super(VentanaVerificacionVenta, self).__init__(parent)
        loadUi('UI/ContinuarVentas.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        self.informacionCliente = []
        self.informacionVenta = []
        
        # -----------------TablaClientes1-------------------------
        self.TablaClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TablaClientes.setTextElideMode(Qt.ElideRight)
        self.TablaClientes.verticalHeader().setVisible(False)
        self.TablaClientes.setColumnCount(3)
        nomCol1 = ("Cliente", "Identificacion", "Celular")
        self.TablaClientes.setHorizontalHeaderLabels(nomCol1)
        # Ancho columnas
        for indice, ancho in enumerate((200, 160, 159), start=0):
            self.TablaClientes.setColumnWidth(indice, ancho)

        # -----------------TablaClientes2-------------------------
        self.TablaClientes_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TablaClientes_2.setTextElideMode(Qt.ElideRight)
        self.TablaClientes_2.verticalHeader().setVisible(False)
        self.TablaClientes_2.setColumnCount(3)
        nomCol1 = ("Telefono", "Direccion", "Departamento")
        self.TablaClientes_2.setHorizontalHeaderLabels(nomCol1)

        # Ancho columnas
        for indice, ancho in enumerate((200, 160, 159), start=0):
            self.TablaClientes_2.setColumnWidth(indice, ancho)

        # -----------------TablaClientes3-------------------------
        self.TablaClientes_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TablaClientes_3.setTextElideMode(Qt.ElideRight)
        self.TablaClientes_3.verticalHeader().setVisible(False)
        self.TablaClientes_3.setColumnCount(3)
        nomCol1 = ("E-mail", "Tipo de pago", "Fecha")
        self.TablaClientes_3.setHorizontalHeaderLabels(nomCol1)

        # Ancho columnas
        for indice, ancho in enumerate((200, 160, 159), start=0):
            self.TablaClientes_3.setColumnWidth(indice, ancho)

        # -----------------ListaCodigos-------------------------

        ##################BOTONES##################

        self.botonRegresarVentas.clicked.connect(self.abrirVentas)
        self.BotonRegresar.clicked.connect(self.abrirVentas)
        self.botonFinalizar.clicked.connect(self.finalizarVenta)
        self.BotonFactura.clicked.connect(self.hacerFactura)
        self.BotonCorreo.clicked.connect(self.mandarCorreo)
        self.BotonFacturaCorreo.clicked.connect(self.mandarFacturaCorreo)

        ##################FUNCIONES##################

    def ver(self):
        if self.Admin:
            self.Usuarios.setEnabled(True)
        else:
            self.Usuarios.setEnabled(False)

    def abrirVentas(self):
        self.hide()
        otraVentana = Venta(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def finalizarVenta(self):

        for index in range(self.listWidgetC.count()):
            self.informacionCliente.append(self.listWidgetC.item(index).text())

        for index in range(self.listWidgetV.count()):
            self.informacionVenta.append(self.listWidgetV.item(index).text())

        patt = re.compile(r"\[.*\]")
        self.informacionVenta = [ast.literal_eval(e) if isinstance(e, str) and patt.fullmatch(e) else e for e in
                                 self.informacionVenta]

        try:
            self.botonFinalizar.setEnabled(False)
            self.botonRegresarVentas.setEnabled(False)
            self.BotonRegresar.setEnabled(True)
            self.BotonFactura.setEnabled(True)
            self.BotonCorreo.setEnabled(True)

            QMessageBox.information(self, "Mensaje", "Proceso Terminado", QMessageBox.Ok)
            enviarVenta(self.informacionCliente, self.informacionVenta)
        except:
            QMessageBox.information(self, "Mensaje", "Proceso interrumpido, No se pudo realizar la venta",
                                    QMessageBox.Ok)

    def hacerFactura(self):
        pathNombre = self.informacionCliente[3]
        buttonReply = QMessageBox.question(self, 'Factura', "Agregar Terminos y Condiciones",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            # FECHA, NUMERO FACTURA, CLIENTE, IDENTIFICACION, CELULAR, DEPARTAMENTO, TELEFONO, DIRECCION, CORREO, DESCUENTO, TPAGO, VALOR DESCUENTO
            generarFactura(pathNombre, self.informacionVenta, self.informacionCliente, True)
        else:
            generarFactura(pathNombre, self.informacionVenta, self.informacionCliente, False)
        self.BotonFactura.setEnabled(False)
        self.BotonFacturaCorreo.setEnabled(True)

    def mandarCorreo(self):
        codigos = []
        for index in range(self.ListaCodigos.count()):
            codigos.append(self.ListaCodigos.item(index).text())
        hacerCodigos(codigos)
        try:
            QMessageBox.question(self, 'Mensaje', "Proceso terminado", QMessageBox.Ok)
            mandarCorreoHtml(self.informacionCliente[8])
        except:
            QMessageBox.question(self, 'Mensaje', "Error verifique correo ingresado", QMessageBox.Ok)

    def mandarFacturaCorreo(self):
        codigos = []
        for index in range(self.ListaCodigos.count()):
            codigos.append(self.ListaCodigos.item(index).text())
        hacerCodigos(codigos)
        pathArchivo = "Facturas/" + self.informacionCliente[3] + ".pdf"
        try:
            QMessageBox.question(self, 'Mensaje', "Proceso terminado", QMessageBox.Ok)
            mandarCorreoFactura(self.informacionCliente[8], pathArchivo)
        except:
            QMessageBox.question(self, 'Mensaje', "Error verifique correo ingresado", QMessageBox.Ok)
