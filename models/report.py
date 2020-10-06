"""
Este módulo contiene la clase para hacer cambios sobre los reportes en la base de datos.
"""

from db import db

class ReportModel(db.Model):
	"""
	Ocurre cuando un usuario reporta a un vendedor por un comportamineto inadecuado.
	"""
	__tablename__ = 'Reports'

	report_id = db.Column(db.Integer(), primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete = 'CASCADE'))
	comment = db.Column(db.String(150), nullable = False)

	def __init__(self, user_id: int, comment: str):
		self.user_id = user_id
		self.comment = comment
	
	def json(self):
		return {
			"report_id": self.report_id,
			"comment": self.comment,
			"user": self.user.json()
		}

	@classmethod
	def find_by_id(cls, report_id: int):
		return cls.query.filter_by(report_id = report_id).first()

	@classmethod
	def get_all(cls):
		return cls.query.all()

	def save_to_db(self):
		"""
		Guarda los detalles del reporte generado. No se puede modificar aunque el método lo permita.
		"""
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		"""
		Elimina el reporte de la base de datos.
		"""
		db.session.delete(self)
		db.session.commit()
