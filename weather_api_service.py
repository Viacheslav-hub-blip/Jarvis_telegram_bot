from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json
from json.decoder import JSONDecodeError
import ssl
from typing import Literal, TypeAlias
import urllib.request
from urllib.error import URLError

import config
from exeptions import ApiServiceError

Celsius: TypeAlias = float


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    temperature_feels_like: float
    temperature_max: float
    temperature_min: float
    weather_type: WeatherType
    wind: float
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(city: str) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        city=city)
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(city: str) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(
        city=city)
    #print(url)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
        print(openweather_dict)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        temperature_feels_like=_parse_temperature_feels_like(openweather_dict),
        temperature_max=_parse_temperature_max(openweather_dict),
        temperature_min=_parse_temperature_min(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        wind=_parse_wind(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, "sunrise"),
        sunset=_parse_sun_time(openweather_dict, "sunset"),
        city=_parse_city(openweather_dict)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    print(openweather_dict["main"])
    return round(openweather_dict["main"]["temp"])


def _parse_temperature_feels_like(openweather_dict: dict) -> float:
    return openweather_dict["main"]["feels_like"]


def _parse_temperature_max(openweather_dict: dict) -> float:
    return openweather_dict["main"]["temp_max"]


def _parse_temperature_min(openweather_dict: dict) -> float:
    return openweather_dict["main"]["temp_min"]


def _parse_wind(openweather_dict: dict) -> float:
    return openweather_dict["wind"]["speed"]


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_sun_time(
        openweather_dict: dict,
        time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict["sys"][time])


def _parse_city(openweather_dict: dict) -> str:
    try:
        return openweather_dict["name"]
    except KeyError:
        raise ApiServiceError


if __name__ == "__main__":
    print(get_weather("Moscow"))
