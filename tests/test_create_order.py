from methods import create_order, verify_response_code

import allure
import pytest


class TestCreateOrder:
    @allure.title('Заказ создаётся при разных значениях параметра color')
    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None
        ]
    )
    def test_color(self, color):
        response = create_order(color=color)
        verify_response_code(response, 201)
        assert isinstance(response.json()["track"], int)
