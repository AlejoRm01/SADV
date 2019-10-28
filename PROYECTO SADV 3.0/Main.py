import sys
from PyQt5 import QtCore, QtWidgets
from Login import Login
from Inventario import Inventario
from Compra import Compra
from Venta import Venta
from Usuario import Usuario

"""
Clase Main
Encargada de llamara a las demas clases, ponerlas en ejecucion, y administrar datos entre ellas.
"""
class Controlador:

    def __init__(self):
        pass

    def show_Ingreso(self):
        self.Login = Login()
        self.Login.switch_Inventario.connect(self.show_Inventario)
        self.Login.show()

    def show_Inventario(self):
        self.inventario = Inventario()
        self.inventario.switch_Compra.connect(self.show_Compra)
        self.inventario.switch_Venta.connect(self.show_Venta)
        self.inventario.switch_Usuario.connect(self.show_Usuario)
        self.Login.close()
        self.inventario.show()
        
    def show_Compra(self):
        self.compra = Compra()
        self.compra.switch_Inventario.connect(self.show_Inventario)
        self.compra.switch_Venta.connect(self.show_Venta)
        self.compra.switch_Usuario.connect(self.show_Usuario)
        self.compra.show()
        
    def show_Venta(self):
        self.venta = Venta()
        self.venta.switch_Inventario.connect(self.show_Inventario)
        self.venta.switch_Compra.connect(self.show_Venta)
        self.venta.switch_Usuario.connect(self.show_Usuario)
        self.venta.show()
        
    def show_Usuario(self):
        self.usuario = Usuario()
        self.usuario.switch_Inventario.connect(self.show_Inventario)
        self.usuario.switch_Compra.connect(self.show_Compra)
        self.usuario.switch_Venta.connect(self.show_Venta)
        self.usuario.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controlador = Controlador()
    controlador.show_Ingreso()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()