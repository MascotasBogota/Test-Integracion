from playwright.sync_api import sync_playwright
import time
import random

def generar_segundo_usuario():
    numero = random.randint(10000, 99999)
    return {
        "correo": f"segundo_usuario_{numero}@correo.com",
        "password": "Test1234",
        "nombre": f"Segundo Usuario {numero}"
    }

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    context = browser.new_context(viewport={"width": 1500, "height": 800})
    page = context.new_page()

    usuario = generar_segundo_usuario()

    print("📥 Registrando segundo usuario")
    page.goto("http://localhost:5173")
    time.sleep(1)

    page.get_by_test_id("navbar-register-link").first.click()
    time.sleep(1)
    page.get_by_test_id("signup-email-button").click()
    page.get_by_test_id("signup-name-input").fill(usuario["nombre"])
    page.get_by_test_id("signup-email-input").fill(usuario["correo"])
    page.get_by_test_id("signup-password-input").fill(usuario["password"])
    page.get_by_test_id("signup-confirm-password-input").fill(usuario["password"])
    time.sleep(1)
    page.get_by_test_id("signup-submit-button").click()

    page.wait_for_url("**/login", timeout=10000)
    print("🔐 Iniciando sesión...")
    page.get_by_test_id("login-email-input").fill(usuario["correo"])
    page.get_by_test_id("login-password-input").fill(usuario["password"])
    time.sleep(1)
    page.get_by_test_id("login-submit-button").click()
    page.wait_for_url("**/home", timeout=10000)
    print("✅ Segundo usuario en /home")
    time.sleep(2)

    print("📑 Abriendo un reporte cualquiera...")
    page.locator("[data-testid='report-card']").nth(0).click()
    page.wait_for_url("**/reportes/**", timeout=10000)
    time.sleep(2)

    print("📍 Creando avistamiento...")
    page.get_by_role("link", name="Avistamiento").click()
    page.wait_for_url("**/sighting/**", timeout=10000)
    page.get_by_placeholder("Escribe los detalles importantes").fill("Lo vi cerca del parque, parecía asustado.")
    mapa = page.locator(".mapa")
    mapa.wait_for()
    box = mapa.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    time.sleep(1.5)
    page.get_by_role("button", name="Enviar").click()
    page.wait_for_url("**/reportes/**", timeout=10000)
    print("✅ Avistamiento creado.")
    time.sleep(2)

    print("📍 Creando hallazgo...")
    page.get_by_role("link", name="Encontrado").click()
    page.wait_for_url("**/found/**", timeout=10000)
    page.get_by_placeholder("Escribe los detalles importantes").fill("Lo encontré y lo tengo en casa, está a salvo.")
    mapa = page.locator(".mapa")
    mapa.wait_for()
    box = mapa.bounding_box()
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    time.sleep(1.5)
    page.set_input_files("input[type=file]", "mascota.jpg")
    time.sleep(1)
    page.get_by_role("button", name="Enviar").click()
    page.wait_for_url("**/reportes/**", timeout=10000)
    print("✅ Hallazgo creado.")
    time.sleep(2)

    print("✏️ Editando avistamiento desde icono...")
    page.locator("img[alt='pencil-response']").nth(0).click()
    page.wait_for_url("**/sighting_edit/**", timeout=10000)
    page.get_by_placeholder("Escribe los detalles importantes").fill("Actualización: lo vi cerca del parque anoche.")
    page.get_by_role("button", name="Enviar").click()
    time.sleep(2)
    print("✅ Avistamiento actualizado.")

    print("✏️ Editando hallazgo desde icono...")
    page.locator("img[alt='pencil-response']").nth(1).click()
    page.wait_for_url("**/found_edit/**", timeout=10000)
    page.get_by_placeholder("Escribe los detalles importantes").fill("Actualización: el perro está en el refugio de la 123.")
    page.get_by_role("button", name="Enviar").click()
    time.sleep(2)
    print("✅ Hallazgo actualizado.")

    print("🗑️ Eliminando hallazgo desde icono...")
    page.locator("img[alt='trash-response']").nth(1).click()
    time.sleep(3)

    print("🔚 Cerrando sesión...")
    page.get_by_test_id("navbar-logout-button").first.click()
    time.sleep(3)
    print("👋 Sesión cerrada.")

    browser.close()
