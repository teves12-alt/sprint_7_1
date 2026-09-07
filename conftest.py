import pytest
import random
import string
import requests
from config import BASE_URL

@pytest.fixture
def courier_data():
    """Только генерирует уникальные данные. Ничего не отправляет."""
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    return {
        "login": f"courier_{suffix}",
        "password": f"pass_{suffix}",
        "firstName": f"Name_{suffix}",
    }

@pytest.fixture
def registered_courier(courier_data):
    """
    Создает курьера ПЕРЕД тестом.
    Удаляет курьера ПОСЛЕ теста (даже если тест упал).
    Идеально для требования наставника.
    """
    data = courier_data
    
    # --- SETUP ---
    response = requests.post(f"{BASE_URL}/courier", json=data)
    
    if response.status_code == 201:
        pass  # Отлично, создан
    elif response.status_code == 409:
        pass  # Ок, уже есть (устойчивость к порядку запуска)
    else:
        pytest.fail(f"Не удалось подготовить курьера: статус {response.status_code}")
    
    yield data  # Отдаем данные тесту
    
    # --- TEARDOWN (Очистка) ---
    try:
        # Логинимся, чтобы получить ID для удаления
        login_resp = requests.post(f"{BASE_URL}/courier/login", json={"login": data["login"], "password": data["password"]})
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            if courier_id:
                requests.delete(f"{BASE_URL}/courier/{courier_id}")
    except Exception as e:
        print(f"⚠️ Warning: Failed to cleanup courier {data['login']}: {e}")
