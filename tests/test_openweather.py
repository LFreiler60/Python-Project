import pytest

from services.openweather import OpenWeatherService


def test_fahrenheit_to_celsius():
    result = OpenWeatherService.fahrenheit_to_celsius(32)

    assert result == pytest.approx(0)


def test_meters_to_miles():
    result = OpenWeatherService.meters_to_miles(1609.34)

    assert result == pytest.approx(1)