from rest_framework import status
from rest_framework.response import Response


class ResponseHandlerMixin:
    def form_response(self, body=None, message="OK", code=status.HTTP_200_OK):
        return Response(
            {
                "body": body if body else {},
                "status": {
                    "code": code,
                    "message": message,
                },
            },
            status=status.HTTP_200_OK,
        )

    def success_response(self, body=None):
        return self.form_response(
            body=body if body else {},
        )

    def error_response(self, message: str, body=None,  code: int = status.HTTP_400_BAD_REQUEST):
        return self.form_response(
            body=body if body else {},
            message=message,
            code=code
        )