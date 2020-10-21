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
	name = db.Column(db.String(20), unique = True, nullable = False)

	products = db.relationship('ProductModel', backref = 'category', cascade = 'all, delete-orphan', lazy = 'dynamic')

	def __init__(self, name: str):
		self.name = name

	def json(self):
		"""
		Devuelve la categoría en formato JSON.
		"""
		return {
			"id": self.category_id,
			"name": self.name
		}

	@classmethod
	def find_by_id(cls, category_id: int):
		"""
		Devuelve un objeto de esta clase con base en su ID, si no es encontrado devuelve None.
		"""
		return cls.query.filter_by(category_id = category_id).first()

	@classmethod
	def find_by_name(cls, name: str):
		"""
		Devuelve un objeto CategoryModel con base en su nombre.
		"""
		return cls.query.filter_by(name = name).first()

	@classmethod
	def get_all(cls):
		"""
		Devuelve la lista de categorías existentes.
		"""
		return cls.query.all()

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
