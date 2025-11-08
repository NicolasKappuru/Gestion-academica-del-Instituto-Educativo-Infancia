# Gestion-academica-del-Instituto-Educativo-Infancia
Este softaware provee de un sistema de gestion academica para el Instituto Educativo Infancia. Donde el cuerpo directivo de la institucion, profesores y acudientes pueden manejar y consultar informacion sobre el desepeño de los niños a cargo del instituto.

## Para crear el entorno
python -m venv env

## Para activar el entorno (en windows)
.\env\Scripts\Activate.ps1

## Migrar la BD, una vez que la tengas creada en postgres con las mismas credenciales que se encuentran en el core/setting.py. A continuacion un ejemplo con el componente de usuarios. 

python manage.py makemigrations usuarios
python manage.py migrate





