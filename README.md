# Gestión Académica del Instituto Educativo Infancia

Este software provee un sistema de gestión académica para el Instituto Educativo Infancia, permitiendo que el cuerpo directivo, profesores y acudientes puedan gestionar y consultar información relacionada con el desempeño académico de los niños a cargo del instituto.

El sistema está desarrollado como una aplicación backend en Django, orientada a la gestión de datos académicos.

---

## 🛠️ Tecnologías utilizadas

- Lenguaje de programación: Python  
- Framework: Django  
- Base de datos: PostgreSQL  
- IDE recomendado: Visual Studio Code  
- Entorno virtual: venv  
- Plataforma de despliegue: Render  

> Nota: En versiones anteriores del repositorio, el proyecto se ejecutaba únicamente de manera local.

---

## 📦 Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.10 o superior  
- PostgreSQL  
- Git  
- Visual Studio Code  

---

## 📚 Instalación de dependencias

Es obligatorio instalar las librerías necesarias listadas en el archivo `requirements.txt` para el correcto funcionamiento del proyecto.

```bash
pip install -r requirements.txt
```

---

## 🧪 Creación del entorno virtual

### Crear el entorno virtual
```bash
python -m venv env
```

### Activar el entorno (Windows)
```bash
.\env\Scripts\Activate.ps1
```

---

## 🗄️ Configuración de la base de datos

1. Crear una base de datos en PostgreSQL.
2. Configurar las credenciales en el archivo `core/settings.py`.

Asegúrate de que los datos de conexión coincidan con los de tu base de datos local o de despliegue.

---

## 🔄 Migraciones de la base de datos

Una vez configurada la base de datos, ejecuta las migraciones.  
Ejemplo para el componente de usuarios:

```bash
python manage.py makemigrations usuarios
python manage.py migrate
```

---

## ▶️ Ejecución del proyecto en entorno local

```bash
python manage.py runserver
```

Luego accede desde el navegador a:

```
http://127.0.0.1:8000/
```

---

## 🧠 Alimentación inicial de la base de datos (Recomendado)

Para un uso adecuado del sistema, se recomienda alimentar la base de datos utilizando los scripts personalizados que se encuentran en las carpetas `management/commands/` de algunas de las apps del proyecto.

Ejemplo genérico:
```bash
python manage.py nombre_del_script
```

---

## 🚀 Despliegue

El proyecto está configurado para su despliegue en la plataforma Render. Revisa los archivos de configuración del repositorio para los detalles específicos del despliegue.

---

## ✍️ Autores

- Nicolás Castro  
- Edison Álvarez  




