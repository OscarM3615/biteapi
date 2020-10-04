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
	user_id = db.Column(db.Integer(), db.ForeignKey('Users.user_id', ondelete = 'CASCADE'))
	product_id = db.Column(db.Integer(), db.ForeignKey('Products.product_id', ondelete = 'CASCADE'))

	def __init__(self, user_id, product_id):
		self.user_id = user_id
		self.product_id = product_id

	def save_to_db(self):
		"""
		Guarda los datos del objeto en la base de datos. No se puede actualizar aunque el método lo permite.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina el registro de la base de datos. Ocurre cuando un usuario quita un producto de sus favoritos.
		"""
		db.session.delete(self)
		db.session.commit()
