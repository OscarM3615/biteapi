"""
Este módulo contiene las expresiones regulares necesarias para validar datos utilizados en la API.
"""

import re

identityRegex = re.compile(r'^[a-záéíóúñ]{1,20}$', re.IGNORECASE)
emailRegex = re.compile(r'^[A-Za-z0-9_\-]+(\.[A-Za-z0-9_\-]+)*@([A-Za-z0-9_\-]+\.)+[a-z]{2,5}$')
passwordRegex = re.compile(r'.{4,}')
