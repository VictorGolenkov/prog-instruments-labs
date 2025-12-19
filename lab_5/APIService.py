"""Модуль для взаимодействия с внешними API сервисами.

Содержит класс ExternalAPIService для получения данных о геолокации
и погоде из внешних REST API.
"""

import logging
import requests

logger = logging.getLogger('ExternalAPI')

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
        
        logger.info("Запрос геолокации из внешнего API")
        
        try:
            logger.debug(f"Отправка запроса к {cls.IP_INFO_WEBSITE_LINK}")
            response = requests.get(cls.IP_INFO_WEBSITE_LINK, timeout=10)
            response.raise_for_status()
            
            logger.debug(f"Получен ответ со статусом: {response.status_code}")
            data = response.json()
            
            if 'loc' not in data:
                logger.error("Ключ 'loc' отсутствует в ответе API")
                raise KeyError("Location data not found in response")
            
            location = data['loc']
            logger.info(f"Геолокация успешно получена: {location}")
            return location
            
        except KeyError as e:
            logger.error(f"Ошибка структуры данных API: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении геолокации: {str(e)}", exc_info=True)
            raise

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
        
        logger.info(f"Запрос температуры для города {cls.CITY_NAME}")
        
        try:
            weather_api_url = (f"{cls.WEATHER_WEBSITE_LINK}"
                           f"&q={cls.CITY_NAME}"
                           f"&appid={cls.WEATHER_WEBSITE_API_KEY}")
            
            logger.debug(f"Отправка запроса к OpenWeatherMap API")
            response = requests.get(weather_api_url, timeout=10)
            response.raise_for_status()
            
            logger.debug(f"Получен ответ со статусом: {response.status_code}")
            data = response.json()
            
            if 'main' not in data or 'temp' not in data['main']:
                logger.error("Данные о температуре отсутствуют в ответе API")
                raise KeyError("Temperature data not found in response")
            
            temperature = data['main']['temp']
            logger.info(f"Температура успешно получена: {temperature}°C")
            return temperature
            
        except KeyError as e:
            logger.error(f"Ошибка структуры данных API: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении температуры: {str(e)}", exc_info=True)
            raise