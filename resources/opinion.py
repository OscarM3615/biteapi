"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de opiniones.
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.opinion import OpinionModel
from models.product import ProductModel
from constants import user_types, rating_values

class Opinion(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar opiniones.
	"""
	@jwt_required()
	def get(self, product_id: int, opinion_id: int):
		"""
		Devuelve los datos de una opinión por separado.
		"""
		opinion = OpinionModel.find_by_id(opinion_id)
		if not opinion:
			return {"message": f"La opinión con ID {opinion_id!r} no ha sido encontrada."}, 404

		return opinion.json()

	@jwt_required()
	def delete(self, product_id: int, opinion_id: int):
		"""
		Borra una opinión de un producto por ser inadecuada. Solo pueden hacerlo los admins.
		"""
		if current_identity.user_type != user_types['admin']:
			return {"message": "No tiene permitido eliminar esta opinión."}, 401

		opinion = OpinionModel.find_by_id(opinion_id)
		if not opinion:
			return {"message": f"La opinión con ID {opinion_id!r} no ha sido encontrada."}, 404

		opinion.delete_from_db()
		return {"message": f"Opinión con ID {opinion_id!r} eliminada correctamente."}

class OpinionList(Resource):
	"""
	Esta clase maneja los métodos HTTP para trabajar sobre la lista de opiniones.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('product_id', type = int, required = True, help = 'El ID del producto es requerido.')
	parser.add_argument('rating',
		type = int,
		required = True,
		choices = rating_values,
		help = f'La calificación debe estar entre {rating_values[0]!r} y {rating_values[-1]!r}.'
	)
	parser.add_argument('comment', type = str, required = True, help = 'El comentario es requerido.')

	@jwt_required()
	def get(self, product_id: int):
		"""
		Devuelve la lista de opiniones de un producto.
		"""
		if not ProductModel.find_by_id(product_id):
			return {"message": f"El producto con ID {product_id!r} no ha sido encontrado."}, 404
		return [opinion.json() for opinion in OpinionModel.get_by_product(product_id)]

	@jwt_required()
	def post(self, product_id: int):
		"""
		Agrega una opinión a un producto en particular.
		"""
		if current_identity.user_type == user_types['vendor']:
			return {"message": "Un vendedor no puede realizar opiniones sobre los productos."}, 401

		if not ProductModel.find_by_id(product_id):
			return {"message": f"El producto con ID {product_id!r} no ha sido encontrado."}, 404

		data = OpinionList.parser.parse_args()

		new_opinion = OpinionModel(**data)
		new_opinion.save_to_db()

		return new_opinion.json(), 201
