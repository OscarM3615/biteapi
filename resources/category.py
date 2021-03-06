"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de categorías.
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.category import CategoryModel
from constants import user_types

class Category(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar categorías.
	"""
	@jwt_required()
	def get(self, category_id: int):
		"""
		Obtener los datos de una categoría.
		"""
		category = CategoryModel.find_by_id(category_id)
		if not category:
			return {"message": f"La categoría con ID {category_id!r} no ha sido encontrada."}, 404
		return category.json()

	@jwt_required()
	def delete(self, category_id: int):
		"""
		Eliminar una categoría de la base de datos (Solo los admin pueden hacerlo).
		"""
		if current_identity.user_type != user_types['admin']:
			return {"message": "No tiene permitido eliminar una categoría."}, 401

		category = CategoryModel.find_by_id(category_id)
		if not category:
			return {"message": "La categoría no ha sido encontrada."}, 404

		category.delete_from_db()
		return {"message": f"Categoría con ID {category_id!r} eliminada correctamente."}

class CategoryList(Resource):
	"""
	Esta clase maneja los métodos HTTP para trabajar sobre la lista de categorías.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('name', type = str, required = True, help = 'El nombre de la categoría es requerido.')

	@jwt_required()
	def get(self):
		"""
		Obtener la lista de categorías existentes.
		"""
		return [category.json() for category in CategoryModel.get_all()]

	@jwt_required()
	def post(self):
		"""
		Agregar una nueva categoría (Solo los admin pueden hacerlo).
		"""
		if current_identity.user_type != user_types['admin']:
			return {"message": "No tiene permitido crear nuevas categorías."}, 401

		data = CategoryList.parser.parse_args()
		if CategoryModel.find_by_name(data['name']):
			return {"message": f"La categoría {data['name']!r} ya existe."}, 400

		new_category = CategoryModel(**data)
		new_category.save_to_db()

		return new_category.json(), 201
