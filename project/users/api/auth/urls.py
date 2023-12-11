from django.urls import path
from project.users.api.auth.views import AuthViewSet

urlpatterns = [
    path("login/", AuthViewSet.as_view({"post": "login"})),
    path("refersh/", AuthViewSet.as_view({"post": "refresh"}))
]