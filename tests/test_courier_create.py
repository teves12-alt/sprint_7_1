import allure
import requests
from config import BASE_URL

@allure.feature("Создание курьера")
class TestCourierCreate:

    @allure.title("Курьер успешно создаётся, возвращается ok:true и код 201")
    def test_create_success(self, courier_data):
        response = requests.post(f"{BASE_URL}/courier", json=courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_duplicate_login_fails(self, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": "otherpass",
            "firstName": "Other",
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 409

    @allure.title("Ошибка, если не передано обязательное поле (login)")
    def test_missing_login_returns_error(self, courier_data):
        payload = {
            "password": courier_data["password"],
            "firstName": courier_data["firstName"],
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code in (400, 422)

    @allure.title("Ошибка, если не передано обязательное поле (password)")
    def test_missing_password_returns_error(self, courier_data):
        payload = {
            "login": courier_data["login"],
            "firstName": courier_data["firstName"],
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code in (400, 422)