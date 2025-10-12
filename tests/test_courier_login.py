import requests
from helpers import CourierGenerator
from curl import URL
from data import ErrorMessages
import allure 

class TestCourierLogin:

    @allure.title('Тест успешной авторизации и получения id')
    def test_successful_courier_login_returns_id(self):
        with allure.step('Создать курьера'):
            courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data is not None, "Не удалось создать курьера для теста"
        
        login, password, first_name = courier_data
        create_payload = {"login": login, "password": password, "firstName": first_name}
        create_response = requests.post(URL.CREATING_COURIER, data=create_payload)
        
        with allure.step('Проверить создание курьера и код ошибки'):
            assert create_response.status_code == 201
        
        with allure.step('Проверить что при входе, возвращается id'):
            login_payload = {"login": login, "password": password}
        response = requests.post(URL.COURIER_LOGIN, data=login_payload)
    
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
    
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)
        
    @allure.title('Тест авторизации с неверным логином')
    def test_login_with_incorrect_login(self):
        
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data is not None
        
        _, password, _ = courier_data
        payload = {"login": "error_login", "password": password}
        response = requests.post(URL.COURIER_LOGIN, data=payload)
        
        assert response.status_code in [404, 400], f"Ожидался код 404 или 400, получен {response.status_code}"
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text

    @allure.title('Тест авторизации с неверным паролем')
    def test_login_with_incorrect_password(self):
        
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data is not None, "Не удалось создать курьера для теста"
        
        login, _, _ = courier_data
        payload = {"login": login, "password": "wrong_password"}
        response = requests.post(URL.COURIER_LOGIN, data=payload)
        
        assert response.status_code in [404, 400], f"Ожидался код 404 или 400, получен {response.status_code}"
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text
    
    
    @allure.title('Тест авторизации без логина')
    def test_login_without_login_field(self):
        
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data is not None
        
        _, password, first_name = courier_data
        payload = {"password": password, "first_name": first_name}
        response = requests.post(URL.COURIER_LOGIN, data=payload)
        
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        assert ErrorMessages.COURIER_ID_REQUIRED in response.text

    @allure.title('Тест авторизации без пароля')
    def test_login_without_password_field(self):
        
        courier_data = CourierGenerator.register_new_courier_and_return_login_password()
        assert courier_data is not None
        
        login, _, first_name = courier_data
        payload = {"login": login, "first_name": first_name}
        response = requests.post(URL.COURIER_LOGIN, data=payload)
        
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        assert ErrorMessages.COURIER_ID_REQUIRED in response.text

    @allure.title('Тест авторизации несуществующим пользователем')
    def test_login_with_nonexistent_user_returns_error(self):
        
        payload = {"login": "pupsik_123", "password": "pupsik456789"}
        response = requests.post(URL.COURIER_LOGIN, data=payload, timeout=30)
        
        assert response.status_code == 404, f"Ожидался код 404 или 400, получен {response.status_code}"
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text
