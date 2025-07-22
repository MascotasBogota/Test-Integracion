from playwright.sync_api import sync_playwright
import time
import json
import random
import os

USUARIO_JSON = "usuario_test.json"

def generar_datos_usuario():
    numero = random.randint(1000, 9999)
    return {
        "nombre": f"Usuario Test {numero}",
        "correo": f"usuario_test_{numero}@correo.com",
        "password": "Test1234"
    }

def guardar_datos(usuario):
    with open(USUARIO_JSON, "w", encoding="utf-8") as f:
        json.dump(usuario, f, indent=2)
    print(f"💾 Datos guardados en {os.path.abspath(USUARIO_JSON)}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    context = browser.new_context(viewport={"width": 1500, "height": 800})
    page = context.new_page()

    usuario = generar_datos_usuario()
    guardar_datos(usuario)

    print("🔗 Abriendo ruta raíz `/`...")
    page.goto("http://localhost:5173")
    time.sleep(1)

    print("📝 Registrando usuario desde /")
    page.get_by_test_id("navbar-register-link").first.click()
    time.sleep(1)

    page.get_by_test_id("signup-email-button").first.click()
    time.sleep(1)

    page.get_by_test_id("signup-name-input").fill(usuario["nombre"])
    page.get_by_test_id("signup-email-input").fill(usuario["correo"])
    page.get_by_test_id("signup-password-input").fill(usuario["password"])
    page.get_by_test_id("signup-confirm-password-input").fill(usuario["password"])
    time.sleep(1)

    page.get_by_test_id("signup-submit-button").click()
    page.wait_for_url("**/login", timeout=10000)
    print("✅ Usuario registrado. Redirigido al login.")
    time.sleep(1)

    print("🔐 Iniciando sesión...")
    page.get_by_test_id("login-email-input").fill(usuario["correo"])
    page.get_by_test_id("login-password-input").fill(usuario["password"])
    time.sleep(1)
    page.get_by_test_id("login-submit-button").click()

    page.wait_for_url("**/home", timeout=10000)
    print("🏠 En home.")
    time.sleep(2)

    print("📋 Creando reporte...")
    page.get_by_test_id("create-report-button").click()
    time.sleep(2)

    page.get_by_placeholder("Escribe el nombre de tu mascota").fill("Rafael")
    page.locator("select").select_option("Gato")
    page.get_by_placeholder("Escribe los detalles importantes").fill("Se perdió en el parque.")
    time.sleep(1)
    # Esperar el mapa y hacer clic centrado
    mapa = page.locator(".mapa")
    mapa.wait_for()
    box = mapa.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    time.sleep(1.5)

    page.set_input_files("input[type=file]", "mascota.jpg")
    time.sleep(1)

    page.mouse.click(700, 500)
    time.sleep(1)

    page.get_by_role("button", name="Crear").click()
    page.wait_for_url("**/home", timeout=10000)
    print("✅ Reporte creado.")
    time.sleep(2)

    print("📂 Navegando a Mis Reportes")
    page.get_by_test_id("my-reports-button").click()
    time.sleep(5)

    print("🗑️ Eliminando reporte...")
    page.locator("[data-testid='report-card']").nth(0).click()
    time.sleep(5)
    page.locator("img[alt='trash']").click()
    time.sleep(2)

    print("📋 Creando segundo reporte...")
    page.get_by_test_id("create-report-button").click()
    time.sleep(2)

    page.get_by_placeholder("Escribe el nombre de tu mascota").fill("Firulais")
    page.locator("select").select_option("Perro")
    page.get_by_placeholder("Escribe los detalles importantes").fill("Se perdió en el parque.")
    time.sleep(1)
    # Esperar el mapa y hacer clic centrado
    mapa = page.locator(".mapa")
    mapa.wait_for()
    box = mapa.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    time.sleep(1.5)

    page.set_input_files("input[type=file]", "mascota2.jpg")
    time.sleep(1)

    page.mouse.click(700, 500)
    time.sleep(1)

    page.get_by_role("button", name="Crear").click()
    page.wait_for_url("**/home", timeout=10000)
    print("✅ Reporte creado.")

    print("✏️ Editando segundo reporte...")
    page.get_by_test_id("my-reports-button").click()
    time.sleep(2)
    page.locator("[data-testid='report-card']").nth(0).click()
    time.sleep(2)
    page.locator("img[alt='pencil']").click()
    time.sleep(2)
    page.get_by_placeholder("Escribe los detalles importantes").fill("Actualización: lo vieron anoche cerca de casa.")
    time.sleep(1)
    page.get_by_role("button", name="Actualizar").click()
    time.sleep(6)

    print("🔚 Cerrando sesión...")
    page.get_by_test_id("navbar-logout-button").first.click()
    time.sleep(3)
    print("✅ Sesión cerrada.")

    browser.close()
