"""
Este módulo contiene la clase para hacer cambios sobre los productos en la base de datos.
"""

from db import db

class ProductModel(db.Model):
	"""
	Producto para vender, agregado por un vendedor.
	"""
	__tablename__ = 'Products'

	product_id = db.Column(db.Integer(), primary_key = True)
	user_id = db.Column(db.Integer(), db.ForeignKey('Users.id', ondelete = 'CASCADE'))
	category_id = db.Column(db.Integer(), db.ForeignKey('Categories.category_id', ondelete = 'CASCADE'))
	name = db.Column(db.String(20), nullable = False)
	description = db.Column(db.String(255), nullable = False)
	price = db.Column(db.Float(precision = 2), nullable = False)
	image = db.Column(db.String(100), nullable = False)
	visible = db.Column(db.Boolean(), nullable = False)

	favourites = db.relationship('FavouriteModel', backref = 'product', cascade = 'all, delete-orphan', lazy = 'dynamic')
	orders = db.relationship('OrderModel', backref = 'product', cascade = 'all, delete-orphan', lazy = 'dynamic')
	opinions = db.relationship('OpinionModel', backref = 'product', cascade = 'all, delete-orphan', lazy = 'dynamic')

	def __init__(self, user_id: int, category_id: int, name: str, description: str, price: float, image: str):
		self.user_id = user_id
		self.category_id = category_id
		self.name = name
		self.description = description
		self.price = price
		self.image = image
		self.visible = True

	def save_to_db(self):
		"""
		Guarda o actualiza los datos del producto agregado por el vendedor.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina el producto de la base de datos.
		"""
		db.session.delete(self)
		db.session.commit()
