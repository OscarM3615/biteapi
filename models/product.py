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
	image = db.Column(db.String(16000000), nullable = False)
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

	def json(self):
		"""
		Devuelve el producto en formato JSON.
		"""
		return {
			"product_id": self.product_id,
			"user": self.user.json(),
			"category": self.category.json(),
			"name": self.name,
			"description": self.description,
			"price": self.price,
			"image": self.image
		}

	@classmethod
	def find_by_id(cls, product_id: int):
		return cls.query.filter_by(product_id = product_id).first()

	@classmethod
	def get_by_user(cls, user_id: int):
		return cls.query.filter_by(user_id = user_id).all()

	@classmethod
	def get_visibles(cls):
		return cls.query.filter_by(visible = True).all()

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
