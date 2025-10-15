import pytest
import random
import string
import requests
from curl import URL
import allure

@pytest.fixture
def generate_courier_data():
    """Генерирует случайные данные для создания курьера"""
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    return login, password, first_name

@pytest.fixture
def register_new_courier_and_return_login_password(generate_courier_data):
    """Фикстура для создания курьера с последующим удалением после теста"""
    login, password, first_name = generate_courier_data
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    with allure.step(f"Создаем тестового курьера {login}"):
        response = requests.post(URL.CREATING_COURIER, data=payload)
        assert response.status_code == 201, f"Не удалось создать курьера, статус: {response.status_code}"
    
    # Возвращаем данные тесту
    yield login, password, first_name
    
    # Этот код выполнится после завершения теста
    with allure.step(f"Удаляем тестового курьера {login}"):
            # Логинимся чтобы получить ID курьера
        login_payload = {"login": login, "password": password}
        login_response = requests.post(URL.COURIER_LOGIN, data=login_payload)
            
        login_response.status_code == 200
        courier_id = login_response.json()["id"]
                # Удаляем курьера
        delete_response = requests.delete(f"{URL.CREATING_COURIER}/{courier_id}")