class ErrorMessages:
    # Класс для хранения всех текстов ошибок API

    # Ошибки создания и работы с курьерами
    LOGIN_ALREADY_EXISTS = "Этот логин уже используется"
    NOT_ENOUGH_DATA_FOR_CREATE = "Недостаточно данных для создания учетной записи"
    COURIER_NOT_FOUND = "Курьера с таким id нет"
    COURIER_ID_REQUIRED = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
    INVALID_INPUT_SYNTAX = "invalid input syntax"
    # Успешные сообщения
    OK_TRUE = '{"ok":true}'
    TRACK_FIELD = "track"

class DataOrder:
    order_data= {
        'firstname': 'Елизавета',
        'lastName': 'Сидельникова',
        'address': 'Юбилейный 62',
        'metroStation': 4,
        'phone': '89272182207',
        'rentTime': 3,
        'deliveryDate': '2025-10-15',
        'comment': 'Боюсь самокатов'
    }