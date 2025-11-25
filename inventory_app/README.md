# Aplicación de Inventario (Manejo de Artículos)

Esta aplicación es una implementación mínima de los requisitos en `requisitos.md`.

Características
- Página inicial con botones: Asignar Artículo y Seguimiento
- Formularios para asignar artículos con los campos: Código, Descripción, Categoría, Unidad, Cantidad, Valor unitario y Valor total
- Página de seguimiento que lista los artículos en inventario
- Editar y eliminar artículos desde la página de seguimiento

Requisitos
- Python 3.8+

Instalación y ejecución (PowerShell)
```powershell
# Crear y activar entorno virtual (opcional, recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la app
python app.py
```

La aplicación quedará disponible en http://127.0.0.1:5000

Notas
- La base de datos se crea automáticamente como `inventory.db` en la carpeta del proyecto la primera vez que accede a la aplicación.
- En producción, use una clave secreta fuerte y un servidor web más robusto (Gunicorn, uWSGI, etc.).

Uso de datos de ejemplo
```powershell
# Solo si desea agregar datos de ejemplo
python seed.py
```

Importar desde Excel
```
La aplicación ahora incluye una opción para importar artículos desde un archivo Excel (.xlsx).
Use el botón "Importar desde Excel" en la página principal o vaya a /import. Puede usar el archivo de ejemplo `datos.xlsx` que incluye el proyecto; la hoja debe contener encabezados con: Código, Descripción de Artículo, Categoría, Unidad de medida, Cantidad, Valor Artículo (unitario), Valor total.
``` 
