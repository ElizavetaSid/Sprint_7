class URL:
    MAIN_URL = 'https://qa-scooter.praktikum-services.ru/'      # Главная страница "Яндекс Самокат"
    COURIER_LOGIN = (MAIN_URL+'api/v1/courier/login')      # POST-Запрос на Логин курьера в системе
    CREATING_COURIER = (MAIN_URL+'api/v1/courier')        # POST-Запрос на Создание курьера
    CREATING_ORDER = (MAIN_URL+'api/v1/orders')           # POST-Запрос для Создания заказа
    GETTING_LIST_ORDERS = (MAIN_URL+'api/v1/orders')          # GET-Запрос для Получения списка заказов
    CANCEL_ORDER = (MAIN_URL+'api/v1/orders/cancel')        #PUT-Запрос на отмену заказа