import allure
import requests

from config import BASE_URL


@allure.feature("Создание курьера")
class TestCourierCreate:

    @allure.title("Курьер успешно создаётся: проверка шагов регистрации")
    def test_create_success(self, created_courier_for_test):
        """
        ВАЖНО: Этот тест САМ выполняет шаги регистрации.
        Фикстура created_courier_for_test только:
          1. Отдаёт уникальные данные (логин, пароль, имя).
          2. Гарантирует очистку (удаление) курьера ПОСЛЕ теста через блок teardown.

        Мы НЕ полагаемся на то, что фикстура что-то создала ДО теста.
        Мы сами делаем POST-запрос здесь, чтобы честно протестировать эндпоинт создания.
        """
        data = created_courier_for_test

        # ШАГ 1: Выполняем действие (создаём курьера)
        with allure.step("Отправляем POST-запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}/courier", json=data)

        # ШАГ 2: Проверяем результат действия (статус код)
        with allure.step("Проверяем, что сервер вернул статус 201 Created"):
            assert response.status_code == 201, (
                f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"
            )

        # ШАГ 3: Проверяем тело ответа
        with allure.step("Проверяем, что в ответе сервера ok: true"):
            body = response.json()
            assert body == {"ok": True}, (
                f"Ожидался ответ 'ok': True, получен: {body}"
            )

       

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_duplicate_login_fails(self, registered_courier):
     
        payload = {
            "login": registered_courier["login"],
            "password": "otherpass123",
            "firstName": "Other Name",
        }

        with allure.step("Пытаемся создать дубликат курьера с тем же логином"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяем, что сервер отвергает дубликат (статус 409)"):
            assert response.status_code == 409, (
                f"Ожидался статус 409, получен {response.status_code}. Ответ: {response.text}"
            )

    @allure.title("Ошибка, если не передано обязательное поле (login)")
    def test_missing_login_returns_error(self, courier_data):
        """
        Для негативных тестов нам не нужно, чтобы курьер реально существовал.
        Достаточно просто уникальных данных из простой фикстуры courier_data.
        """
        payload = {
            "password": courier_data["password"],
            "firstName": courier_data["firstName"],
        }

        with allure.step("Отправляем запрос без обязательного поля 'login'"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяем, что сервер возвращает ошибку 400"):
            assert response.status_code == 400, (
                f"Ожидался статус 400, получен {response.status_code}. Ответ: {response.text}"
            )

    @allure.title("Ошибка, если не передано обязательное поле (password)")
    def test_missing_password_returns_error(self, courier_data):
        """
        Негативный тест: проверяем реакцию API на отсутствие пароля.
        """
        payload = {
            "login": courier_data["login"],
            "firstName": courier_data["firstName"],
        }

        with allure.step("Отправляем запрос без обязательного поля 'password'"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяем, что сервер возвращает ошибку 400"):
            assert response.status_code == 400, (
                f"Ожидался статус 400, получен {response.status_code}. Ответ: {response.text}"
            )

