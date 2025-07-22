from playwright.sync_api import sync_playwright
import json
import time
import random
import os

USUARIO_JSON = "usuario_test.json"
NUEVO_JSON = "usuario_test_actualizado.json"
NUEVA_IMAGEN = "nueva_foto.jpg"

def cargar_usuario():
    with open(USUARIO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    context = browser.new_context(viewport={"width": 1500, "height": 800})
    page = context.new_page()

    usuario = cargar_usuario()

    print("🔐 Iniciando sesión...")
    page.goto("http://localhost:5173/login")
    page.get_by_test_id("login-email-input").fill(usuario["correo"])
    page.get_by_test_id("login-password-input").fill(usuario["password"])
    page.get_by_test_id("login-submit-button").click()
    page.wait_for_url("**/home", timeout=10000)
    print("✅ Sesión iniciada.")
    time.sleep(2)

    print("⚙️ Abriendo perfil...")
    page.get_by_test_id("navbar-profile-link").first.click()
    page.wait_for_url("**/perfil", timeout=10000)
    time.sleep(2)

    print("✏️ Editando perfil...")

    nuevo_nombre = f"{usuario['nombre']} Editado"
    nuevo_telefono = "3216549870"
    nueva_direccion = "Calle Falsa 123"
    nuevo_usuario = f"user{random.randint(1000,9999)}"
    nuevo_genero = "female"
    nuevo_correo = usuario["correo"]  # o cámbialo si quieres

    # Llenar todos los campos
    page.get_by_test_id("profile-name-input").fill(nuevo_nombre)
    page.get_by_test_id("profile-email-input").fill(nuevo_correo)
    page.get_by_test_id("profile-username-input").fill(nuevo_usuario)
    page.get_by_test_id("profile-phone-input").fill(nuevo_telefono)
    page.get_by_test_id("profile-direction-input").fill(nueva_direccion)
    page.get_by_test_id("profile-gender-select").select_option(nuevo_genero)


    print("🖼️ Subiendo nueva foto de perfil...")
    page.set_input_files("#fileInput", NUEVA_IMAGEN)
    time.sleep(2)

    print("💾 Guardando perfil...")
    page.get_by_role("button", name="Guardar cambios").click()
    time.sleep(3)
    
    print("⚙️ Abriendo perfil...")
    page.get_by_test_id("navbar-profile-link").first.click()
    page.wait_for_url("**/perfil", timeout=10000)
    time.sleep(2)

    # CAMBIO DE CONTRASEÑA
    print("🔒 Cambiando contraseña...")
    page.get_by_role("link", name="Cambiar contraseña").click()
    page.wait_for_url("**/change_password", timeout=10000)
    time.sleep(2)

    password_actual = usuario["password"]
    password_nueva = "NuevaPass123"
    confirmacion = "NuevaPass123"

    page.get_by_test_id("current-pass").fill(password_actual)
    page.get_by_test_id("pass").fill(password_nueva)
    page.get_by_test_id("confirm-pass").fill(confirmacion)
    page.get_by_role("button", name="Reestablecer").click()

    print("✅ Contraseña actualizada.")
    time.sleep(6)
    
    
    print("🔚 Cerrando sesión...")
    page.get_by_test_id("navbar-logout-button").first.click()
    time.sleep(4)
    print("✅ Sesión cerrada.")

    # GUARDAR DATOS ACTUALIZADOS
    usuario_actualizado = {
        "nombre": nuevo_nombre,
        "correo": nuevo_correo,
        "password": password_nueva,
        "username": nuevo_usuario,
        "telefono": nuevo_telefono,
        "direccion": nueva_direccion,
        "genero": nuevo_genero
    }

    with open(NUEVO_JSON, "w", encoding="utf-8") as f:
        json.dump(usuario_actualizado, f, indent=2)
        print(f"💾 Datos actualizados guardados en {os.path.abspath(NUEVO_JSON)}")

    print("🎉 Perfil y contraseña actualizados correctamente.")
    browser.close()
