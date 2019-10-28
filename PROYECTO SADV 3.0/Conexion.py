import pymongo
from Verificar import *

def conectar():
   client = pymongo.MongoClient()
   db = client['Diem']
   return db

def obtenerProductos():
   db = conectar()
   result = db.Productos.find()
   productos = []
   for i in result:
      productos.append(i['Descripcion'])
   return productos

def enviarCompra(factura, descripcion, socio, moneda, tasa, fecha, valorLote, codigos):
   db = conectar()
   db.Compras.insert({
      'Factura': factura,
      'Descripcion': descripcion,
      'Socio': socio,
      'Moneda': moneda,
      'Tasa': tasa,
      'Fecha': fecha,
      'ValorLote': valorLote,
      'Codigos': codigos
   })

def obtenerCodigosActualizacion(descripcion):
   db = conectar()
   result = db.Productos.find({'Descripcion': descripcion})
   codigos = []
   denominacion = 0
   stockMinimo = 0
   for i in result:
      codigos = i['Codigos']
      denominacion = i['Denominacion']
      stockMinimo = i['StockMinimo']

   return denominacion, descripcion, stockMinimo, codigos

def enviarCodigos(codigos, descripcion):

   db = conectar()
   denominacion, descripcion, stockMinimo, codigosViejos = obtenerCodigosActualizacion(descripcion)
   codigos.extend([element for element in codigosViejos if element not in codigos])

   db.Productos.update({
      'Descripcion': descripcion
   },
   {
      'Denominacion': denominacion,
      'Descripcion': descripcion,
      'StockMinimo' : stockMinimo,
      'Codigos': codigos
   })

def obtenerInventario():
   db = conectar()
   result = db.Productos.find()
   inventario = []
   for i in result:
      cantidad = len(i['Codigos'])
      stockMinimo = i['StockMinimo']
      denominacion = i['Denominacion']
      acumulado = denominacion * cantidad
      if (cantidad >= stockMinimo):
         inventario.append([cantidad,denominacion,acumulado,i['Descripcion'],stockMinimo,'Stock Completo'])
      else:
         inventario.append([cantidad,denominacion,acumulado,i['Descripcion'],stockMinimo,'No suficiente'])
   return inventario

def obtenerCodigosParaVender(producto, cantidad):
   db = conectar()
   denominacion, descripcion, stockMinimo, codigosViejos = obtenerCodigosActualizacion(producto)

   aux = 0
   codigosParaVender = []
   codigos = []
   for i in codigosViejos:
      aux += 1
      if aux <= int(cantidad):
         codigosParaVender.append(i)
      if aux > int(cantidad):
         codigos.append(i)
   db.Productos.update({
      'Descripcion': descripcion
   },
   {
      'Denominacion': denominacion,
      'Descripcion': descripcion,
      'StockMinimo' : stockMinimo,
      'Codigos': codigos
   })

   return codigosParaVender

def verificarCodigos(codigos):

      db = conectar()
      result = db.Productos.find()

      for i in result:
         codigosDB = i['Codigos']
         comparacion = [item for item in codigos if item in codigosDB]
         comparacion.insert(0, "Codigos Repetidos")
         if len(comparacion) > 1:
            return comparacion
         else:
            return ['False']

def enviarVenta(cliente, venta):
   #FECHA, NUMERO FACTURA, CLIENTE, IDENTIFICACION, CELULAR, DEPARTAMENTO, TELEFONO, DIRECCION, CORREO, DESCUENTO, TPAGO
   db = conectar()
   db.ventas.insert({
      'Fecha': cliente[0],
      'Factura': cliente[1],
      'Cliente': cliente[2],
      'Identificacion': cliente[3],
      'Celular': cliente[4],
      'Departamento': cliente[5],
      'Telefono': cliente[6],
      'Direccion': cliente[7],
      'Correo': cliente[8],
      'Descuento': cliente[9],
      'Tipo_Pago': cliente[10],
      'Productos': venta
   })

def obtenerUsuarios():
   db = conectar()

   usuarios = db.Usuarios.find({'Administrador': False})
   us = []
   for i in usuarios:
      us.append(i['Nombre del usuario']) 
   return us

def borrarUs(usuario):
   db = conectar()
   db.Usuarios.remove({'Nombre del usuario': usuario})

def agregarUs(usuario,contraseña, tipoUsu) :
    con = encriptar(contraseña)

    db = conectar()
    db.Usuarios.insert({
        'Nombre del usuario' : usuario,
        'Contraseña' : con,
        'Administrador' : tipoUsu
    })
