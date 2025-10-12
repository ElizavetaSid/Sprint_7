import requests
from helpers import CourierGenerator
from curl import URL


class TestCourierCreation:

    def test_successful_courier_creation(self):
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data
        
        login, password, first_name = courier_data
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(URL.CREATING_COURIER, data=payload)

        assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
        assert response.json() == {"ok": True}, "Тело ответа не соответствует {'ok': true}"


    def test_create_courier_missing_login(self):
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data, "Предусловие не выполнено: вспомогательный метод не вернул данные"
        
        login, password, first_name = courier_data
        payload = {
            # "login" отсутствует
            "password": password,
            "firstName": first_name
        }
        response = requests.post(URL.CREATING_COURIER, data=payload)
        assert response.status_code == 400, f"Недостаточно данных для создания учетной записи"

    def test_create_courier_missing_password(self):
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data, "Предусловие не выполнено: вспомогательный метод не вернул данные"
        
        login, password, first_name = courier_data
        payload = {
            "login": login,
            # "password" отсутствует
            "firstName": first_name
        }
        response = requests.post(URL.CREATING_COURIER, data=payload)
        assert response.status_code == 400, f"Недостаточно данных для создания учетной записи"

    def test_create_duplicate_courier_409(self):
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data

        login, password, first_name = courier_data
    
    # Шаг 2: Повторно пытаемся создать курьера с точно такими же данными
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        first_response = requests.post(URL.CREATING_COURIER, data=payload)
        assert first_response.status_code == 201, "Первый курьер не создан"

        duplicate_response = requests.post(URL.CREATING_COURIER, data=payload)
    
    # Шаг 3: Проверяем, что сервер вернул ошибку 409 Conflict
        assert duplicate_response.status_code == 409, f"Ожидался 409, получен код : {duplicate_response.status_code}"
