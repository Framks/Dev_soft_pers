
class InvalidArgumentException(Exception):
    def __init__(self,field, message):
        self.message = f"Erro no campo '{field}': {message}"
        super().__init__(f"Erro no campo '{field}': {message}")

class NotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class OperationalException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class ValidationException(Exception):
    def __init__(self, message: str, errors: list):
        self.message = message
        self.errors = errors

    def errors(self):
        return self.errors