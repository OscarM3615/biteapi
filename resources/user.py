"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de usuarios.
"""

import re
import bcrypt
from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar usuarios.
	"""
	pass

class UserRegistration(Resource):
	"""
	Esta clase permite el registro de nuevos usuarios.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('first_name', type = str, required = True, help = 'El nombre es requerido.')
	parser.add_argument('last_name', type = str, required = True, help = 'El apellido es requerido.')
	parser.add_argument('email', type = str, required = True, help = 'El correo es requerido.')
	parser.add_argument('password',type = str, required = True, help = 'La contraseña es requerida.')

	def post(self):
		data = UserRegistration.parser.parse_args()

		identityRegex = re.compile(r'^[a-záéíóúñ]{1,20}$', re.IGNORECASE)
		emailRegex = re.compile(r'^[A-Za-z0-9_\-]+(\.[A-Za-z0-9_\-]+)*@([A-Za-z0-9_\-]+\.)+[a-z]{2,5}$')
		passwordRegex = re.compile(r'.{4,}')

		if UserModel.find_by_email(data['email']):
			return {"message": "Ya existe una cuenta registrada con ese correo."}, 400

		if identityRegex.match(data['first_name']) is None or identityRegex.match(data['last_name']) is None:
			return {"message": "El formato del nombre o apellido no es correcto."}, 400

		if emailRegex.match(data['email']) is None:
			return {"message": "El correo proporcionado no parece ser un correo realmente."}, 400

		if passwordRegex.match(data['password']) is None:
			return {"message": "La contraseña indicada es muy corta (mínimo 4 caracteres)."}, 400

		hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
		new_user = UserModel(data['first_name'], data['last_name'], data['email'], hashed_password)
		new_user.save_to_db()

		return {"message": "Usuario creado correctamente."}, 201
