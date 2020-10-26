"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de órdenes.
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.order import OrderModel
from models.product import ProductModel
from constants import user_types, admitted_order_states

class Order(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar pedidos.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('status',
		type = str,
		required = True,
		choices = admitted_order_states,
		help = f'Solo se puede marcar el pedido como: {admitted_order_states!r}.'
	)

	@jwt_required()
	def get(self, order_id: int):
		"""
		Devuelve los detalles de un pedido, solo si el usuario quien lo realizó o es el vendedor del producto.
		"""
		order = OrderModel.find_by_id(order_id)
		if not order:
			return {"message": f"El pedido con ID {order_id!r} no ha sido encontrado."}, 404

		if order.customer_id != current_identity.id and order.vendor_id != current_identity.id:
			return {"message": "No tiene permitido consultar el pedido."}, 401

		return order.json()

	@jwt_required()
	def put(self, order_id: int):
		"""
		Permite actualizar el estado del pedido. Lo puede hacer el vendedor del producto.
		"""
		order = OrderModel.find_by_id(order_id)
		if not order:
			return {"message": f"El pedido con ID {order_id!r} no ha sido encontrado."}, 404

		if current_identity.id != order.vendor_id:
			return {"message": "No tiene permitido finalizar este pedido."}, 401

		data = Order.parser.parse_args()

		order.status = data['status']
		order.save_to_db()

		return order.json()

	@jwt_required()
	def delete(self, order_id: int):
		"""
		Permite eliminar el pedido de forma que este se cancele. Puede ser realizado por quien hizo el pedido.
		"""
		order = OrderModel.find_by_id(order_id)
		if not order:
			return {"message": f"El pedido con ID {order_id!r} no ha sido encontrado."}, 404

		if current_identity.id != order.customer_id:
			return {"message": "No tiene permitido cancelar este pedido."}, 401

		order.delete_from_db()
		return {"message": f"Pedido con ID {order_id!r} eliminado correctamente."}

class OrderList(Resource):
	"""
	Esta clase maneja los métodos HTTP para trabajar sobre la lista de pedidos.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('product_id', type = int, required = True, help = 'El ID del producto es requerido.')
	parser.add_argument('location', type = str, required = True, help = 'El ubicación para entregar es requerida.')
	parser.add_argument('amount', type = int, required = True, help = 'La cantidad es requerida.')
	parser.add_argument('comment', type = str, default = '', help = 'Comentario para el vendedor (opcional).')

	@jwt_required()
	def get(self):
		"""
		Devuelve la lista de pedidos hechos por un usuario, si es vendedor, la lista de pedidos recibidos.
		"""
		if current_identity.user_type == user_types['vendor']:
			return [order.json() for order in OrderModel.get_by_vendor(current_identity.id)]
		return [order.json() for order in OrderModel.get_by_customer(current_identity.id)]

	@jwt_required()
	def post(self):
		"""
		Permite realizar un nuevo pedido, los vendedores no pueden realizarlos.
		"""
		if current_identity.user_type == user_types['vendor']:
			return {"message": "No tiene permitido realizar pedidos."}, 401

		data = OrderList.parser.parse_args()
		product = ProductModel.find_by_id(data['product_id'])
		if not product:
			return {"message": f"El producto con ID {data['product_id']!r} no ha sido encontrado."}, 404

		if data['amount'] <= 0:
			return {"message": f"La cantidad ({data['amount']}) no es válida."}, 400

		new_order = OrderModel(current_identity.id, product.user_id, **data)
		new_order.save_to_db()

		return new_order.json(), 201
