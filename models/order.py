"""
Este módulo contiene la clase para hacer cambios sobre los pedidos en la base de datos.
"""

from datetime import datetime
from db import db

class OrderModel(db.Model):
	"""
	El pedido es generado cuando un usuario pide el producto de un vendedor.
	"""
	__tablename__ = 'Orders'

	order_id = db.Column(db.Integer(), primary_key = True)
	customer_id = db.Column(db.Integer(), db.ForeignKey('Users.id', ondelete = 'CASCADE'))
	vendor_id = db.Column(db.Integer(), db.ForeignKey('Users.id', ondelete = 'CASCADE'))
	product_id = db.Column(db.Integer(), db.ForeignKey('Products.product_id', ondelete = 'CASCADE'))
	location = db.Column(db.String(50), nullable = False)
	amount = db.Column(db.Integer(), nullable = False)
	comment = db.Column(db.String(100))
	status = db.Column(db.String(15), nullable = False)
	order_time = db.Column(db.DateTime(), default = datetime.utcnow)

	def __init__(self, customer_id: int, vendor_id: int, product_id: int, location: str, amount: float, comment: str):
		self.customer_id = customer_id
		self.vendor_id = vendor_id
		self.product_id = product_id
		self.location = location
		self.amount = amount
		self.comment = comment
		self.status = 'pendiente'

	def json(self):
		"""
		Devuelve el pedido en formato JSON.
		"""
		return {
			"customer": self.customer.json(),
			"product": self.product.json(),
			"location": self.location,
			"amount": self.amount,
			"comment": self.comment,
			"status": self.status,
			"order_time": str(self.order_time)
		}

	@classmethod
	def find_by_id(cls, order_id: int):
		"""
		Devuelve un objeto OrderModel con base en su ID.
		"""
		return cls.query.filter_by(order_id = order_id).first()

	@classmethod
	def get_by_customer(cls, customer_id: int):
		"""
		Devuelve la lista de pedidos que ha realizado un usuario normal.
		"""
		return cls.query.filter_by(customer_id = customer_id).all()

	@classmethod
	def get_by_vendor(cls, vendor_id: int):
		"""
		Devuelve la lista de pedidos que tiene por hacer un vendedor.
		"""
		return cls.query.filter_by(vendor_id = vendor_id).all()

	def save_to_db(self):
		"""
		Permite guardar o actualizar los detalles del pedido en la base de datos.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina el pedido de la base de datos.
		"""
		db.session.delete(self)
		db.session.commit()
