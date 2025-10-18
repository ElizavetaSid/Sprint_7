import requests
import pytest
from curl import URL
from data import DataOrder, ErrorMessages
import allure 

class TestOrderCreation:

    # Параметры для тестирования разных вариантов цветов
    @pytest.mark.parametrize('colors, test_description', [
        (['BLACK'], 'Заказ с черным самокатом'),
        (['GREY'], 'Заказ с серым самокатом'), 
        (['BLACK', 'GREY'], 'Заказ с двумя цветами'),
        ([], 'Заказ без указания цвета')
    ])
    @allure.title('Создание заказа с разными цветами: {test_description}')
    def test_create_order_with_different_colors(self, colors, test_description):
        
        with allure.step('Копируем базовые данные заказа'):
            order_payload = DataOrder.order_data.copy()
        
        with allure.step('Добавляем цвета если они указаны'):
            colors and order_payload.update({'color': colors})
        
        with allure.step('Отправляем запрос на создание заказа'):
            response = requests.post(URL.CREATING_ORDER, json=order_payload)
        
        with allure.step('Проверяем успешный статус код'):
            assert response.status_code == 201
        
        with allure.step('Проверяем, что в ответе есть track number'):
            response_data = response.json()
            assert ErrorMessages.TRACK_FIELD in response_data
        
        with allure.step('Получаем track_number из ответа'):
            track_number = response_data['track']

        with allure.step('Подготавливаем данные для отмены заказа'):
            cancel_payload = f"{URL.CANCEL_ORDER}?track={track_number}"
        
        with allure.step('Отправляем запрос на отмену заказа'):
            cancel_response = requests.put(cancel_payload)
        
        with allure.step('Проверяем успешную отмену заказа'):
            assert cancel_response.status_code == 200, f"Ожидался 200, получен {cancel_response.status_code}"
            
           