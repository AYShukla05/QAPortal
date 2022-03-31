from jwt import InvalidTokenError
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, APIException
from django.db import IntegrityError


def base_exception_handler(exc, context):
    print("Exception", exc)
    # Call DRF's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    print("Exception custom", exc.get_full_details())
    # print("Exception status code is", exc['statusCode'])
    print("Context is:", context)
    # check that a ValidationError exception is
    response.data = {"details": exc}

    # print("\n\n\nExcetion Details\n\n\n\n", exc.details)
    if isinstance(exc, APIException):
        print("Details of APIException", exc.get_full_details())
        print("Codes of APIException", exc.get_codes())
        print("Detail for for APIException", exc.detail)
        response.data = {
            "details": {"message":exc.detail},
            "ErrorDetails": exc.get_full_details(),
        }
        if exc.get_codes() == ["invalid"]:
            response.data = {
                "details": {"message": "Username or email already exists"},
                "Error Details": exc.get_full_details(),
            }
        return response
    if isinstance(exc, InvalidTokenError):
        response.status_code = 401
        response.data = {
            "details": {"message": "Wrong Login Credentials"},
            "Error Details": exc.get_full_details(),
        }
        print("\n\n\n\nResponse", response)
        return response

    if isinstance(exc, ValidationError):
        # here prepare the 'custom_error_response' and
        # set the custom response data on response object
        print("\n\n\nValidation Error")
        response.data = {
            "details": {"message": "Username or email already exists"},
            "Error Details": exc.get_full_details(),
        }
        response.status_code = 401
        return response

    response.message = exc
    print("Response is \n\n\n\n\n\n\n\n", response)
    return response
