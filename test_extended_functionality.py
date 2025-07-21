# -*- coding: utf-8 -*-
import requests
import time

# Configuración de las URLs base para cada microservicio
BASE_URL_LOGIN = "http://localhost:5000/api"
BASE_URL_REPORTS = "http://localhost:5050"
BASE_URL_NOTIFICATIONS = "http://localhost:5010"

# --- Funciones de Cliente reutilizadas ---

def register_user(email, password, full_name="Test User"):
    try:
        response = requests.post(f"{BASE_URL_LOGIN}/users/register", json={"full_name": full_name, "email": email, "password": password})
        return response.status_code in [201, 409]
    except requests.exceptions.RequestException:
        return False

def login_user(email, password):
    try:
        response = requests.post(f"{BASE_URL_LOGIN}/users/login", json={"email": email, "password": password})
        return response.json().get('token') if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

# --- NUEVAS FUNCIONES DE TEST ---

def test_update_profile(token):
    print("\n--- Test: Actualizar Perfil de Usuario ---")
    new_name = f"NombreCambiado {int(time.time())}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        update_response = requests.put(f"{BASE_URL_LOGIN}/profile/", headers=headers, json={"full_name": new_name})
        if update_response.status_code != 200:
            print(f"[FAILURE] No se pudo actualizar el perfil: {update_response.text}")
            return False

        get_response = requests.get(f"{BASE_URL_LOGIN}/profile/", headers=headers)
        updated_name = get_response.json().get("profile", {}).get("full_name")
        if updated_name == new_name:
            print(f"[SUCCESS] El nombre del perfil se actualizó a: {updated_name}")
            return True
        else:
            print(f"[FAILURE] La verificación falló. Esperado: {new_name}, Obtenido: {updated_name}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[FATAL] Error de conexión: {e}")
        return False

def test_reports_crud(token):
    print("\n--- Test: CRUD de Reportes ---")
    headers = {"Authorization": f"Bearer {token}"}
    report_id = None
    try:
        report_data = {"pet_name": "TestPet", "type": "gato", "description": "Gato para CRUD test", "location": {"type": "Point", "coordinates": [1, 1]}}
        create_resp = requests.post(f"{BASE_URL_REPORTS}/reports/", headers=headers, json=report_data)
        if create_resp.status_code != 201:
            print(f"[FAILURE] CREATE fallido: {create_resp.text}")
            return False
        report_id = create_resp.json().get("_id")

        list_resp = requests.get(f"{BASE_URL_REPORTS}/reports/public", headers=headers)
        if list_resp.status_code != 200 or not any(r["_id"] == report_id for r in list_resp.json()):
            print(f"[FAILURE] READ (List) fallido")
            return False

        get_resp = requests.get(f"{BASE_URL_REPORTS}/reports/public/{report_id}", headers=headers)
        if get_resp.status_code != 200:
            print(f"[FAILURE] READ (One) fallido")
            return False

        update_data = {"description": "Nueva descripcion actualizada"}
        update_resp = requests.put(f"{BASE_URL_REPORTS}/reports/{report_id}", headers=headers, json=update_data)
        if update_resp.status_code != 200 or update_resp.json().get("description") != "Nueva descripcion actualizada":
            print(f"[FAILURE] UPDATE fallido")
            return False

        delete_resp = requests.delete(f"{BASE_URL_REPORTS}/reports/{report_id}", headers=headers)
        if delete_resp.status_code != 204:
            print(f"[FAILURE] DELETE fallido")
            return False

        print("[SUCCESS] CRUD de reportes ejecutado exitosamente.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[FATAL] Error de conexión: {e}")
        return False

def test_mark_notification_as_read(token_a, token_b):
    print("\n--- Test: Marcar Notificación como Leída ---")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    try:
        report_data = {"pet_name": "NotifyPet", "type": "perro", "description": "Test para notif", "location": {"type": "Point", "coordinates": [2, 2]}}
        create_resp = requests.post(f"{BASE_URL_REPORTS}/reports/", headers=headers_a, json=report_data)
        report_id = create_resp.json().get("_id")

        response_data = {"type": "avistamiento", "comment": "Lo vi cerca del parque TEST.", "location": {"type": "Point", "coordinates": [-74.07, 4.65]}, "images": []}
        requests.post(f"{BASE_URL_REPORTS}/responses/{report_id}", headers=headers_b, json=response_data)
        time.sleep(2)

        notif_resp = requests.get(f"{BASE_URL_NOTIFICATIONS}/notifications/", headers=headers_a)
        notifications = notif_resp.json()
        if not notifications or not notifications["data"]["notifications"]:
            print("[FAILURE] No se recibieron notificaciones.")
            return False

        notification_id = notifications["data"]["notifications"][0].get("id")
        mark_read_resp = requests.patch(f"{BASE_URL_NOTIFICATIONS}/notifications/{notification_id}/read", headers=headers_a)
        if mark_read_resp.status_code != 200:
            print(f"[FAILURE] No se pudo marcar como leída: {mark_read_resp.text}")
            return False

        print("[SUCCESS] Notificación marcada como leída exitosamente.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[FATAL] Error de conexión: {e}")
        return False

# --- Flujo Principal ---
def main():
    print("--- INICIANDO TEST DE FUNCIONALIDADES EXTENDIDAS ---")

    email_a = "extendedap.test.user.a@example.com"
    email_b = "extendedap.test.user.b@example.com"
    password = "Password123"

    register_user(email_a, password, "User A Extended")
    register_user(email_b, password, "User B Extended")
    token_a = login_user(email_a, password)
    token_b = login_user(email_b, password)

    if not (token_a and token_b):
        print("[FATAL] No se pudieron obtener los tokens. Abortando.")
        return

    passed = 0
    failed = 0

    if test_update_profile(token_a):
        passed += 1
    else:
        failed += 1

    if test_reports_crud(token_a):
        passed += 1
    else:
        failed += 1

    if test_mark_notification_as_read(token_a, token_b):
        passed += 1
    else:
        failed += 1

    print(f"\n--- TEST DE FUNCIONALIDADES EXTENDIDAS FINALIZADO ---")
    print(f"[SUMMARY] Total: {passed + failed} | [SUCCESS] {passed} | [FAILURE] {failed}")

if __name__ == "__main__":
    main()
