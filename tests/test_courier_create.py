import allure
import requests

from config import BASE_URL


@allure.feature("Создание курьера")
class TestCourierCreate:

    @allure.title("Курьер успешно создаётся (проверка сценария регистрации)")
    def test_create_success(self, registered_courier):
        """
        Используем фикстуру registered_courier. Она УЖЕ создала курьера ДО начала теста
        и ГАРАНТИРОВАННО удалит его ПОСЛЕ.
        """
        # 1. Проверяем, что данные полные
        assert "login" in registered_courier, "Отсутствует поле login в данных курьера"
        assert "password" in registered_courier, "Отсутствует поле password в данных курьера"
        assert "firstName" in registered_courier, "Отсутствует поле firstName в данных курьера"

        # 2. Дополнительная проверка: пробуем залогиниться этим курьером
        with allure.step("Проверяем, что созданный курьер может авторизоваться"):
            login_payload = {
                "login": registered_courier["login"],
                "password": registered_courier["password"],
            }
            response = requests.post(f"{BASE_URL}/courier/login", json=login_payload)

            assert response.status_code == 200, (
                f"Ожидался статус 200 при логине, получен {response.status_code}"
            )
            body = response.json()
            assert "id" in body, "В ответе авторизации отсутствует поле id"
            assert body.get("ok") is True, "Поле ok в ответе авторизации не равно true"

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_duplicate_login_fails(self, registered_courier):
        """
        Фикстура registered_courier уже создала курьера с уникальным логином.
        Мы пытаемся создать ВТОРОГО курьера с тем же логином.
        """
        payload = {
            "login": registered_courier["login"],
            "password": "otherpass123",
            "firstName": "Other Name",
        }

        with allure.step("Пытаемся создать дубликат курьера с тем же логином"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяем, что сервер отвергает дубликат (статус 409)"):
            assert response.status_code == 409, (
                f"Ожидался статус 409, получен {response.status_code}"
            )

    @allure.title("Ошибка, если не передано обязательное поле (login)")
    def test_missing_login_returns_error(self, courier_data):
        payload = {
            "password": courier_data["password"],
            "firstName": courier_data["firstName"],
        }

        with allure.step("Отправляем запрос без поля 'login'"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяем, что сервер возвращает ошибку 400"):
            assert response.status_code == 400, (
                f"Ожидался статус 400, получен {response.status_code}"
            )

    @allure.title("Ошибка, если не передано обязательное поле (password)")
    def test_missing_password_returns_error(self, courier_data):
        payload = {
            "login": courier_data["login"],
            "firstName": courier_data["firstName"],
        }

        with allure.step("Отправляем запрос без поля 'password'"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяем, что сервер возвращает ошибку 400"):
            assert response.status_code == 400, (
                f"Ожидался статус 400, получен {response.status_code}"
            )
