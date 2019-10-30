import sys, time, locale
from Utiles.Conexion import getProductos
from UI.UI_compra import *

"""
Clase Compra
En esta clase se realiza  toda la actividad de realizar una compra, confirmar comprar
confirmar envio de correos y confirmar la genereacion de facturas.
"""
class Compra():
    def __init__(self):
        self.UIc = UI_Compra(getProductos())
        self.informacionCompra = []
        self.referencia = None
        if(self.referencia != None):
            self.ingresar()        
        self.UIc.sigAceptar.connect(self.aceptar)
        self.UIc.sigEliminar.connect(self.eliminar)
        self.UIc.sigEliminarTodo.connect(self.eliminarTodo)
        self.UIc.sigEditar.connect(self.editar)
    #-----------------Triggers-----------------
    def show(self):
        self.UIc.show()
    def hide(self):
        self.UIc.hie() 
        
    def ingresar(self):
        pass
    def aceptar(self):
        pass        
    def editar(self):
       pass
    def eliminar(self):
        pass
    def eliminarTodo(self):
        pass
    
    