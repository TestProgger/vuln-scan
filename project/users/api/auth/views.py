from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from project.utils.response import ResponseHandlerMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from project.users.models import User
from project.users.consts import ResponseError


class AuthViewSet(ViewSet, ResponseHandlerMixin):
    permission_classes = (AllowAny, )

    def login(self, request: Request):
        try:
            user = User.objects.get(username=request.data.get("username"))
            if not user.check_password(request.data.get("password")):
                return self.error_response(message=ResponseError.INVALID_USERNAME_OR_PASSWORD.value)
        except:
            return self.error_response(message=ResponseError.INVALID_USERNAME_OR_PASSWORD.value)

        refresh = RefreshToken.for_user(user)

        return self.success_response(
            body={
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        )

    def refresh(self, request: Request):
        serializer = TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            raise Exception(ResponseError.INVALID_REFRESH_TOKEN.value)
        return self.success_response(
            body={**serializer.validated_data, "refresh": request.data.get("refresh")}
        )
