from methods import create_order, verify_response_code

import pytest


@pytest.mark.parametrize(
    "color",
    [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ]
)
def test_color(color):
    response = create_order(color=color)
    verify_response_code(response, 201)
    assert isinstance(response.json()["track"], int)
