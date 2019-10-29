import sys
from Utiles.Verificar import verificar
from UI.UI_login import *
from Constantes import ADMINISTRADOR
class Login():
    
    def __init__(self):
        self.UIl = UI_login()
        self.usurio = None
        self.contrasena = None
        self.tipoCuenta = None
        self.UIl.sigValidar.connect(self.validar)
    #-----------------FUNCIONES-----------------
    def validar(self):
        self.usurio = self.UIl.getUsuario()
        self.contrasena = self.UIl.getContrasena()
        self.tipoCuenta = self.UIl.getTipoCuenta()
        Tipo_cuenta = True if (self.tipoCuenta == ADMINISTRADOR) else False
        if verificar(self.usurio, self.contrasena, Tipo_cuenta):
            self.UIl.abrirInventario()
        else:
            self.UIl.abrirInventario()
            #self.UIl.throwMsgErrorProceso()
            
    def show(self):
        self.UIl.show()
    def close(self):
        self.UIl.close()