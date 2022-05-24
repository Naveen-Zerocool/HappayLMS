from functools import wraps

from rest_framework import status

from HappayLMS.standard_responses import StandardResponse


def required_params(params):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if not all(param in request.request.data for param in params):
                return StandardResponse(response_data={}, error={"fields_required": params},
                                        message="Required details not present",
                                        http_status=status.HTTP_400_BAD_REQUEST)
            return func(request, *args, **kwargs)
        return inner
    return decorator
