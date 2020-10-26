"""
Pruebas unitarias para comprobar que las expresiones regulares funcionan como es debido.
"""

from unittest import TestCase, main as tests_main

from app import app
from models.category import CategoryModel
from models.favourite import FavouriteModel
from models.opinion import OpinionModel
from models.order import OrderModel
from models.product import ProductModel
from models.report import ReportModel
from models.user import UserModel
from db import db
from regex import identityRegex, emailRegex, passwordRegex, base64Regex

class TestRegex(TestCase):
	"""
	Comprobar que las expresiones regulares funcionan correctamente.
	"""

	def test_un_nombre(self):
		"""Debe aceptar un solo nombre, incluso con acento."""
		self.assertIsNotNone(identityRegex.match('Óscar'))

	def test_dos_nombres(self):
		"""Debe aceptar si se incluyen los dos nombres."""
		self.assertIsNotNone(identityRegex.match('Óscar Antonio'))

	def test_tres_nombres(self):
		"""No debe aceptar más de dos nombres."""
		self.assertIsNone(identityRegex.match('Óscar Antonio Miranda'))

	def test_nombre_con_numeros(self):
		"""No debe aceptar nombres con números."""
		self.assertIsNone(identityRegex.match('OscarM3615'))

	def test_nombre_con_simbolos(self):
		"""No debe aceptar nombres con símbolos."""
		self.assertIsNone(identityRegex.match('André.'))

	def test_correo_dominio(self):
		"""Debe aceptar correos con la forma dominio.com"""
		self.assertIsNotNone(emailRegex.match('oscarmiranda3615@gmail.com'))

	def test_correo_subdominio(self):
		"""Debe aceptar correos con la forma subdominio.dominio.com"""
		self.assertIsNotNone(emailRegex.match('alXXXXXX@alumnos.uacj.mx'))

	def test_solo_dominio(self):
		"""Debe rechazar incluir solo el dominio."""
		self.assertIsNone(emailRegex.match('correo.com'))

	def test_sin_usuario(self):
		"""Debe rechazar cadenas que compiencen con @."""
		self.assertIsNone(emailRegex.match('@gmail.com'))

	def test_solo_usuario(self):
		"""Debe rechazar cadenas que no tengan el dominio."""
		self.assertIsNone(emailRegex.match('andre707'))

	def test_pw_4(self):
		"""Aceptar contraseñas de cuatro caracteres."""
		self.assertIsNotNone(passwordRegex.match('1234'))

	def test_pw_largo(self):
		"""Debe aceptar contraseñas largas."""
		self.assertIsNotNone(passwordRegex.match('contraseñamuylarga'))

	def test_pw_simbolos(self):
		"""Debe aceptar contraseñas con símbolos inusuales."""
		self.assertIsNotNone(passwordRegex.match('@password()'))

	def test_pw_corta(self):
		"""Rechazar cadenas de menos de 4 caracteres."""
		self.assertIsNone(passwordRegex.match('123'))

	def test_base64_valido(self):
		"""Se debe aceptar cualquier base64 que sea de tipo imagen."""
		self.assertIsNotNone(base64Regex.match('data:image/png;base64,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'))

	def test_base64_invalido(self):
		"""Rechazar cadenas que no sean base64."""
		self.assertIsNone(base64Regex.match('Esto no es base64'))

	def test_base64_no_imagen(self):
		"""Rechazar cadenas de base64 que no sean imágenes."""
		self.assertIsNone(base64Regex.match('data:text/html;base64,R0lGODlhPQBEAPeoAJosM//AwO/AwHVYZ/z595kzAP/s7P+goOXMv8+fhw/v739/f+8PD98fH/8mJl+fn/9ZWb8/PzWlwv///6wWGbImAPgTEMImIN9gUFCEm/gDALULDN8PAD6atYdCTX9gUNKlj8wZAKUsAOzZz+UMAOsJAP/Z2ccMDA8PD/95eX5NWvsJCOVNQPtfX/8zM8+QePLl38MGBr8JCP+zs9myn=='))

class TestCategory(TestCase):
	"""
	Comprobar que los métodos de CategoryModel funcionan correctamente.
	"""

	@staticmethod
	def crear_category():
		"""Devuelve un objeto CategoryModel."""
		category = CategoryModel('Test Category')
		category.save_to_db()
		return category

	def test_tiene_id(self):
		"""Verificar que los objetos *Model adquieren ID al almacenarse."""
		category = self.crear_category()
		self.assertIsInstance(category.category_id, int)
		category.delete_from_db()

	def test_json(self):
		"""Verificar que json contenga los datos necesarios."""
		category = self.crear_category()
		category_json = category.json()

		self.assertIsNotNone(category_json.get('id'))
		self.assertIsNotNone(category_json.get('name'))

		category.delete_from_db()

	def test_find_by_name(self):
		"""Comprobar que puede encontrar objetos por nombre."""
		category = self.crear_category()
		self.assertIsInstance(CategoryModel.find_by_name('Test Category'), CategoryModel)
		category.delete_from_db()

class TestUser(TestCase):
	"""
	Verificar el correcto funcionamiento de la clase UserModel.
	"""
	def test_recovery_key(self):
		"""Comprobar que la clave de recuperación no cambia a menos que se indique."""
		user1 = UserModel('Test', 'Account', 'unittest@hotmail.com', '1234')
		user1.save_to_db()
		key1 = user1.recovery_key

		user2 = UserModel.find_by_email('unittest@hotmail.com') 
		key2 = user2.recovery_key

		self.assertEqual(key1, key2)

		user1.delete_from_db()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '05d08a3aa04b7283bba6ebf3'

db.init_app(app)

if __name__ == '__main__':
	with app.app_context():
		tests_main()
