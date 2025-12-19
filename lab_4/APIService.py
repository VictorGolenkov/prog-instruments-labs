"""Модуль для взаимодействия с внешними API сервисами.

Содержит класс ExternalAPIService для получения данных о геолокации
и погоде из внешних REST API.
"""

import requests


class ExternalAPIService:
    """Класс для получения данных из внешних API сервисов.
    
    Предоставляет методы для получения текущей геолокации пользователя
    и температуры в указанном городе. Все конфигурационные параметры
    хранятся как атрибуты класса.
    
    Attributes:
        IP_INFO_WEBSITE_LINK (str): URL API сервиса для определения геолокации.
        CITY_NAME (str): Название города для получения данных о погоде.
        WEATHER_WEBSITE_LINK (str): Базовый URL API сервиса погоды.
        WEATHER_WEBSITE_API_KEY (str): API ключ для доступа к сервису погоды.
    
    Methods:
        fetch_location: Получает текущие координаты местоположения.
        fetch_temperature: Получает текущую температуру в указанном городе.
    """
    
    IP_INFO_WEBSITE_LINK = "https://ipinfo.io/"
    CITY_NAME = "Samara"
    WEATHER_WEBSITE_LINK = "http://api.openweathermap.org/data/2.5/weather?units=metric"
    WEATHER_WEBSITE_API_KEY = "c6e315d09197cec231495138183954bd"

    @classmethod
    def fetch_location(cls) -> str:
        """Получает текущие географические координаты местоположения.
        
        Использует сервис ipinfo.io для определения координат устройства
        по его IP-адресу. Возвращает строку в формате "широта,долгота".
        
        Returns:
            str: Строка с координатами в формате "широта,долгота".
        
        Raises:
            requests.RequestException: При ошибках сетевого соединения.
            KeyError: Если API ответ не содержит ожидаемых данных.
            JSONDecodeError: Если ответ не является валидным JSON.
        """
        
        response = requests.get(cls.IP_INFO_WEBSITE_LINK)
        data = response.json()
        location: str = data['loc']
        return location

    @classmethod
    def fetch_temperature(cls) -> float:
        """Получает текущую температуру воздуха в указанном городе.
        
        Использует OpenWeatherMap API для получения текущих погодных условий
        в городе, указанном в атрибуте класса CITY_NAME.
        
        Returns:
            float: Температура в градусах Цельсия.
        
        Raises:
            requests.RequestException: При ошибках сетевого соединения.
            KeyError: Если API ответ не содержит ожидаемых данных.
            JSONDecodeError: Если ответ не является валидным JSON.
        """
        
        weather_api_url = (f"{cls.WEATHER_WEBSITE_LINK}"
                       f"&q={cls.CITY_NAME}"
                       f"&appid={cls.WEATHER_WEBSITE_API_KEY}")
 
        response = requests.get(weather_api_url)
        data = response.json()
        temperature = data['main']['temp']
        return temperature