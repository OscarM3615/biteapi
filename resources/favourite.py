"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de favoritos.
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.favourite import FavouriteModel
from models.product import ProductModel

class Favourite(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar favoritos.
	"""
	@jwt_required()
	def delete(self, favourite_id: int):
		"""
		Permite eliminar un favorito del usuario. Solo elimina la referencia, no al producto.
		"""
		favourite = FavouriteModel.find_by_id(favourite_id)
		if not favourite:
			return {"message": f"El favorito con ID {favourite_id!r} no ha sido encontrado."}, 404
		
		if favourite.user_id != current_identity.id:
			return {"message": "No tiene permitido eliminar este favorito."}, 401
		
		favourite.delete_from_db()
		return {"message": f"Favorito con ID {favourite_id!r} eliminado correctamente."}

class FavouriteList(Resource):
	"""
	Esta clase maneja los métodos HTTP para trabajar sobre la lista de favoritos.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('product_id', type = int, required = True, help = 'El ID del producto es requerido.')

	@jwt_required()
	def get(self):
		"""
		Devuelve la lista de productos favoritos del usuario.
		"""
		return [favourite.json() for favourite in FavouriteModel.get_by_user(current_identity.id)]

	@jwt_required()
	def post(self):
		"""
		Agrega un nuevo producto a los favoritos del usuario.
		"""
		if current_identity.user_type == 'vendedor':
			return {"message": "No puede marcar un producto como favorito."}, 401

		data = FavouriteList.parser.parse_args()
		
		if not ProductModel.find_by_id(data['product_id']):
			return {"message": f"El producto con ID {data['product_id']!r} no ha sido encontrado."}, 404
		if FavouriteModel.find_if_exists(current_identity.id, data['product_id']):
			return {"message": f"El producto con ID {data['product_id']!r} ya está marcado como favorito."}, 400

		new_favourite = FavouriteModel(current_identity.id, data['product_id'])
		new_favourite.save_to_db()

		return new_favourite.json()
