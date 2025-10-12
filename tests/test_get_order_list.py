import requests
import allure
from data import *
from curl import *


class TestsGetOrdersList:

    @allure.title('Тест на проверку получения списка заказов')
    def test_get_orders_list(self):
        with allure.step('Отправить GET-запрос для получения списка заказов'):
            response = requests.get(URL.GETTING_LIST_ORDERS)

        with allure.step('Проверить статус код ответа'):
            assert response.status_code == 200

        response_data = response.json()
        
        with allure.step('Проверяем, что ответ содержит список заказов'):
            assert 'orders' in response_data
            assert isinstance(response_data['orders'], list)

        with allure.step('Если есть заказы, проверяем структуру первого заказа'):
            if len(response_data['orders']) > 0:
                first_order = response_data['orders'][0]
            
            with allure.step('Проверяем обязательные поля в заказе (на основе общих практик API)'):
                assert 'id' in first_order
                assert 'track' in first_order