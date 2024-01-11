import allure
import json
import random
import requests
import string


@allure.step('Генерируем учётные данные курьера')
def generate_courier_payload(exclude_login=False, exclude_password=False, exclude_first_name=False):
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    payload = {}

    if not exclude_login:
        payload["login"] = generate_random_string(10)

    if not exclude_password:
        payload["password"] = generate_random_string(10)

    if not exclude_first_name:
        payload["firstName"] = generate_random_string(10)

    return payload


@allure.step('Получаем пару логин-пароль существующего курьера')
def get_registered_courier_credentials(
        exclude_login=False,
        exclude_password=False,
        corrupt_password=False,
):
    credentials = {}

    if not exclude_login:
        credentials["login"] = "login-test-777"

    if not exclude_password:
        credentials["password"] = "password-test-777" if not corrupt_password else "corrupt-password"

    return credentials


@allure.step('Получаем пару логин-пароль НЕ существующего курьера')
def get_not_registered_courier_credentials():
    return {
        "login": "not-registered-login",
        "password": "not-registered-password"
    }


@allure.step('Создаём курьера [POST]')
def create_courier(payload) -> requests.Response:
    return requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)


@allure.step('Залогин курьера [POST]')
def login_courier(credentials) -> requests.Response:
    return requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=credentials)


@allure.step('Создаём заказ [POST]')
def create_order(color=None) -> requests.Response:
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha"
    }
    if color:
        payload["color"] = color
    return requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', data=json.dumps(payload))


@allure.step('Загружаем список заказов [GET]')
def get_orders_list(params=None) -> requests.Response:
    return requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders', params=params)


@allure.step('Проверяем код ответа сервера')
def verify_response_code(response: requests.Response, code: int):
    assert response.status_code == code

