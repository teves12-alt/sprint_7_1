import pytest
import random
import string
import requests
from config import BASE_URL



@pytest.fixture
def courier_data():
   
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    return {
        "login": f"courier_{suffix}",
        "password": f"pass_{suffix}",
        "firstName": f"Name_{suffix}",
    }


# 2. Сложная фикстура: готовит курьера (создаёт) и убирает за собой (удаляет)
@pytest.fixture
def registered_courier(courier_data):
    data = courier_data
    
    # --- ЭТАП ПОДГОТОВКИ (SETUP) ---
    # Пытаемся создать курьера
    response = requests.post(f"{BASE_URL}/courier", json=data)

    if response.status_code == 201:
        pass  # Отлично, курьер создан заново
    elif response.status_code == 409:
        pass  # Ок, курьер уже есть (например, база не очистилась). 
              # Мы НЕ падаем здесь, чтобы тест был устойчивым к порядку запуска.
    else:
        # Если сервер вернул что-то совсем странное (500, 400 и т.д.) — падаем
        pytest.fail(
            f"Не удалось подготовить курьера: статус {response.status_code}, "
            f"ответ: {response.text}"
        )
    
    # ВАЖНО: yield отдаёт данные тесту и ставит выполнение на паузу
    yield data 
    
    # --- ЭТАП ОЧИСТКИ (TEARDOWN) ---
    # Этот блок выполнится ВСЕГДА после завершения теста (даже если тест упал)
    try:
        # Сначала нужно залогиниться, чтобы получить ID курьера для удаления
        login_resp = requests.post(
            f"{BASE_URL}/courier/login",
            json={"login": data["login"], "password": data["password"]},
        )
        
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            if courier_id:
                # Удаляем курьера
                delete_resp = requests.delete(f"{BASE_URL}/courier/{courier_id}")
                # Можно добавить проверку статуса удаления, если API это гарантирует
        else:
            # Если не смогли залогиниться, курьер может остаться в базе.
            # Выводим предупреждение, но не ломаем тест, чтобы видеть реальные баги
            print(f"⚠️ WARNING: Failed to login for cleanup. Courier '{data['login']}' might still exist. Status: {login_resp.status_code}")
            
    except Exception as e:
        # Ловим любые сетевые ошибки или таймауты
        print(f"⚠️ WARNING: Unexpected error during cleanup for courier '{data['login']}': {e}")

