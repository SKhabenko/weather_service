import aiohttp
from urllib.parse import urlencode

from aiohttp import ClientResponse, ContentTypeError

from exceptions import APIException
from logger import db_logger

logger = db_logger


class OpenWeatherClient:
    def __init__(self, base_url: str, appid: str) -> None:
        self.base_url = base_url
        self.appid = appid

    async def get_weather(self, city: str, units: str):
        """
        Получение данных о погоде у сервиса OpenWeatherMap
        :param city: Город, для которого требуется получить информацию о погоде.
        :param units: Система измерения, в которой возвращается результат.
                      Может принимать значения:
                      * imperial (Фаренгейт)
                      * metric (Градусы Цельсия)
                      * default (Кельвины)
        """
        args = {
            "q": city,
            "units": units
        }
        return await self._call("GET", "/weather", args)

    async def _call(self, method: str, path: str, args: dict):
        """
        Выолнение HTTP запроса на сервер
        """
        headers = {}
        url = '{}{}'.format(self.base_url, path)
        args.update(
            appid=self.appid
        )

        logger.info(f"Send request to OpenWeather. method={method}; url={url}; body={args}")
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url, params=urlencode(args), headers=headers) as response:
                    # В случае ошибки при обращении к API транслируем ошибку сервиса OpenWeather
                    text = await response.text()
                    if response.status != 200:
                        logger.error(
                            f"Unsuccessful response from OpenWeather: "
                            f"code={response.status}, body: {text}",
                        )
                        raise APIException(
                            message="Unsuccessful response code from OpenWeather",
                            details=text,
                            http_code=response.status
                        )
                    logger.info(f"Got response from OpenWeather. body={text}")

                    return await self._parse_response(response)

        except Exception:
            logger.error('Unhandled exception while make request to OpenWeather')
            raise

    async def _parse_response(self, response: 'ClientResponse') -> dict:
        """
        Метод разбирает ответ сервиса OpenWeather,
        и подставляет в ответ только интересующие значения.
        """
        try:
            data = await response.json()
            result = {
                "temp": data["main"]["temp"],
                "temp_min": data["main"]["temp_min"],
                "temp_max": data["main"]["temp_max"],
            }
            return result
        except ContentTypeError:
            logger.error('Unexpected format OpenWeather')
            raise APIException(
                message="External services error",
                http_code=500
            )
