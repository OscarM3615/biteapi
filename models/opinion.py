"""
Este módulo contiene la clase para hacer cambios sobre las opiniones en la base de datos.
"""

from db import db

class OpinionModel(db.Model):
	"""
	Opinión de un usuario sobre un producto comprado.
	"""
	__tablename__ = 'Opinions'

	opinion_id = db.Column(db.Integer(), primary_key = True)
	product_id = db.Column(db.Integer(), db.ForeignKey('Products.product_id', ondelete = 'CASCADE'))
	rating = db.Column(db.Integer(), nullable = False)
	comment = db.Column(db.String(50), nullable = False)

	def __init__(self, product_id: int, rating: int, comment: str):
		self.product_id = product_id
		self.rating = rating
		self.comment = comment

	def json(self):
		"""
		Devuelve la opinión en formato JSON.
		"""
		return {
			"id": self.opinion_id,
			"productId": self.product_id,
			"rating": self.rating,
			"comment": self.comment
		}

	@classmethod
	def find_by_id(cls, opinion_id: int):
		"""
		Devuelve los detalles de una opinión con base en su ID.
		"""
		return cls.query.filter_by(opinion_id = opinion_id).first()

	@classmethod
	def get_by_product(cls, product_id: int):
		"""
		Devuelve la lista de opiniones hechas sobre un producto.
		"""
		return cls.query.filter_by(product_id = product_id).all()

	def save_to_db(self):
		"""
		Guarda la opinión en la base de datos. No puede ser actualizada, aunque el método lo permita.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina la opinión de la base de datos.
		"""
		db.session.delete(self)
		db.session.commit()
