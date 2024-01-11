from methods import get_orders_list, verify_response_code

import allure


class TestListOrders:
    @allure.title('Запрос списка заказов без courierId успешно возвращает список заказов')
    def test_not_pass_courier_id_returns_orders_list(self):
        response = get_orders_list()
        verify_response_code(response, 200)
        assert isinstance(response.json()["orders"], list)

    @allure.title('Запрос списка заказов для несуществующего courierId завершается ошибкой')
    def test_pass_non_existent_courier_id_returns_error(self):
        non_existent_courier_id = 999999
        response = get_orders_list(params={"courierId": non_existent_courier_id})
        verify_response_code(response, 404)
        assert str(non_existent_courier_id) in response.json()["message"]

    @allure.title('Запрос списка заказов с существующим courierId успешно возвращает список заказов')
    def test_pass_existent_courier_id_returns_orders_list(self):
        existent_courier_id = 250114
        response = get_orders_list(params={"courierId": existent_courier_id})
        verify_response_code(response, 200)
        assert isinstance(response.json()["orders"], list)
