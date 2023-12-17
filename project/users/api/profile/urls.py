from django.urls import path
from project.users.api.profile.views import ProfileViewSet

urlpatterns = [
    path("info/", ProfileViewSet.as_view({"get", "info"}))
]