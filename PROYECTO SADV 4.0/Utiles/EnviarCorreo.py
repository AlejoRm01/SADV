import os
import smtplib
import imghdr
from Constantes import *
from email.message import EmailMessage
import smtplib, getpass, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

def mandarCorreoHtml(correo):
    EMAIL_ADDRESS = EMAIL
    EMAIL_PASSWORD = CONTRASEÑA

    msg = EmailMessage()
    msg['Subject'] = ASUNTO
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = correo
    msg.set_content(ASUNTO)

    #msg.add_alternative()

    archivos = [CODIGOS]

    for archivo in archivos:
        with open(archivo, 'rb') as f:
            file_data = f.read()
            file_name = f.name

    msg.add_attachment(file_data, maintype = 'aplication', subtype ='octect-stream', filename = file_name)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def mandarCorreoFactura(correo, pathArchivo):
    EMAIL_ADDRESS = EMAIL
    EMAIL_PASSWORD = CONTRASEÑA
    msg = EmailMessage()
    msg['Subject'] = ASUNTO
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = correo

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title></title>
    </head>
    <body style="background-color: #222831 ">

    <!--Copia desde aquí-->
    <table style="max-width: 600px; padding: 10px; margin:0 auto; border-collapse: collapse;">
        <tr>
            <td style="background-color: #222831; text-align: left; padding: 0">
            </td>
        </tr>

        <div style="text-align: center">
            <a href="link">
            
            <img src="https://i.postimg.cc/gcgjkHCw/DIEM-T.png" align="center"></a>
            </div>

        <tr>
            <td style="background-color: #222831">
                <div style="color: #222831; margin: 4% 10% 2%; text-align: justify;font-family: sans-serif">
                    <h1 align="center" style="color: #ff6600; margin: 0 0 7px">Tu Factura</h1>
                    <p align="center" style="color: #ecf0f1; margin: 2px; font-size: 15px">
                        Listo, Ya tienes tus codigos.<br>
                        Guarda este correo  y tu facttura<br>
                        por si pierdes tus codigos o pasa algo con tu cuenta</p>
                        <p align="center" style="color: #ecf0f1; margin: 5px; font-size: px">
                            <b>codigos</b></p>
                    </ul>
                    <div style="width: 100%;margin:10px 0; display: inline-block;text-align: center">
            
                    </div>
                    <div style="width: 100%; text-align: center">
                        <a style="text-decoration: none; margin: 10px; border-radius: 5px; padding: 11px 23px; color: white; background-color: #3498db" href="http://diem.com.co/">Ir a la página</a>	
                    </div>
                    <p style="color: #b3b3b3; font-size: 12px; text-align: center;margin: 30px 0 0">DIEM.COM.CO</p>
                </div>
            </td>
        </tr>
    </table>
    <!--hasta aquí-->

    </body>
    </html>



    """, subtype='html')
    
    archivos = [pathArchivo]

    for archivo in archivos:
        with open(archivo, 'rb') as f:
            file_data = f.read()
            file_name = f.name

    msg.add_attachment(file_data, maintype = 'aplication', subtype ='octect-stream' , filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

#mandarCorreoHtml('arodriguem@hotmail.com')
#mandarCorreoFactura('alejo543rm@gmail.com', 'Facturas/1000748121.pdf')