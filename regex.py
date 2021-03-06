"""
Este módulo contiene las expresiones regulares necesarias para validar datos utilizados en la API.
"""

import re

identityRegex = re.compile(r'^[a-záéíóúñ]{1,20}( [a-záéíóúñ]{1,20})?$', re.IGNORECASE)
emailRegex = re.compile(r'^[A-Za-z0-9_\-]+(\.[A-Za-z0-9_\-]+)*@([A-Za-z0-9_\-]+\.)+[a-z]{2,5}$')
passwordRegex = re.compile(r'.{4,}')
base64Regex = re.compile(r'data:image\/[^;]+;base64[^"]+')
imgurlRegex = re.compile(r'^https?:\/\/([\w\-]+\.)*[\w\-]+\.[a-z]+\/([\w\.\-\%]+\/)*[\w\.\-\%\(\)]+\.(jpe?g|png)(\?[\w\.\-\=\&]*)?$', re.IGNORECASE)
