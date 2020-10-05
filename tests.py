"""
Pruebas unitarias para comprobar que las expresiones regulares funcionan como es debido.
"""

from unittest import TestCase, main as tests_main
from regex import identityRegex, emailRegex, passwordRegex

class IdentityTest(TestCase):
	"""
	Comprobar que identityRegex funciona.
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

class EmailTest(TestCase):
	"""
	Comprobar que emailRegex funciona.
	"""

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

class PasswordTest(TestCase):
	"""
	Comprobar que passwordRegex funciona.
	"""

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

if __name__ == '__main__':
	tests_main()
