"""
Pruebas unitarias para comprobar que las expresiones regulares funcionan como es debido.
"""

from unittest import TestCase, main as tests_main

from app import app
from models.category import CategoryModel
from models.favourite import FavouriteModel # pylint: disable=unused-import
from models.opinion import OpinionModel # pylint: disable=unused-import
from models.order import OrderModel # pylint: disable=unused-import
from models.product import ProductModel # pylint: disable=unused-import
from models.report import ReportModel # pylint: disable=unused-import
from models.user import UserModel # pylint: disable=unused-import
from db import db
from regex import identityRegex, emailRegex, passwordRegex, imgurlRegex

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

	def test_imagen_raiz(self):
		"""Imagen en la raíz de un sitio web."""
		self.assertIsNotNone(imgurlRegex.match('https://sitio.com/imagen.jpg'))

	def test_imagen_folder(self):
		"""Imagen dentro de un directorio en sitio web."""
		self.assertIsNotNone(imgurlRegex.match('https://sitio.com/dir1/imagen.jpg'))

	def test_imagen_folder2(self):
		"""Imagen dentro de varios directorios."""
		self.assertIsNotNone(imgurlRegex.match('https://sitio.com/dir1/dir2/imagen.jpg'))

	def test_no_imagen(self):
		"""El archivo no es de tipo imagen."""
		self.assertIsNone(imgurlRegex.match('https://sitio.com/archivo.txt'))

	def test_dominio_con_espacios(self):
		"""El dominio de la imagen tiene espacios."""
		self.assertIsNone(imgurlRegex.match('https://sitio no valido.com/imagen.png'))

	def test_nombre_imagen_invalido(self):
		"""El nombre de la imagen tiene caracteres inválidos."""
		self.assertIsNone(imgurlRegex.match('https://sitio.com/"imagen.png"'))

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
