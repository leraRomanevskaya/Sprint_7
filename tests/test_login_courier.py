from methods import get_registered_courier_credentials, get_not_registered_courier_credentials, login_courier, \
    verify_response_code

import allure
import pytest


class TestLoginCourier:
    @allure.title('Успешный залогин возвращает код 200 и ответ с id')
    def test_auth_success(self):
        credentials = get_registered_courier_credentials()
        response = login_courier(credentials)
        verify_response_code(response, 200)
        assert isinstance(response.json()["id"], int)

    @allure.title('Попытка залогина без логина или пароля завершается ошибкой')
    @pytest.mark.parametrize(
        "exclude_login,exclude_password",
        [
            (True, False),
            (False, True)
        ]
    )
    def test_auth_without_one_credential_returns_error_status_code(self, exclude_login, exclude_password):
        credentials = get_registered_courier_credentials(exclude_login=exclude_login, exclude_password=exclude_password)
        response = login_courier(credentials)
        verify_response_code(response, 400)
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Попытка залогина с неправильным паролем возвращает код 404')
    def test_auth_wrong_password_returns_error_status_code(self):
        credentials = get_registered_courier_credentials(corrupt_password=True)
        response = login_courier(credentials)
        verify_response_code(response, 404)
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Попытка залогина для несуществующего логина возвращает код 404')
    def test_auth_not_registered_courier_returns_error_status_code(self):
        credentials = get_not_registered_courier_credentials()
        response = login_courier(credentials)
        verify_response_code(response, 404)
        assert response.json()["message"] == "Учетная запись не найдена"
