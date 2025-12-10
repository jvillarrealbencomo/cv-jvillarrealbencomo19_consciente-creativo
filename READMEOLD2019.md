# CV Interactivo - Versión 2019

Este proyecto fue iniciado en 2019 como una aplicación Flask para mostrar mi currículum de forma interactiva. En ese momento, trabajaba con una cuenta de GitHub asociada al correo [javiervillarrealbencomo@gmail.com], la cual perdí temporalmente.

## Funcionalidades originales

- Menú principal con secciones: Inicio, Educación, Experiencia, Productos TI, Apoyo, Cursos, Datos personales, Documentos.
- Submenú de documentos: Títulos, Certificados laborales, Certificaciones, Listado.
- Renderizado con plantillas HTML y recursos estáticos.
- Visualización de documentos asociados (imágenes).
- Servidor local Flask en 127.0.0.1:5000.

## Nota sobre el correo

La cuenta original de GitHub quedó inaccesible por pérdida de contraseña. En 2025, recuperé el acceso al correo porque el proyecto lo tenía en un correo y en el drive y de allí recuperé el proyecto y no recuperé desde la cuenta de github por olvidar contraseña, pero decidí continuar el portafolio con una nueva cuenta para evitar más retrasos.

Este archivo preserva la historia técnica y personal del proyecto original.


# 📌 Guion rápido para alternar entre CV 2019 y CV 2025

## 🔹 CV 2019 (rama `master`, entorno Python 3.9)
```powershell
# Activar entorno histórico
.\venv39\Scripts\activate

# Cambiar a la rama original
git checkout master

# Instalar dependencias (solo la primera vez)
python -m pip install -r src/requirements.txt

# Ejecutar la aplicación
python src/index.py

# Activar entorno moderno
.\venv311\Scripts\activate

# Cambiar a la rama actualizada
git checkout version-2025
# o si estás integrando:
git checkout cv2019-integration

# Ejecutar la aplicación
python run.py
