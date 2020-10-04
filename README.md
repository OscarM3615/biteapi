# Bite API #

API para la aplicación web progresiva para la venta de comida en Ciudad Juárez.

---

## Configuración del proyecto ##

### Clonar el repositorio ###

`$ git clone https://github.com/oscarmiranda3615/biteapp.git`

### Crear una entorno virtual dentro del repositorio (solo se realiza una vez) ###

`$ virtualenv venv`

*Es necesario que se llame __venv__, pues así está escrito en los archivos a excluir en cambios realizados*

### Activar el entorno virtual (cada vez que se va a trabajar en el repositorio) ###

Desde cmd:

`$ venv\Scripts\activate.bat`

Desde PowerShell:

`$ .\venv\Scripts\activate.ps1`

### Instalar las dependencias del proyecto ###

`$ pip install -r requirements.txt`

---

## Estructura base del proyecto ##

```
+ biteapi (Raíz del proyecto)
+	models (Código backend con acceso a la BD)
+		*.py
+	resources (Accesos a la API)
+		*.py
+	.gitignore (Archivos a excluir del repositorio)
+	.pylintrc (Configuración del linter)
+	app.py (Configuración de la API)
+	db.py (Configuración de la BD)
+	requirements.txt (Dependencias del proyecto)
```

---

## Extensiones recomendadas para Visual Studio Code ##

### Live Share (Microsoft) ###

> Colaboración en tiempo real sobre el proyecto.

[Ver en Marketplace](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare)

---

## Acerca de ##

Proyecto realizado por:

- [Óscar Miranda](https://github.com/OscarM3615)
- [André Marín](https://github.com/al180222)
