from cryptography.fernet import Fernet
from pymongo import MongoClient

#---------------------------Encriptar-----------------------------------
def encriptar(message):
    file = open('key.key','rb')
    key = file.read()
    file.close()

    encoded = message.encode()

    f = Fernet(key)
    encrypted = f.encrypt(encoded)

    return encrypted
#------------------Desencriptar-------------------------
def desencriptarContra(usuario,tipo):
    client = MongoClient()
    db = client['Diem']
    usuarios = db.Usuarios
    result = usuarios.find({
        'Nombre del usuario': usuario,
        'Administrador': tipo
    })

    if not(type(result) == None):
        for i in result:
            m = i['Contraseña']
            file = open('key.key','rb')
            key2 = file.read()
            file.close()

            f2 = Fernet(key2)
            decrypted = f2.decrypt(m).decode()

            return decrypted
#------------------------Verificar---------------------------- ----

def verificar(usuario,contra,tipo):
    entrar = False
    res = desencriptarContra(usuario,tipo)
    if contra == res :
        entrar = True
        return entrar
    else:
        return entrar

 