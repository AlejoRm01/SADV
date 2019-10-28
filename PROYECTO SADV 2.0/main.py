import sys,time, locale, ast, re, os
from EnviarCorreo import mandarCorreoFactura, mandarCorreoHtml
from Conexion import *
from Factura import generarFactura, fecha, hacerCodigos
from Verificar import verificar
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Constantes import *

class VentanaIngreso(QMainWindow):
    def __init__(self):
        super(VentanaIngreso, self).__init__()
        loadUi('UI/Ingreso.ui', self)
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
        Contra_ing = self.lineEditContrasena.text()
        Usuario_ing = self.lineEditUsuario.text()
        Tipo_cuenta = True if (self.comboboxTipoCuenta.currentText() == ADMINISTRADOR) else False
        if verificar(Usuario_ing, Contra_ing, Tipo_cuenta):
            self.hide()
            otraVentana = VentanaInventario(self)
            otraVentana.Admin = Tipo_cuenta
            otraVentana.ver()
            otraVentana.show()
        else:
            QMessageBox.information(self, "Mensaje", "Contraseña incorrecta", QMessageBox.Ok)

class VentanaInventario(QMainWindow):
    Admin = False

    def __init__(self, parent=None):
        super(VentanaInventario, self).__init__(parent)
        loadUi('UI/Inventario.ui', self)
        self.setWindowIcon(QIcon(ICONO))
        ##################TABLA##################

        # Numero de columnas y nombre de estas
        self.tablaInventario.setColumnCount(6)
        nombreColumnas = ("Cantidad", "Denominacion", "Acumulado", "Descripcion", "Stock Minimo", "Estado")
        self.tablaInventario.setHorizontalHeaderLabels(nombreColumnas)
        self.tablaInventario.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaInventario.verticalHeader().setVisible(False)
        self.tablaInventario.setTextElideMode(Qt.ElideRight)
        self.tablaInventario.setAlternatingRowColors(True)
        self.tablaInventario.setDragDropOverwriteMode(False)
        self.tablaInventario.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Ancho columnas
        for indice, ancho in enumerate((70, 90, 80, 500, 90, 150), start=0):
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
        self.hide()
        otraVentana = VentanaCompra(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirVentas(self):
        self.hide()
        otraVentana = VentanaVenta(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirUsuarios(self):
        self.hide()
        otraVentana = VentanaUsuario(self)
        otraVentana.show()

class VentanaCompra(QMainWindow):
    Admin = False

    def __init__(self, parent=None):
        super(VentanaCompra, self).__init__(parent)
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
        self.hide()
        otraVentana = VentanaInventario(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirVentas(self):
        self.hide()
        otraVentana = VentanaVenta(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirUsuarios(self):
        self.hide()
        otraVentana = VentanaUsuario(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

class VentanaVenta(QMainWindow):
    Admin = False

    def __init__(self, parent=None):
        super(VentanaVenta, self).__init__(parent)
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
        self.checkBoxDigital.stateChanged.connect(self.clickBoxDigital)
        self.checkBoxFisico.stateChanged.connect(self.clickBoxFisico)
        self.botonVentasAceptar.clicked.connect(self.aceptar)
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

    def aceptar(self):

        locale.setlocale(locale.LC_ALL, '')
        self.lineEditDescuento.setEnabled(False)
        producto = self.comboBoxDescripcion.currentText()
        cantidad = self.spinBoxCantidad.value()
        cantidad = int(cantidad)
        valorTotal = 0
        descuento = int(self.lineEditDescuento.text())/ 100

        if cantidad > 0:
            try:
                precio = self.lineEditPrecio.text()
                valor = int(cantidad) * int(precio)
                self.arrAux.append(valor)
                self.venta.append([producto, str(cantidad), precio, str(valor)])
                valorT = str(locale.currency(valor, grouping=True))
                descripcion = producto + ' Cantidad: ' + str(cantidad) + "  Valor: " + str(valorT)

                for i in self.arrAux:
                    valorTotal += int(i)
                
                descuento = descuento * valorTotal
                descuento =  valorTotal - descuento
                self.descuento = valorTotal - descuento
                self.subtotal = valorTotal 
                self.total = descuento
                valorTotal = str(locale.currency(valorTotal, grouping=True))
                descuento = str(locale.currency(descuento, grouping=True))

                self.Label_Total.setText(str(valorTotal))
                self.valor_Descuento.setText(str(descuento))
                self.botonContinuarVenta.setEnabled(True)
                self.listWidget.addItem(descripcion)
                self.lineEditPrecio.setText("")
                self.spinBoxCantidad.setValue(0)
                

            except:
                QMessageBox.information(self, "Mensaje", "Proceso interrumpido, Corrija los valores introducidos",
                                        QMessageBox.Ok)

        else:
            QMessageBox.information(self, "Mensaje", "Proceso interrumpido, Observe cantidad y precio introducido", QMessageBox.Ok)

    def eliminar(self):

        self.row = self.listWidget.currentRow()
        self.arrAux.pop(self.row)
        self.venta.pop(self.row)

        valorTotal = 0
        descuento = int(self.lineEditDescuento.text())/ 100

        for i in self.arrAux:
                    valorTotal += int(i)

        descuento = descuento * valorTotal
        descuento =  valorTotal - descuento
        self.descuento = valorTotal - descuento
        self.subtotal = valorTotal 
        self.total = descuento
        
        descuento = str(locale.currency(descuento, grouping=True))
        valorTotal = str(locale.currency(valorTotal, grouping=True))

        self.valor_Descuento.setText(descuento)
        self.Label_Total.setText(str(valorTotal))
        self.listWidget.takeItem(self.row)

    def eliminarTodo(self):
        self.listWidget.clear()
        self.Label_Total.setText('0')
        self.valor_Descuento.setText('0')
        self.lineEditDescuento.setEnabled(True)
        self.venta = []
        self.arrAux = []
    def clickBoxDigital(self, state):
        if state == Qt.Checked:
            self.checkBoxFisico.setChecked(False)

    def clickBoxFisico(self, state):
        if state == Qt.Checked:
            self.checkBoxDigital.setChecked(False)

    def abrirInventario(self):
        self.hide()
        otraVentana = VentanaInventario(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirCompras(self):
        self.hide()
        otraVentana = VentanaCompra(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirUsuarios(self):
        self.hide()
        otraVentana = VentanaUsuario(self)
        otraVentana.Admin = self.Admin
        otraVentana.show()

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
        otraVentana = VentanaVenta(self)
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

class VentanaUsuario(QMainWindow):
    Admin = False

    def __init__(self, parent=None):
        super(VentanaUsuario, self).__init__(parent)
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

    def abrirInventario(self):
        self.hide()
        otraVentana = VentanaInventario(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirCompras(self):
        self.hide()
        otraVentana = VentanaCompra(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def abrirVentas(self):
        self.hide()
        otraVentana = VentanaVenta(self)
        otraVentana.Admin = self.Admin
        otraVentana.ver()
        otraVentana.show()

    def aggUsuario(self):
        usu = self.lineEditUsuario.text()
        con = self.lineEditContrasena.text()
        tipo = True if (self.comboBoxTipoCuenta.currentText() == "Administrador/a") else False
        agregarUs(usu, con, tipo)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = VentanaIngreso()
    main.show()
    sys.exit(app.exec_())

#jhonmarioclinicadelplay
