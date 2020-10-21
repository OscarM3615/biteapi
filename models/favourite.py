"""
Este módulo contiene la clase para hacer cambios sobre los favoritos en la base de datos.
"""

from db import db

class FavouriteModel(db.Model):
	"""
	Se genera un objeto de esta clase cuando un usuario marca un producto como favorito.
	"""
	__tablename__ = 'Favourites'

	favourite_id = db.Column(db.Integer(), primary_key = True)
	user_id = db.Column(db.Integer(), db.ForeignKey('Users.id', ondelete = 'CASCADE'))
	product_id = db.Column(db.Integer(), db.ForeignKey('Products.product_id', ondelete = 'CASCADE'))

	def __init__(self, user_id: int, product_id: int):
		self.user_id = user_id
		self.product_id = product_id

	def json(self):
		"""
		Devuelve el favorito en formato JSON.
		"""
		return {
			"id": self.favourite_id,
			"product": self.product.json()
		}
	
	@classmethod
	def find_by_id(cls, favourite_id: int):
		"""
		Devuelve un favorito con base en su ID.
		"""
		return cls.query.filter_by(favourite_id = favourite_id).first()
	
	@classmethod
	def find_if_exists(cls, user_id: int, product_id: int):
		"""
		Devuelve el objeto si existe, de lo contrario, devuelve None.
		"""
		return cls.query.filter_by(user_id = user_id).filter_by(product_id = product_id).first()

	@classmethod
	def get_by_user(cls, user_id: int):
		"""
		Devuelve la lista de favoritos de un usuario.
		"""
		return cls.query.filter_by(user_id = user_id).all()

	def save_to_db(self):
		"""
		Guarda los datos del objeto en la base de datos. No se puede actualizar aunque el método lo permita.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina el registro de la base de datos. Ocurre cuando un usuario quita un producto de sus favoritos.
		"""
		db.session.delete(self)
		db.session.commit()
