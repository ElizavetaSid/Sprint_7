import requests
from helpers import CourierGenerator
from curl import URL
from data import ErrorMessages
import allure 

class TestCourierLogin:

    @allure.title('Тест успешной авторизации и получения id')
    def test_successful_courier_login_returns_id(self,register_new_courier_and_return_login_password):
        with allure.step('Создать курьера'):
            login, password, first_name = register_new_courier_and_return_login_password
        
            login_payload = {"login": login, "password": password}
            response = requests.post(URL.COURIER_LOGIN, data=login_payload)
        
        with allure.step('Проверить успешную авторизацию'):
            assert response.status_code == 200
    
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)
        
    @allure.title('Тест авторизации с неверным логином')
    def test_login_with_incorrect_login(self, register_new_courier_and_return_login_password):
        
        login, password, first_name = register_new_courier_and_return_login_password
        payload = {"login": "error_login", "password": password, "first_name": first_name}
        response = requests.post(URL.COURIER_LOGIN, data=payload)
        
        assert response.status_code in [404, 400], f"Ожидался код 404 или 400, получен {response.status_code}"
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text

    @allure.title('Тест авторизации с неверным паролем')
    def test_login_with_incorrect_password(self, register_new_courier_and_return_login_password):
        
        login, password, first_name = register_new_courier_and_return_login_password
        payload = {"login": login, "password": "wrong_password", "first_name": first_name}
        response = requests.post(URL.COURIER_LOGIN, data=payload)
        
        assert response.status_code in [404, 400], f"Ожидался код 404 или 400, получен {response.status_code}"
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text
    
    
    @allure.title('Тест авторизации без логина')
    def test_login_without_login_field(self,generate_courier_data):
        
        login, password, first_name = generate_courier_data
        payload = {"password": password, "first_name": first_name}
        response = requests.post(URL.COURIER_LOGIN, data=payload)
        
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        assert ErrorMessages.COURIER_ID_REQUIRED in response.text

    @allure.title('Тест авторизации без пароля')
    def test_login_without_password_field(self, generate_courier_data):

        login, password, first_name = generate_courier_data
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
