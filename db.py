"""
Este módulo proporciona el objeto que permite trabajar sobre la base de datos. Evita circular imports.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
