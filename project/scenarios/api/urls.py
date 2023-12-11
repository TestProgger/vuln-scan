from django.urls import path
from project.scenarios.api.views import ScenarioViewSet

urlpatterns = [
    path('upload/', ScenarioViewSet.as_view({"post": "upload"})),
    path('list/', ScenarioViewSet.as_view({"get", "list"})),
    path('run/', ScenarioViewSet.as_view({"post": "run_scenario"}))
]