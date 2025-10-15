import requests
from curl import URL
import allure

class TestCourierCreation:

    @allure.title("Тест успешного создания курьера")
    def test_successful_courier_creation(self, generate_courier_data):
        login, password, first_name = generate_courier_data
    
        payload = {
            "login": login,
            "password": password, 
            "firstName": first_name
         }
        
        response = requests.post(URL.CREATING_COURIER, data=payload)
    
        with allure.step('Проверяем код статуса 201 и правильное тело ответа'):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
            assert response.json() == {"ok": True}, "Тело ответа не соответствует {'ok': true}"
  
        requests.delete(f"{URL.CREATING_COURIER}/{login}")

    @allure.title('Тесты на отсутствие обязательных полей')
    @allure.description('Тест без логина. Тест без пароля')
    def test_create_courier_missing_login(self, generate_courier_data):
        login, password, first_name = generate_courier_data
        
        payload = {
            # "login" отсутствует
            "password": password,
            "firstName": first_name
        }
        response = requests.post(URL.CREATING_COURIER, data=payload)
        assert response.status_code == 400, f"Недостаточно данных для создания учетной записи"

    def test_create_courier_missing_password(self, generate_courier_data):
        login, password, first_name = generate_courier_data
    
        payload = {
            "login": login,
            # "password" отсутствует
            "firstName": first_name
        }
        response = requests.post(URL.CREATING_COURIER, data=payload)
        assert response.status_code == 400, f"Недостаточно данных для создания учетной записи"

    @allure.title('Тест создания дубликата курьера')
    def test_create_duplicate_courier_409(self, generate_courier_data):
        login, password, first_name = generate_courier_data
    
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        with allure.step('Создаем курьера первый раз'):
            first_response = requests.post(URL.CREATING_COURIER, data=payload)
            assert first_response.status_code == 201, "Первый курьер не создан"
        with allure.step('Пытаемся создать курьера с теми же данными второй раз'):
            duplicate_response = requests.post(URL.CREATING_COURIER, data=payload)
            assert duplicate_response.status_code == 409, f"Ожидался 409, получен код : {duplicate_response.status_code}"

        with allure.step('Удаляем тестового курьера'):
            login_payload = {"login": login, "password": password}
            login_response = requests.post(URL.COURIER_LOGIN, data=login_payload)
        
        login_response.status_code == 200
        courier_id = login_response.json()["id"]
        requests.delete(f"{URL.CREATING_COURIER}/{courier_id}")