from flask import Flask
import mysql.connector
import os 
import time



# $env:FLASK_APP="app"
#https://cursos.alura.com.br/forum/topico-erro-ao-instalar-mysql-windows-118603 ajuda para SisVet

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port = 3306,
    password="4389leo;",
    auth_plugin='mysql_native_password'
)   

from views import *

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True) 





