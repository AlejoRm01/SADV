import sys, time, locale
from Utiles.Factura import fecha as getFecha
#from Utiles.Conexion import 
from UI.UI_compra import *

"""
Clase Compra
En esta clase se realiza  toda la actividad de realizar una compra, confirmar comprar
confirmar envio de correos y confirmar la genereacion de facturas.
"""
class Compra():
    def __init__(self):
        self.UIc = UI_Compra()
        self.fecha = getFecha()
        self.UIc.setLEfecha(self.fecha)
        self.UIc.sigAceptar.connect(self.aceptar)
        self.UIc.sigAceptar.connect(self.aceptar)
        self.UIc.sigEliminar.connect(self.eliminar)
        self.UIc.sigEliminarTodo.connect(self.eliminarTodo)
        self.UIc.sigIngresarCodigos.connect(self.ingresarCodigos)
        self.UIc.sigEditar.connect(self.editar)
    #-----------------FUNCIONES-----------------
    def show(self):
        self.UIc.show()
            
    
            
    
    def editar(self):
       pass
    def eliminar(self):
        pass
    def eliminarTodo(self):
        pass
    def show(self):
        pass
    def hide(self):
        self.UIc.hie()
    