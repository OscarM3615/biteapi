"""
Este módulo contiene la clase para hacer cambios sobre las categorías en la base de datos.
"""

from db import db

class CategoryModel(db.Model):
	"""
	Categoría a la que puede pertenecer un producto.
	"""
	__tablename__ = 'Categories'

	category_id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String(20))

	products = db.relationship('ProductModel', backref = 'category', cascade = 'all, delete-orphan', lazy = 'dynamic')

	def __init__(self, name: str):
		self.name = name

	def save_to_db(self):
		"""
		Actualizar los datos de la categoría en la base de datos.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Eliminar el registro de la base de datos.
		"""
		db.session.delete(self)
		db.session.commit()
