"""
Este módulo contiene la clase para hacer cambios sobre los usuarios en la base de datos.
"""

from db import db
from constants import user_types

class UserModel(db.Model):
	"""
	El usuario puede registrarse desde los recursos, entonces se creará en la base de datos.
	"""
	__tablename__ = 'Users'

	id = db.Column(db.Integer(), primary_key = True)
	first_name = db.Column(db.String(20), nullable = False)
	last_name = db.Column(db.String(20), nullable = False)
	email = db.Column(db.String(50), unique = True, nullable = False)
	password = db.Column(db.String(80), nullable = False)
	user_type = db.Column(db.String(10), nullable = False)
	picture = db.Column(db.String(10485760))
	active_state = db.Column(db.Boolean(), nullable = False)

	customers = db.relationship('OrderModel', backref = 'customer', cascade = 'all, delete-orphan', lazy = 'dynamic', foreign_keys = 'OrderModel.customer_id')
	favourites = db.relationship('FavouriteModel', backref = 'user', cascade = 'all, delete-orphan', lazy = 'dynamic')
	products = db.relationship('ProductModel', backref = 'user', cascade = 'all, delete-orphan', lazy = 'dynamic')
	reports = db.relationship('ReportModel', backref = 'user', cascade = 'all, delete-orphan', lazy = 'dynamic')
	vendors = db.relationship('OrderModel', backref = 'vendor', cascade = 'all, delete-orphan', lazy = 'dynamic', foreign_keys = 'OrderModel.vendor_id')

	def __init__(self, first_name: str, last_name: str, email: str, password: str):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.user_type = user_types['normal']
		self.picture = None
		self.active_state = True

	def json(self):
		"""
		Devuelve el usuario en formato JSON.
		"""
		return {
			"id": self.id,
			"first_name": self.first_name,
			"last_name": self.last_name,
			"email": self.email,
			"type": self.user_type,
			"picture": self.picture,
			"is_active": self.active_state
		}

	@classmethod
	def find_by_id(cls, user_id: int):
		"""
		Devuelve un objeto de esta clase con base en su ID, si no es encontrado devuelve None.
		"""
		return cls.query.filter_by(id = user_id).first()

	@classmethod
	def find_by_email(cls, email: str):
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
