from django.urls import path
from project.processes.api.views import ProcessViewSet


urlpatterns = [
    path('list-last-process-messages/', ProcessViewSet.as_view({"get": "list_last_process_messages"})),
    path('run-process/', ProcessViewSet.as_view({"post": "run_process"}))
]