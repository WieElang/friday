import json
from typing import Any, Optional
from django.forms import Form

from rest_framework import status
from rest_framework.response import Response


class ErrorResponse(Response):
    """
    Subclassed `Response` from rest_framework to simplify constructing error messages
    """

    def __init__(self, form: Optional[Form] = None, **kwargs: Any) -> None:
        super().__init__(status=status.HTTP_400_BAD_REQUEST)

        data = kwargs

        if form is not None and form.errors:
            field, errors = list(json.loads(form.errors.as_json()).items())[0]
            error_message = errors[0]['message']
            data['error_message'] = error_message
            data["error_code"] = errors[0].get('code') if errors[0].get('code') else "invalid_data"

        self.data = data
