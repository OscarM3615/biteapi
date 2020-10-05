"""
Este módulo contiene la clase para hacer cambios sobre los usuarios en la base de datos.
"""

from hashlib import sha256
from random import randint
from db import db

class UserModel(db.Model):
	"""
	El usuario puede registrarse desde los recursos, entonces se creará en la base de datos.
	"""
	__tablename__ = 'Users'

	id = db.Column(db.Integer(), primary_key = True)
	first_name = db.Column(db.String(20))
	last_name = db.Column(db.String(20))
	email = db.Column(db.String(50), unique = True)
	password = db.Column(db.String(80))
	user_type = db.Column(db.String(10))
	picture = db.Column(db.String(100))
	active_state = db.Column(db.Boolean())
	recovery_key = db.Column(db.String(64))

	customers = db.relationship('OrderModel', backref = 'customer', cascade = 'all, delete-orphan', lazy = 'dynamic', foreign_keys = 'OrderModel.customer_id')
	favourites = db.relationship('FavouriteModel', backref = 'user', cascade = 'all, delete-orphan', lazy = 'dynamic')
	products = db.relationship('ProductModel', backref = 'user', cascade = 'all, delete-orphan', lazy = 'dynamic')
	reports = db.relationship('ReportModel', backref = 'user', cascade = 'all, delete-orphan', lazy = 'dynamic')
	vendors = db.relationship('OrderModel', backref = 'vendor', cascade = 'all, delete-orphan', lazy = 'dynamic', foreign_keys = 'OrderModel.vendor_id')

	def __init__(self, first_name, last_name, email, password):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.user_type = 'Normal'
		self.picture = None
		self.active_state = True
		self.recovery_key = sha256(str(randint(1, 9999)).encode('utf-8')).hexdigest()

	def json(self):
		return {
			"id": self.id,
			"first_name": self.first_name,
			"last_name": self.last_name,
			"email": self.email,
			"picture": self.picture,
			"is_active": self.active_state
		}

	@classmethod
	def find_by_id(cls, user_id):
		"""
		Devuelve un objeto de esta clase con base en su ID, si no es encontrado devuelve None.
		"""
		return cls.query.filter_by(id = user_id).first()

	@classmethod
	def find_by_email(cls, email):
		"""
		Devuelve un objeto de esta clase con base en su correo, si no es encontrado devuelve None.
		"""
		return cls.query.filter_by(email = email).first()

	def save_to_db(self):
		"""
		Guarda o actualiza los datos del usuario en la base de datos.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina al usuario de la base de datos.
		"""
		db.session.delete(self)
		db.session.commit()
