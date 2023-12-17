from django.urls import path
from project.scenarios.api.views import ScenarioViewSet

urlpatterns = [
    path('upload/', ScenarioViewSet.as_view({"post": "upload"})),
    path('list/', ScenarioViewSet.as_view({"get": "list"})),
    path('get/', ScenarioViewSet.as_view({"get": "get"})),
    path('update/', ScenarioViewSet.as_view({"post": "update"})),
    path('run/', ScenarioViewSet.as_view({"post": "run_scenario"}))
]