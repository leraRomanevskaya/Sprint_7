from methods import get_orders_list, verify_response_code


def test_not_pass_courier_id_returns_orders_list():
    response = get_orders_list()
    verify_response_code(response, 200)
    assert isinstance(response.json()["orders"], list)


def test_pass_non_existent_courier_id_returns_error():
    non_existent_courier_id = 999999
    response = get_orders_list(params={"courierId": non_existent_courier_id})
    verify_response_code(response, 404)
    assert str(non_existent_courier_id) in response.json()["message"]


def test_pass_existent_courier_id_returns_orders_list():
    existent_courier_id = 250114
    response = get_orders_list(params={"courierId": existent_courier_id})
    verify_response_code(response, 200)
    assert isinstance(response.json()["orders"], list)
