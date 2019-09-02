import os

from aiohttp import web
from cerberus import Validator

from exceptions import APIException
from logger import db_logger
from open_weather_client import OpenWeatherClient


client = OpenWeatherClient(
    base_url=os.getenv('OPEN_WEATHER_URL', "https://api.openweathermap.org/data/2.5"),
    appid=os.getenv('OPEN_WEATHER_SECRET_KEY', '123'),
)

logger = db_logger


class Handler:
    """
    Базовый хендлер для верхнеуровневой обработки запросов.
    Выполняет дополнительный "отлов" ошибок, и приведение их к человекочитаемому типу.
    """
    async def get(self, request):
        try:
            logger.info(f"Get new request - {request.query}")
            result = await self._perform_get(dict(request.query))
            return web.json_response(result)
        except Exception as e:
            if not isinstance(e, APIException):
                logger.exception("Unhandled error - {}", e, exc_info=True)
                e = APIException(
                    message="Oops, something happens !:(",
                    http_code=500
                )
            return web.json_response(
                data=e.to_error(),
                status=e.http_code
            )

    async def _perform_get(self, request):
        raise NotImplementedError("Method must be define in child class")


class Weather(Handler):
    request_schema = {
        "city": {
            "type": "string",
            "required": True,
            "regex": "^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$"
        },
        "units": {
            "type": "string",
            "required": False,
            "default": "default"

        }
    }
    validator = Validator(request_schema, allow_unknown=False)

    async def _perform_get(self, params: dict) -> dict:
        """
        Метод, содержащий общую логику получения данных о
        погоде для запрашиваемого города.
        """

        if not self.validator.validate(params):
            logger.error("Failed to validate incoming params")
            raise APIException(
                message="Unexpected request message",
                details=self.validator.errors
            )

        weather = await client.get_weather(
            city=self.validator.document["city"],
            units=self.validator.document["units"],
        )

        # Добавляем к ответу единицы измерения
        weather["units"] = self.validator.document["units"]

        # Поле `response` используется для пробрасывания на клиента расширенной информации
        # об ошибке. В случае успешной операции так же возвращается для унификации API.
        result = {
            "weather": weather,
            "response": {}
        }
        return result
