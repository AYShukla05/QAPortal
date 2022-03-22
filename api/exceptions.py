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
    if isinstance(exc, APIException):
        print("Details of APIException", exc.get_full_details())
        response.data = {"details": exc.get_full_details()}
    elif isinstance(exc, ValidationError):
        # here prepare the 'custom_error_response' and
        # set the custom response data on response object
        response.data = {
            "details": {"message":"Username or email already exists"},
            "Error Details": exc.get_full_details(),
        }
        response.status_code = 401
    # print("Response is \n\n\n\n\n\n\n\n", response)
    return response
