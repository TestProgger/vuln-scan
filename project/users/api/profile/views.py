from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from project.utils.response import ResponseHandlerMixin


class ProfileViewSet(ViewSet, ResponseHandlerMixin):
    permission_classes = (IsAuthenticated, )

    def info(self, request: Request):
        return self.success_response(
            body={
                "id": request.user.id,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "middle_name": request.user.middle_name,
            }
        )