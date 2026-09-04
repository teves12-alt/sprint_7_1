import allure
import pytest
import requests
from config import BASE_URL
from data import (
    ORDER_PAYLOAD_BLACK,
    ORDER_PAYLOAD_GREY,
    ORDER_PAYLOAD_BOTH_COLORS,
    ORDER_PAYLOAD_NO_COLOR,
)


@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("Заказ успешно создаётся с различными цветами: {color_description}")
    @pytest.mark.parametrize(
        "payload, color_description",
        [
            (ORDER_PAYLOAD_BLACK, "BLACK"),
            (ORDER_PAYLOAD_GREY, "GREY"),
            (ORDER_PAYLOAD_BOTH_COLORS, "BOTH COLORS"),
            (ORDER_PAYLOAD_NO_COLOR, "NO COLOR"),
        ],
        ids=[
            "black_scooter",
            "grey_scooter",
            "both_colors",
            "no_color"
        ]
    )
    def test_order_create_various_colors(self, payload, color_description):
        # Шаг 1: Отправка запроса
        with allure.step(f"Отправляем запрос на создание заказа с цветом: {color_description}"):
            response = requests.post(f"{BASE_URL}/orders", json=payload)

        # Шаг 2: Проверка статуса
        with allure.step("Проверяем, что статус код равен 201"):
            assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"

        # Шаг 3: Проверка тела ответа
        with allure.step("Проверяем, что в ответе есть поле 'track' и оно является числом"):
            body = response.json()
            
            assert "track" in body, "В ответе отсутствует обязательное поле 'track'"
            
            track_value = body["track"]
            assert isinstance(track_value, int), f"Поле 'track' должно быть целым числом, получено: {type(track_value).__name__}"
            
            # Дополнительный бонус: можно проверить, что track > 0 (если бизнес-логика требует)
            assert track_value > 0, f"Поле 'track' должно быть положительным числом, получено: {track_value}"

