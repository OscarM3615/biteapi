"""
Punto de inicio al sistema.
En este archivo se establece la configuración sobre las diferentes librerías y se especifican los puntos de acceso para la API.
"""

import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.category import Category, CategoryList
from resources.favourite import Favourite
from resources.opinion import Opinion, OpinionList
from resources.order import Order, OrderList
from resources.product import Product, ProductList, ProductStock
from resources.report import Report, ReportList
from resources.user import User, UserPicture, UserRegistration
from security import authenticate, identity
from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///Data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_AUTH_URL_RULE'] = '/login' # Establecer la ruta de identificación /login.
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 30) # El JWT expira en 1 mes.
app.config['JWT_AUTH_USERNAME_KEY'] = 'email' # Pedir correo en lugar del nombre de usuario.

app.secret_key = os.environ.get('SECRET_KEY', '05d08a3aa04b7283bba6ebf3')

api = Api(app)
jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_tables():
	"""
	Crear las tablas de la base de datos para que puedan ser utilizadas.
	"""
	db.create_all()

# Rutas de la API.
api.add_resource(UserRegistration, '/register')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserPicture, '/users/<int:user_id>/picture')
api.add_resource(CategoryList, '/categories')
api.add_resource(Category, '/categories/<int:category_id>')
api.add_resource(OrderList, '/orders')
api.add_resource(Order, '/orders/<int:order_id>')
api.add_resource(ProductList, '/products')
api.add_resource(Product, '/products/<int:product_id>')
api.add_resource(ProductStock, '/users/<int:user_id>/products')
api.add_resource(OpinionList, '/products/<int:product_id>/opinions')
api.add_resource(Opinion, '/products/<int:product_id>/opinions/<int:opinion_id>')
api.add_resource(ReportList, '/reports')
api.add_resource(Report, '/reports/<int:report_id>')

db.init_app(app)

if __name__ == '__main__':
	app.run(debug = True)
