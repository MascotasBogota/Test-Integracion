# Directorio de Pruebas de Integración y Funcionalidad

Este directorio contiene los scripts necesarios para ejecutar pruebas automatizadas contra los microservicios del proyecto y generar reportes en formato PDF con los resultados.

## Requisitos Previos

Antes de ejecutar cualquier prueba, asegúrate de tener todos los microservicios corriendo. Luego, instala las dependencias de Python necesarias:

```bash
pip install -r requirements.txt
```

## Tipos de Pruebas

Existen dos conjuntos de pruebas que se pueden ejecutar de forma independiente.

### 1. Pruebas de Integración Principal

Estas pruebas simulan un flujo de usuario completo a través de los servicios principales: registro, login, creación de reportes/respuestas y calificación.

- **Para ejecutar las pruebas y generar el reporte**, usa el siguiente comando:
  ```bash
  python generate_report.py
  ```
- **Resultado**: Se generará un archivo llamado `Test_Report_Enhanced.pdf` con el resumen visual de los resultados.

### 2. Pruebas de Funcionalidad Extendida

Estas pruebas verifican endpoints y funcionalidades específicas que no forman parte del flujo principal, como el ciclo CRUD completo de reportes, la actualización de perfiles y el marcado de notificaciones como leídas.

- **Para ejecutar estas pruebas y generar su reporte**, usa el comando:
  ```bash
  python generate_extended_report.py
  ```
- **Resultado**: Se generará un archivo `Test_Report_Extended_Functionality.pdf` con los detalles.

## Descripción de los Archivos

- `test_full_integration.py`: Contiene el script de prueba para el flujo de integración principal.
- `generate_report.py`: Orquesta la ejecución de `test_full_integration.py` y genera el reporte PDF correspondiente.
- `test_extended_functionality.py`: Contiene las pruebas para funcionalidades específicas y endpoints adicionales.
- `generate_extended_report.py`: Orquesta la ejecución de `test_extended_functionality.py` y genera su reporte en PDF.
- `test_password_change.py`: Un script de prueba aislado para la funcionalidad de cambio de contraseña.
- `requirements.txt`: Lista las dependencias de Python necesarias para ejecutar las pruebas y generar los reportes.
- `unal.png`: Logo utilizado en los reportes en PDF.
