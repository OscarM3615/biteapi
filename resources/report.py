"""
Este módulo contiene las clases necesarias para permitir el acceso a los datos de reportes.
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.report import ReportModel
from models.user import UserModel
from constants import user_types

class Report(Resource):
	"""
	Esta clase maneja los métodos HTTP para modificar reportes.
	"""
	@jwt_required()
	def get(self, report_id: int):
		"""
		Devuelve los datos de un reporte específico, incluyendo los datos del usuario reportado. Solo admins.
		"""
		if current_identity.user_type != user_types['admin']:
			return {"message": "No tiene permitido consultar reportes."}, 401
		
		report = ReportModel.find_by_id(report_id)
		if not report:
			return {"message": f"El reporte con ID {report_id!r} no ha sido encontrado."}, 404
		return report.json()

	@jwt_required()
	def delete(self, report_id: int):
		"""
		Elimina un reporte de la base de datos. Solo admins.
		"""
		if current_identity.user_type != user_types['admin']:
			return {"message": "No tiene permitido eliminar reportes."}, 401

		report = ReportModel.find_by_id(report_id)
		if not report:
			return {"message": f"El reporte con ID {report_id!r} no ha sido encontrado."}, 404

		report.delete_from_db()
		return {"message": f"Reporte con ID {report_id!r} eliminado correctamente."}

class ReportList(Resource):
	"""
	Esta clase manejar los métodos HTTP para trabajar sobre la lista de reportes.
	"""
	parser = reqparse.RequestParser()
	parser.add_argument('user_id', type = int, required = True, help = 'El ID del usuario a reportar es requerido.')
	parser.add_argument('comment', type = str, required = True, help = 'Es necesario justificar el reporte.')

	@jwt_required()
	def get(self):
		"""
		Devuelve la lista de reportes, incluyendo los datos del usuario reportado. Solo admins.
		"""
		if current_identity.user_type != user_types['admin']:
			return {"message": "No tiene permitido consultar reportes."}, 401
		return [report.json() for report in ReportModel.get_all()]

	@jwt_required()
	def post(self):
		"""
		Crea un nuevo reporte sobre un usuario.
		"""
		data = ReportList.parser.parse_args()
		if not UserModel.find_by_id(data['user_id']):
			return {"message": f"El usuario con ID {data['user_id']!r} no existe."}, 404
		
		new_report = ReportModel(**data)
		new_report.save_to_db()

		return new_report.json(), 201