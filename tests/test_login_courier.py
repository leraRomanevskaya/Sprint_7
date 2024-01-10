from methods import get_registered_courier_credentials, get_not_registered_courier_credentials, login_courier,\
    verify_response_code

import pytest


def test_auth_success_returns_success_status_code():
    credentials = get_registered_courier_credentials()
    response = login_courier(credentials)
    verify_response_code(response, 200)


def test_auth_success_returns_id():
    credentials = get_registered_courier_credentials()
    response = login_courier(credentials)
    assert isinstance(response.json()["id"], int)


@pytest.mark.parametrize(
    "exclude_login,exclude_password",
    [
        (True, False),
        (False, True)
    ]
)
def test_auth_without_one_credential_returns_error_status_code(exclude_login, exclude_password):
    credentials = get_registered_courier_credentials(exclude_login=exclude_login, exclude_password=exclude_password)
    response = login_courier(credentials)
    verify_response_code(response, 400)


def test_auth_wrong_password_returns_error_status_code():
    credentials = get_registered_courier_credentials(corrupt_password=True)
    response = login_courier(credentials)
    verify_response_code(response, 404)


def test_auth_not_registered_courier_returns_error_status_code():
    credentials = get_not_registered_courier_credentials()
    response = login_courier(credentials)
    verify_response_code(response, 404)
