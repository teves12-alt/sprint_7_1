import allure
import requests
from config import BASE_URL

@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Курьер успешно авторизуется, возвращается id и ok: true")
    def test_login_success(self, registered_courier):
        # Берем данные из фикстуры. Она уже создала курьера!
        login = registered_courier["login"]
        password = registered_courier["password"]

        # --- ШАГ 1: Подготовка и отправка ---
        with allure.step(f"Формируем payload и отправляем запрос на авторизацию для курьера {login}"):
            payload = {"login": login, "password": password}
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        # --- ШАГ 2: Проверка статуса ---
        with allure.step("Проверяем, что статус код ответа равен 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        # --- ШАГ 3: Проверка тела ответа ---
        with allure.step("Проверяем, что в ответе есть id и поле ok равно true"):
            body = response.json()
            
            # Проверка наличия ключа
            assert "id" in body, "В ответе отсутствует обязательное поле 'id'"
            
            # Проверка значения ok
            assert body.get("ok") is True, f"Поле 'ok' должно быть true, получено: {body.get('ok')}"
            
            # Бонус: можно проверить, что id — это число (если API гарантирует)
            assert isinstance(body["id"], int), "Поле 'id' должно быть целым числом"

