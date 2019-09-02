

class APIException(Exception):
    """
    Общее исключение, выбрасываемое функциями API.
    """
    def __init__(
            self, message: str = None, details: str = None, http_code: int = 500,
    ):
        super(APIException, self).__init__()
        details = details or {}

        self.message = message
        self.details = details
        self.http_code = http_code

    def to_error(self):
        return api_error(
            message=self.message,
            details=self.details,
        )


def api_error(message=None, details=None) -> dict:
    """
    Структура, описывающая неуспешный ответ от API.
    """
    return {
        'weather': {},
        'response': {
            'message': message,
            'details': details
        }
    }
