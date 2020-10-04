"""
Este módulo contiene la clase para hacer cambios sobre las órdenes en la base de datos.
"""

from datetime import datetime
from db import db

class OrderModel(db.Model):
	"""
	La orden es generada cuando un usuario pide el producto de un vendedor.
	"""
	__tablename__ = 'Orders'

	order_id = db.Column(db.Integer(), primary_key = True)
	customer_id = db.Column(db.Integer(), db.ForeignKey('Users.user_id', ondelete = 'CASCADE'))
	vendor_id = db.Column(db.Integer(), db.ForeignKey('Users.user_id', ondelete = 'CASCADE'))
	product_id = db.Column(db.Integer(), db.ForeignKey('Products.product_id', ondelete = 'CASCADE'))
	location = db.Column(db.String(50))
	amount = db.Column(db.Integer())
	comment = db.Column(db.String(100))
	status = db.Column(db.String(15))
	order_time = db.Column(db.DateTime(), default = datetime.utcnow)

	def __init__(self, customer_id, vendor_id, product_id, location, amount, comment):
		self.customer_id = customer_id
		self.vendor_id = vendor_id
		self.product_id = product_id
		self.location = location
		self.amount = amount
		self.comment = comment
		self.status = 'Pendiente'

	def save_to_db(self):
		"""
		Permite guardar o actualizar los detalles de la orden en la base de datos.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina la orden de la base de datos.
		"""
		db.session.delete(self)
		db.session.commit()
