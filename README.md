# Test de Integración

Este directorio contiene los scripts para ejecutar pruebas de integración y generar un reporte con los resultados.

## Pasos para la ejecución

### 1. Instalar dependencias

Asegúrate de tener todas las librerías necesarias instalando los `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar las pruebas y generar el reporte

Para correr las pruebas de integración y generar el reporte en PDF, ejecuta el siguiente script:

```bash
python generate_report.py
```

Esto generará un archivo llamado `Test_Report.pdf` con el resumen de los resultados.

## Contenido de los Scripts

A continuación se muestra el contenido de los scripts principales.

### `test_login.py`

```python
# -*- coding: utf-8 -*-
import requests

# Configuración
BASE_URL = "http://localhost:5000/api"
BASE_URL_2 = "http://localhost:5050"
BASE_URL_3 = "http://localhost:5010"
BASE_URL_4 = "http://localhost:5100/api"

# --- Función para registrar un nuevo usuario ---
def register_user(full_name, email, password):
    """Registra un nuevo usuario y devuelve True si tiene éxito."""
    print(f"[REGISTRO] Registrando al usuario: {email}")
    register_data = {
        "full_name": full_name,
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=register_data)
        if response.status_code == 201:
            print(f"[OK] Usuario {email} registrado exitosamente.")
            return True
        else:
            # Si el usuario ya existe (409), lo consideramos válido para poder loguear
            if response.status_code == 409:
                print(f"[INFO] Usuario {email} ya estaba registrado.")
                return True
            print(f"[ERROR] Error registrando a {email}: {response.status_code} -> {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexión al registrar a {email}: {e}")
        return False

# --- Función para hacer login ---
def login_user(email, password):
    """Inicia sesión con un usuario y muestra el resultado."""
    print(f"[LOGIN] Intentando iniciar sesión como: {email}")
    login_data = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"[OK] Login exitoso para {email}")
            if token:
                print(f"      Token (inicio): {token}")
                return token
            else:
                print("      (No se recibió token)")
                return None
        else:
            print(f"[ERROR] Falló el login para {email}. Estado: {response.status_code} | Respuesta: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Ocurrió un error de conexión durante el login de {email}: {e}")
        return None

# --- Funciones para Reportes y Respuestas ---
def create_report(token, report_data):
    """Crea un nuevo reporte y devuelve el ID del reporte si tiene éxito."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL_2}/reports/", json=report_data, headers=headers)
        if response.status_code == 201:
            report_id = response.json().get("_id")
            print(f"[OK] Reporte creado exitosamente con ID: {report_id}")
            return report_id
        else:
            print(f"[ERROR] Error al crear el reporte: {response.status_code} -> {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexión al crear el reporte: {e}")
        return None

def create_response(token, report_id, response_data):
    """Crea una respuesta a un reporte y devuelve el ID de la respuesta si tiene éxito."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL_2}/responses/{report_id}", json=response_data, headers=headers)
        if response.status_code == 201:
            response_id = response.json().get("id")
            print(f"[OK] Respuesta creada exitosamente para el reporte {report_id} con ID: {response_id}")
            return response_id
        else:
            print(f"[ERROR] Error al crear la respuesta: {response.status_code} -> {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexión al crear la respuesta: {e}")
        return None

# --- Funciones para Notificaciones ---
def get_notifications(token):
    """Consulta las notificaciones para un usuario."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL_3}/notifications/", headers=headers)
        if response.status_code == 200:
            notifications = response.json()
            print(f"[OK] Notificaciones recibidas: {notifications}")
            return notifications
        else:
            print(f"[ERROR] Error al obtener notificaciones: {response.status_code} -> {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexión al obtener notificaciones: {e}")
        return None

# --- Funciones para Reputación de Usuario ---
def rate_response(token, report_id, response_id, rating):
    """Califica una respuesta y devuelve True si tiene éxito."""
    headers = {"Authorization": f"Bearer {token}"}
    rating_data = {"rating": rating}
    try:
        response = requests.post(f"{BASE_URL_4}/rate-response/{report_id}/{response_id}", json=rating_data, headers=headers)
        if response.status_code == 200:
            print(f"[OK] Respuesta calificada exitosamente.")
            return True
        else:
            print(f"[ERROR] Error al calificar la respuesta: {response.status_code} -> {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexión al calificar la respuesta: {e}")
        return False


def get_user_profile(token):
    """Obtiene el perfil de un usuario y devuelve su reputación."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            reputation = profile_data.get("profile", {}).get("reputation")
            print(f"[OK] Perfil de usuario obtenido. Reputación: {reputation}")
            return reputation
        else:
            print(f"[ERROR] Error al obtener el perfil del usuario: {response.status_code} -> {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexión al obtener el perfil del usuario: {e}")
        return None

# --- Script principal ---
def main():
    print("--- Iniciando Test de Integración Completo ---")

    # Datos de los usuarios de prueba
    user_a = {"full_name": "Usuario A - test", "email": "userA3@example.com", "password": "PasswordA123"}
    user_b = {"full_name": "Usuario B - test", "email": "userB3@example.com", "password": "PasswordB123"}

    # Fase 1: Registro
    print("\n--- Fase 1: Registro de usuarios ---")
    register_user(user_a["full_name"], user_a["email"], user_a["password"])
    register_user(user_b["full_name"], user_b["email"], user_b["password"])

    # Fase 2: Login y obtención de tokens
    print("\n--- Fase 2: Login y obtención de tokens ---")
    token_a = login_user(user_a["email"], user_a["password"])
    token_b = login_user(user_b["email"], user_b["password"])

    if not token_a or not token_b:
        print("\n[ERROR] No se pudieron obtener los tokens para ambos usuarios. Abortando.")
    else:
        # Fase 3: Usuario A crea un reporte
        print("\n--- Fase 3: Usuario A crea un reporte ---")
        report_data = {
            "pet_name": "Fido",
            "type": "perro",
            "description": "Perro perdido, color negro.",
            "location": {"type": "Point", "coordinates": [-74.08, 4.6]},
            "images": []
        }
        report_id = create_report(token_a, report_data)

        if report_id:
            # Fase 4: Usuario B responde al reporte
            print("\n--- Fase 4: Usuario B responde al reporte ---")
            response_data = {
                "type": "avistamiento",
                "comment": "Lo vi cerca del parque Esta es la buenaaaaa.",
                "location": {"type": "Point", "coordinates": [-74.07, 4.65]},
                "images": []
            }
            response_id = create_response(token_b, report_id, response_data)

            if response_id:
                # Fase 5: Usuario A califica la respuesta de Usuario B
                print("\n--- Fase 5: Usuario A califica la respuesta de Usuario B ---")
                rate_response(token_a, report_id, response_id, "useful")

                # Fase 6: Consultar reputación de Usuario B
                print("\n--- Fase 6: Consultar reputación de Usuario B ---")
                get_user_profile(token_b)

    print("\n--- Test de Integración Finalizado ---")

if __name__ == "__main__":
    main()
```

### `generate_report.py`

```python
import os
import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import test_login

def run_tests_and_get_results():
    """
    Runs the integration tests and returns a summary of the results.
    """
    # Redirect stdout to capture the output of the tests
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    # Run the main test script
    test_login.main()

    # Restore stdout
    sys.stdout = old_stdout

    # Get the output
    output = captured_output.getvalue()
    
    # Process the output to get results
    results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for line in output.split('\n'):
        if "[OK]" in line:
            results["passed"] += 1
            results["details"].append(line)
        elif "[ERROR]" in line:
            results["failed"] += 1
            results["details"].append(line)
    
    results["total_tests"] = results["passed"] + results["failed"]
    
    return results, output

def generate_chart(results, filename="test_results.png"):
    """
    Generates a bar chart of the test results.
    """
    labels = ['Passed', 'Failed']
    values = [results['passed'], results['failed']]
    
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['green', 'red'])
    plt.title('Test Results Summary')
    plt.ylabel('Number of Tests')
    plt.savefig(filename)
    plt.close()
    
    return filename

def generate_pdf_report(results, chart_filename, detailed_output, filename="Test_Report.pdf"):
    """
    Generates a PDF report with the test results and chart.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # --- Insertar logo ---
    try:
        logo_path = "unal.png"
        logo = ImageReader(logo_path)
        logo_width = 100
        logo_height = 100
        logo_x = 40
        logo_y = height - logo_height - 40  # Deja espacio superior
        c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)
    except Exception as e:
        print(f"[WARNING] No se pudo cargar el logo: {e}")

    # --- Título y fecha alineados a la derecha del logo ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(logo_x + logo_width + 20, height - 50, "Integration Test Report")

    c.setFont("Helvetica", 12)
    c.drawString(logo_x + logo_width + 20, height - 70, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- Gráfica ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(logo_x, height - 160, "Test Results Summary")
    c.drawImage(ImageReader(chart_filename), logo_x, height - 370, width=400, height=200)

    # --- Log detallado ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(logo_x, height - 400, "Detailed Log")

    c.setFont("Helvetica", 9)
    text = c.beginText(logo_x, height - 420)
    for line in detailed_output.split('\n'):
        text.textLine(line)
    c.drawText(text)

    c.save()
    print(f"PDF report generated: {filename}")

def main():
    """
    Main function to run tests and generate the report.
    """
    print("Running integration tests...")
    results, detailed_output = run_tests_and_get_results()
    
    print("Generating chart...")
    chart_filename = generate_chart(results)
    
    print("Generating PDF report...")
    generate_pdf_report(results, chart_filename, detailed_output)
    
    # Clean up the chart image
    os.remove(chart_filename)

if __name__ == "__main__":
    main()
```