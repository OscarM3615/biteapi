"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de usuarios.
"""

import bcrypt
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.user import UserModel
from regex import identityRegex, emailRegex, passwordRegex, base64Regex
from constants import admitted_users

class User(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar usuarios.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('first_name', type = str, required = True, help = 'El nombre es requerido.')
	parser.add_argument('last_name', type = str, required = True, help = 'El apellido es requerido.')
	parser.add_argument('email', type = str, required = True, help = 'El correo es requerido.')
	parser.add_argument('user_type',
		type = str,
		choices = admitted_users,
		help = f'El tipo de usuario puede ser: {admitted_users!r}.'
	)

	@jwt_required()
	def get(self, user_id: int):
		"""
		Obtener los datos del usuario. Se le permite a cualquiera.
		"""
		user = UserModel.find_by_id(user_id)
		if not user:
			return {"message": f"El usuario con ID {user_id!r} no ha sido encontrado."}, 404
		return user.json()

	@jwt_required()
	def put(self, user_id: int):
		"""
		Actualizar los datos del usuario. Permitir solo si es el mismo usuario quien lo solicita.
		"""
		if current_identity.id != user_id:
			return {"message": "No tiene permiso para modificar los datos de esta cuenta."}, 401

		data = User.parser.parse_args()
		user = UserModel.find_by_id(user_id)

		if identityRegex.match(data['first_name']) is None or identityRegex.match(data['last_name']) is None:
			return {"message": "El formato del nombre o apellido no es correcto."}, 400

		if emailRegex.match(data['email']) is None:
			return {"message": "El correo proporcionado no parece ser un correo realmente."}, 400

		if UserModel.find_by_email(data['email']) and user.email != data['email']:
			return {"message": "El correo proporcionado ya pertenece a una cuenta registrada."}, 400

		if data.get('user_type'):
			user.user_type = data['user_type']

		user.first_name = data['first_name']
		user.last_name = data['last_name']
		user.email = data['email']
		user.save_to_db()

		return user.json()

	@jwt_required()
	def delete(self, user_id: int):
		"""
		Eliminar un usuario de la base de datos. Permitir eliminación solo si es el mismo usuario o es de tipo admin.
		"""
		if current_identity.id != user_id and current_identity.user_type != 'admin':
			return {"message": "No tiene permiso para eliminar esta cuenta."}, 401

		user = UserModel.find_by_id(user_id)
		if not user:
			return {"message": f"El usuario con ID {user_id!r} no existe."}, 404

		user.delete_from_db()
		return {"message": f"Usuario con ID {user_id!r} borrado correctamente."}

class UserPicture(Resource):
	"""
	Esta clase permite modificar la imagen de perfil del usuario.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('picture', type = str, required = True, help = 'La imagen es requerida (base64 o null).')

	@jwt_required()
	def put(self, user_id: int):
		"""
		Actualiza la imagen del perfil (debe estar en base64).
		"""
		if current_identity.id != user_id:
			return {"message": "No tiene permitido modificar la imagen de perfil de la cuenta."}, 401

		data = UserPicture.parser.parse_args()
		user = UserModel.find_by_id(user_id)

		if data['picture'] is not None and base64Regex.match(data['picture']) is None:
			return {"message": "Se debe proporcionar un base64 de tipo imagen (png, jpg, gif) o null."}, 400

		user.picture = data['picture']
		user.save_to_db()

		return user.json()

class UserRegistration(Resource):
	"""
	Esta clase permite el registro de nuevos usuarios.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('first_name', type = str, required = True, help = 'El nombre es requerido.')
	parser.add_argument('last_name', type = str, required = True, help = 'El apellido es requerido.')
	parser.add_argument('email', type = str, required = True, help = 'El correo es requerido.')
	parser.add_argument('password', type = str, required = True, help = 'La contraseña es requerida.')

	def post(self):
		"""
		Registrar a un usuario en la base de datos proporcionando su nombre completo, correo y contraseña.
		"""
		data = UserRegistration.parser.parse_args()

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

		return new_user.json(), 201

class UserData(Resource):
	"""
	Esta clase permite identificar al usuario. 
	"""
	@jwt_required()
	def get(self):
		"""
		Devuelve los datos del usuario que realizó la petición.
		"""
		user = UserModel.find_by_id(current_identity.id)
		return user.json()
