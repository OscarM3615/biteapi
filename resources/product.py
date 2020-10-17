"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de productos.
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.product import ProductModel
from regex import base64Regex

class Product(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar productos.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('category_id', type = int, required = True, help = 'El ID de la categoría es requerido.')
	parser.add_argument('name', type = str, required = True, help = 'El nombre es requerido.')
	parser.add_argument('description', type = str, required = True, help = 'La descripción es requerida.')
	parser.add_argument('price', type = float, required = True, help = 'El precio es requerido.')
	parser.add_argument('image', type = str, required = True, help = 'La imagen es requerida.')
	parser.add_argument('visible', type = bool, required = True, help = 'La visibilidad para los demás usuarios es requerida.')

	@jwt_required()
	def get(self, product_id: int):
		"""
		Devuelve los detalles de un producto si este es visible o pertenece al usuario.
		"""
		product = ProductModel.find_by_id(product_id)
		if not product:
			return {"message": f"El producto con ID {product_id!r} no ha sido encontrado."}, 404
		
		if product.user_id != current_identity.id and product.visible == False:
			return {"message": "No tiene permitido visualizar este producto."}, 401
		return product.json()

	@jwt_required()
	def put(self, product_id: int):
		"""
		Actualiza los detalles de un producto si pertenece al vendedor.
		"""
		product = ProductModel.find_by_id(product_id)
		if not product:
			return {"message": f"El producto con ID {product_id!r} no ha sido encontrado."}, 404
		
		if product.user_id != current_identity.id or current_identity.user_type != 'vendedor':
			return {"message": "No tiene permitido modificar este producto."}, 401

		data = Product.parser.parse_args()

		if base64Regex.match(data['image']) is None:
			return {"message": "La imagen debe ser base64 de tipo imagen."}, 400
		
		product.category_id = data['category_id']
		product.name = data['name']
		product.description = data['description']
		product.price = data['price']
		product.image = data['image']
		product.visible = data['visible']
		product.save_to_db()

		return product.json()

	@jwt_required()
	def delete(self, product_id: int):
		"""
		Elimina el producto de la base de datos si le pertenece al vendedor.
		"""
		product = ProductModel.find_by_id(product_id)
		if not product:
			return {"message": f"El producto con ID {product_id!r} no ha sido encontrado."}, 404
		
		if product.user_id != current_identity.id:
			return {"message": "No tiene permitido eliminar este producto."}, 401
		
		product.delete_from_db()
		return {"message": f"Producto con ID {product_id!r} eliminado correctamente."}

class ProductList(Resource):
	"""
	Esta clase maneja los métodos HTTP para trabajar sobre la lista de productos.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('category_id', type = int, required = True, help = 'El ID de la categoría es requerido.')
	parser.add_argument('name', type = str, required = True, help = 'El nombre es requerido.')
	parser.add_argument('description', type = str, required = True, help = 'La descripción es requerida.')
	parser.add_argument('price', type = float, required = True, help = 'El precio es requerido.')
	parser.add_argument('image', type = str, required = True, help = 'La imagen es requerida.')

	args = reqparse.RequestParser()
	args.add_argument('vendor_id', type = int, location = 'args')
	args.add_argument('category_id', type = int, location = 'args')
	args.add_argument('search', type = str, location = 'args')

	@jwt_required()
	def get(self):
		"""
		Devuelve la lista de productos existentes.
		"""
		data = ProductList.args.parse_args()
		return [product.json() for product in ProductModel.get_all(**data)]

	@jwt_required()
	def post(self):
		"""
		Agregar un nuevo producto a la base de datos. Permitir solo para vendedores.
		"""
		if current_identity.user_type != 'vendedor':
			return {"message": "Se requiere ser vendedor para agregar productos."}, 401

		data = ProductList.parser.parse_args()

		if base64Regex.match(data['image']) is None:
			return {"message": "La imagen debe ser base64 de tipo imagen."}, 400

		new_product = ProductModel(current_identity.id, **data)
		new_product.save_to_db()

		return new_product.json(), 201

class ProductStock(Resource):
	"""
	Esta clase se encarga de los métodos que devuelvan los productos de un vendedor.
	"""
	@jwt_required()
	def get(self, user_id: int):
		"""
		Devuelve la lista de productos de un vendedor, sean visibles o no. Solo lo puede realizar el mismo vendedor.
		"""
		if current_identity.id != user_id:
			return {"message": "No tiene permitido consultar la lista de productos."}, 401
		return [product.json() for product in ProductModel.get_by_user(user_id)]
