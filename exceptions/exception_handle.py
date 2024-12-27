from fastapi import Request, Response
from fastapi.exceptions import ValidationException

from exceptions.exceptions import InvalidArgumentException
from exceptions.exceptions import NotFoundException
from exceptions.exceptions import OperationalException


def not_found_exception(request: Request, exc: NotFoundException) -> Response:
    return Response(
        status_code=404,
        content={"message": exc.message}
    )

def invalid_argument_exception(request: Request, exc: InvalidArgumentException) -> Response:
    return Response(
        status_code=400,
        content={"message": exc.message}
    )

def operational_exception(request: Request, exc: OperationalException) -> Response:
    return Response(
        status_code=400,
        content={"message": exc.message}
    )

def validation_exception_handle(request: Request, exc: ValidationException) -> Response:
    return Response(
        status_code=422,
        content={"message": "Os dados fornecidos não são válidos.", "errors": exc.errors()}
    )

def exception_handle(request: Request, exc: Exception) -> Response:
    return Response(
        status_code=400,
        content={"Bad-Request": str(exc)}
    )