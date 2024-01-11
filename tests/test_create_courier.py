from methods import create_courier, generate_courier_payload, verify_response_code

import allure
import pytest


class TestCreateCourier:

    @allure.title('Успешная регистрация курьера возвращает код 201 и ответ ok:true')
    def test_courier_creation_is_successful(self):
        payload = generate_courier_payload()
        response = create_courier(payload)
        verify_response_code(response, 201)
        assert response.json()["ok"] is True
        assert len(response.json()) == 1

    @allure.title('Регистрация курьера с недостающим обязательным полем завершается ошибкой')
    @pytest.mark.parametrize(
        "exclude_login,exclude_password,exclude_first_name",
        [
            (True, False, False),
            (False, True, False),
            (False, False, True)
        ]
    )
    def test_missing_required_field_returns_error(self, exclude_login, exclude_password, exclude_first_name):
        payload = generate_courier_payload(
            exclude_login=exclude_login,
            exclude_password=exclude_password,
            exclude_first_name=exclude_first_name
        )
        response = create_courier(payload)
        verify_response_code(response, 400)
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title('Повторная регистрация существующего курьера завершается ошибкой')
    def test_register_existing_login_response_code(self):
        payload = generate_courier_payload()
        response = create_courier(payload)  # Регистрируем курьера
        verify_response_code(response, 201)
        response = create_courier(payload)  # Регистрируем курьера второй раз
        verify_response_code(response, 409)
        assert response.json()["message"] == "Этот логин уже используется"
