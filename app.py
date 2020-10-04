"""
Punto de inicio al sistema.
En este archivo se establece la configuración sobre las diferentes librerías y se especifican los puntos de acceso para la API.
"""

import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///Data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', '05d08a3aa04b7283bba6ebf3')

api = Api(app)
jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_tables():
	"""
	Crear las tablas de la base de datos para que puedan ser utilizadas.
	"""
	db.create_all()

db.init_app(app)

if __name__ == '__main__':
	app.run(debug = True)
