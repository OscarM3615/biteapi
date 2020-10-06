"""
Funciones para determinar la identidad del usuario y comprobar sus credenciales.
"""

import bcrypt
from models.user import UserModel

def authenticate(email: str, password: str):
	"""
	Devuelve al usuario en caso de que sus credenciales sean correctas, si no devuelve None.
	"""
	user = UserModel.find_by_email(email)

	if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
		return user
	return None

def identity(payload):
	"""
	Devuelve el usuario buscando el ID proporcionado en el JWT.
	"""
	user_id = payload['identity']
	return UserModel.find_by_id(user_id)
