from methods import create_courier, generate_courier_payload, \
    verify_response_code, verify_response_returns_success, verify_response_returns_error

import pytest


def test_courier_creation_is_successful():
    payload = generate_courier_payload()
    response = create_courier(payload)
    verify_response_returns_success(response)


def test_successful_response_code():
    payload = generate_courier_payload()
    response = create_courier(payload)
    verify_response_code(response, 201)


def test_successful_response_body():
    payload = generate_courier_payload()
    response = create_courier(payload)
    assert response.json()["ok"] is True
    assert len(response.json()) == 1


def test_register_same_couriers_is_prohibited():
    payload = generate_courier_payload()
    response = create_courier(payload)  # Регистрируем курьера
    verify_response_returns_success(response)
    response = create_courier(payload)  # Регистрируем курьера второй раз
    verify_response_returns_error(response)


@pytest.mark.parametrize(
    "exclude_login,exclude_password,exclude_first_name",
    [
        (True, False, False),
        (False, True, False),
        (False, False, True)
    ]
)
def test_missing_required_field_returns_error(exclude_login, exclude_password, exclude_first_name):
    payload = generate_courier_payload(
        exclude_login=exclude_login,
        exclude_password=exclude_password,
        exclude_first_name=exclude_first_name
    )
    response = create_courier(payload)
    verify_response_returns_error(response)


@pytest.mark.parametrize(
    "exclude_login,exclude_password",
    [
        (True, False),
        (False, True),
    ]
)
def test_missing_field_response_code(exclude_login, exclude_password):
    payload = generate_courier_payload(exclude_login=exclude_login, exclude_password=exclude_password)
    response = create_courier(payload)
    verify_response_code(response, 400)


def test_register_existing_login_response_code():
    payload = generate_courier_payload()
    response = create_courier(payload)  # Регистрируем курьера
    verify_response_returns_success(response)
    response = create_courier(payload)  # Регистрируем курьера второй раз
    verify_response_code(response, 409)
