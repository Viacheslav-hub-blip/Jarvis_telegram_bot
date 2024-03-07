from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    return (f"{weather.city}, температура {weather.temperature}°C, ощущается как {weather.temperature_feels_like}\n"
            f"минимальная температура {weather.temperature_min}\n"
            f"максимальная температура {weather.temperature_max}\n"
            f"скорость ветра {weather.wind} м/c. \n"
            f"{weather.weather_type}. \n"
            f"Восход: {weather.sunrise.strftime('%H:%M')}.\n"
            f"Закат: {weather.sunset.strftime('%H:%M')}\n")