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
	image = db.Column(db.String(10485760), nullable = False)
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
			"id": self.product_id,
			"vendor": self.user.json(),
			"category": self.category.json(),
			"name": self.name,
			"description": self.description,
			"price": self.price,
			"image": self.image,
			"visible": self.visible
		}

	@classmethod
	def find_by_id(cls, product_id: int):
		"""
		Devuelve un objeto ProductModel con base en su ID.
		"""
		return cls.query.filter_by(product_id = product_id).first()

	@classmethod
	def get_by_user(cls, user_id: int):
		"""
		Devuelve una lista de productos que pertenezcan al usuario.
		"""
		return cls.query.filter_by(user_id = user_id).all()

	@classmethod
	def get_page(cls, page: int, vendor_id: int = None, category_id: int = None, search: str = None):
		"""
		Devuelve una lista de productos con el atributo visible en True.
		"""
		results = cls.query.filter_by(visible = True).order_by(cls.product_id.desc())
		if vendor_id:
			results = results.filter_by(user_id = vendor_id)
		if category_id:
			results = results.filter_by(category_id = category_id)
		if search:
			results = results.filter(cls.name.like(f'%{search}%'))
		return results.paginate(page, 10, False).items

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

	@classmethod
	def delete_user_products(cls, user_id: int):
		"""
		Elimina todos los productos de un usuario.
		"""
		cls.query.filter_by(user_id = user_id).delete()
		db.session.commit()
